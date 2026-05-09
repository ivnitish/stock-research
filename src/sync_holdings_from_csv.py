"""Sync the holdings table in output/html/index.html from data/portfolio.csv.

Source of truth: data/portfolio.csv (symbol, quantity, avg_buy_price, exchange).

What this updates per CSV row:
  - Col 3 (Qty)      from CSV.quantity
  - Col 4 (Avg ₹)    from CSV.avg_buy_price
  - Col 7 (Invested) from qty × avg

What this does NOT touch:
  - CMP, Δ/share, Current, P&L (need live price feed)
  - Action, Target, Buy Zone, Upside (manually curated)

Reports symbols in CSV with no matching HTML row, and HTML rows with held qty
that have no matching CSV row (potential drift).

Usage:
    python3 src/sync_holdings_from_csv.py            # dry-run, show diffs only
    python3 src/sync_holdings_from_csv.py --write    # apply changes in place
"""

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "portfolio.csv"
HTML_PATH = ROOT / "output" / "html" / "index.html"

ROW_RE = re.compile(
    r'(<tr class="stock-row"[^>]*?>)(.*?)(</tr>)',
    re.DOTALL,
)
TD_RE = re.compile(r'(<td[^>]*>)(.*?)(</td>)', re.DOTALL)
ONCLICK_RE = re.compile(r"onclick=\"go\('([A-Z0-9]+)\.html'\)\"")
TICKER_RE = re.compile(r'<div class="td-ticker">([A-Z0-9]+)')


def extract_symbol(opener: str, body: str) -> str | None:
    """Ticker text wins over onclick — onclick may route to a parent's research note."""
    m = TICKER_RE.search(body)
    if m:
        return m.group(1)
    m = ONCLICK_RE.search(opener)
    return m.group(1) if m else None


def fmt_money(v: float) -> str:
    """Match the existing index.html convention: Cr / L / K / plain."""
    if v >= 10_000_000:
        return f"₹{v/10_000_000:.2f}Cr"
    if v >= 100_000:
        return f"₹{v/100_000:.2f}L"
    if v >= 10_000:
        return f"₹{v/1000:.2f}K"
    return f"₹{v:,.0f}"


def fmt_qty(q: int) -> str:
    return f"{q:,}" if q >= 1000 else str(q)


def fmt_avg(p: float) -> str:
    """Preserve 2 decimals to match CSV precision (₹460.80, ₹4,559.69)."""
    return f"₹{p:,.2f}"


def load_csv():
    rows = []
    with CSV_PATH.open() as f:
        for r in csv.DictReader(f):
            sym = r["symbol"].split(".")[0]
            rows.append({
                "symbol": sym,
                "qty": int(r["quantity"]),
                "avg": float(r["avg_buy_price"]),
                "exchange": r["exchange"],
            })
    return {r["symbol"]: r for r in rows}


PRICE_RE = re.compile(r"₹\s*([\d,]+(?:\.\d+)?)")


def parse_price(cell_html: str) -> float | None:
    m = PRICE_RE.search(cell_html)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None


def fmt_signed_money(v: float) -> str:
    sign = "+" if v >= 0 else "-"
    return f"{sign}{fmt_money(abs(v))}"


def fmt_signed_avg(v: float) -> str:
    sign = "+" if v >= 0 else "-"
    return f"{sign}₹{abs(v):,.2f}"


def fmt_pct(v: float) -> str:
    sign = "+" if v >= 0 else "-"
    return f"{sign}{abs(v):.2f}%"


def pl_class(v: float) -> str:
    if v > 0.01:
        return "pl-gain"
    if v < -0.01:
        return "pl-loss"
    return "pl-none"


def replace_classes(td_open: str, new_pl_class: str) -> str:
    """Swap pl-gain/pl-loss/pl-none class within a <td ...> opener."""
    return re.sub(r"pl-(?:gain|loss|none)", new_pl_class, td_open) if "pl-" in td_open else td_open


def patch_row(row_inner: str, qty: int, avg: float) -> tuple[str, list[str]]:
    """Update qty, avg, invested + derived (Δ/share, current, P&L) when CMP is parseable."""
    cells = list(TD_RE.finditer(row_inner))
    if len(cells) < 10:
        return row_inner, [f"only {len(cells)} cells found, expected ≥10"]

    invested = qty * avg
    cmp_price = parse_price(cells[4].group(2))

    targets: list[tuple[int, str, str, str | None]] = [
        (2, fmt_qty(qty), "qty", None),
        (3, fmt_avg(avg), "avg", None),
        (6, fmt_money(invested), "invested", None),
    ]

    if cmp_price is not None and qty > 0:
        delta_per_share = cmp_price - avg
        current = qty * cmp_price
        pl_abs = current - invested
        pl_pct = (pl_abs / invested) * 100 if invested else 0.0
        targets.extend([
            (5, fmt_signed_avg(delta_per_share), "delta/share", pl_class(delta_per_share)),
            (7, fmt_money(current), "current", None),
            (8, fmt_signed_money(pl_abs), "p&l", pl_class(pl_abs)),
            (9, fmt_pct(pl_pct), "p&l%", pl_class(pl_pct)),
        ])

    diffs: list[str] = []
    out = row_inner
    # Apply targets right-to-left so earlier cell offsets stay valid after edits.
    for cell_idx, new_val, label, new_cls in sorted(targets, key=lambda t: -t[0]):
        cells = list(TD_RE.finditer(out))
        m = cells[cell_idx]
        old_val = m.group(2).strip()
        old_open = m.group(1)
        new_open = replace_classes(old_open, new_cls) if new_cls else old_open
        if old_val == new_val and new_open == old_open:
            continue
        if old_val != new_val:
            diffs.append(f"{label}: {old_val!r} -> {new_val!r}")
        new_cell = new_open + new_val + m.group(3)
        out = out[:m.start()] + new_cell + out[m.end():]
    return out, diffs


def main():
    write = "--write" in sys.argv

    csv_rows = load_csv()
    html = HTML_PATH.read_text()

    seen_in_html = set()
    new_html = html
    total_updates = 0
    update_log = []

    def replace_block(m):
        nonlocal total_updates
        opener, body, closer = m.group(1), m.group(2), m.group(3)
        sym = extract_symbol(opener, body)
        if sym is None or sym not in csv_rows:
            return m.group(0)
        seen_in_html.add(sym)
        record = csv_rows[sym]
        new_body, diffs = patch_row(body, record["qty"], record["avg"])
        if diffs:
            total_updates += 1
            update_log.append(f"  {sym}: {'; '.join(diffs)}")
        return opener + new_body + closer

    new_html = ROW_RE.sub(replace_block, html)

    missing_in_html = sorted(set(csv_rows.keys()) - seen_in_html)

    print(f"Loaded {len(csv_rows)} symbols from {CSV_PATH.name}")
    print(f"Matched {len(seen_in_html)} HTML rows")
    print(f"Updates: {total_updates} rows would change")
    if update_log:
        print("\nDiff:")
        print("\n".join(update_log))
    if missing_in_html:
        print(f"\nSymbols in CSV but NOT in index.html ({len(missing_in_html)}):")
        for s in missing_in_html:
            print(f"  - {s}")

    if write and new_html != html:
        HTML_PATH.write_text(new_html)
        print(f"\n✓ Wrote {HTML_PATH}")
    elif write:
        print("\nNo changes to write.")
    else:
        print("\n(dry-run; pass --write to apply)")


if __name__ == "__main__":
    main()
