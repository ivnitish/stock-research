"""Single-command portfolio refresh.

Reads the latest broker holdings export (xlsx) from data/broker-exports/,
joins with data/portfolio.csv, and refreshes output/html/index.html:

  - CMP cell (col 4) for each held row, from broker close price
  - Derived cells: Δ/share, current value, P&L abs, P&L % (re-uses
    sync_holdings_from_csv logic — qty/avg are already kept in sync)
  - Top-of-page Portfolio Snapshot block: invested, current, P&L,
    weighted expected 3-yr CAGR (from each row's base-case target cell)

Also flags stale research file Status: headers (research/<SYMBOL>.md
header still saying EXITED while portfolio.csv shows held qty).

Source-of-truth chain:
  broker xlsx (closing price) + portfolio.csv (qty, avg)
                         ↓
                 index.html row state
                         ↓
              Portfolio Snapshot block

Usage:
    python3 src/refresh_portfolio.py              # dry run, print snapshot
    python3 src/refresh_portfolio.py --write      # apply changes in place
    python3 src/refresh_portfolio.py --horizon 5  # 5-yr CAGR instead of 3-yr
"""

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "portfolio.csv"
HTML_PATH = ROOT / "output" / "html" / "index.html"
BROKER_DIR = ROOT / "data" / "broker-exports"
RESEARCH_DIR = ROOT / "research"

# Broker export uses ISIN; portfolio.csv uses symbol. Add new entries when
# adding new positions — script will warn if an ISIN appears with no mapping.
ISIN_TO_SYMBOL: dict[str, str] = {
    "INE242C01024": "ANANTRAJ",
    "INE025R01021": "ARTEMISMED",
    "INE0LEZ01016": "ATHERENERG",
    "INE213C01025": "BANCOINDIA",
    "INE257A01026": "BHEL",
    "INE506A01018": "DREDGECORP",
    "INE0MLS01022": "EPACKPEB",
    "INE758T01015": "ETERNAL",
    "INE382Z01011": "GRSE",
    "INE346A01027": "ICICIAMC",
    "INE202H01019": "KERNEX",
    "INE317F01035": "NESCO",
    "INE619B01017": "NEWGEN",
    "INE882B01037": "NWIL",
    "INE082C01024": "PATELSAI",
    "INE301A01014": "RAYMOND",
    "INE667G01023": "SAKSOFT",
    "INE024F01011": "SHILCTECH",
    "INE980Y01015": "SOUTHWEST",
    "INE1VXE01018": "STLNETWORK",
    "INE00H001014": "SWIGGY",
    "INE628D01014": "THRIVE",
    "INE251B01027": "ZENTEC",
}

DEFAULT_HORIZON_YEARS = 3

# ---------- regex helpers (mirrored from sync_holdings_from_csv.py) ----------
ROW_RE = re.compile(r'(<tr class="stock-row"[^>]*?>)(.*?)(</tr>)', re.DOTALL)
TD_RE = re.compile(r"(<td[^>]*>)(.*?)(</td>)", re.DOTALL)
ONCLICK_RE = re.compile(r"onclick=\"go\('([A-Z0-9]+)\.html'\)\"")
TICKER_RE = re.compile(r'<div class="td-ticker">([A-Z0-9]+)')
PRICE_RE = re.compile(r"₹\s*([\d,]+(?:\.\d+)?)")
SNAPSHOT_RE = re.compile(
    r"<!-- BEGIN_PORTFOLIO_SNAPSHOT -->.*?<!-- END_PORTFOLIO_SNAPSHOT -->",
    re.DOTALL,
)


def extract_symbol(opener: str, body: str) -> str | None:
    m = TICKER_RE.search(body)
    if m:
        return m.group(1)
    m = ONCLICK_RE.search(opener)
    return m.group(1) if m else None


def parse_price(cell_html: str) -> float | None:
    m = PRICE_RE.search(cell_html)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None


def fmt_money(v: float) -> str:
    if v >= 10_000_000:
        return f"₹{v/10_000_000:.2f}Cr"
    if v >= 100_000:
        return f"₹{v/100_000:.2f}L"
    if v >= 10_000:
        return f"₹{v/1000:.2f}K"
    return f"₹{v:,.0f}"


def fmt_cmp(v: float) -> str:
    """Match index.html convention: comma-separated, 2dp for <1000, 0dp otherwise."""
    if v < 1000:
        return f"₹{v:.2f}"
    return f"₹{v:,.0f}"


def fmt_qty(q: int) -> str:
    return f"{q:,}" if q >= 1000 else str(q)


def fmt_avg(p: float) -> str:
    return f"₹{p:,.2f}"


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
    return re.sub(r"pl-(?:gain|loss|none)", new_pl_class, td_open) if "pl-" in td_open else td_open


# ---------- loaders ----------
def load_csv() -> dict[str, dict]:
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


def find_latest_broker_export() -> Path:
    candidates = list(BROKER_DIR.rglob("*Holdings*.xlsx"))
    if not candidates:
        candidates = list(BROKER_DIR.rglob("*.xlsx"))
    if not candidates:
        raise FileNotFoundError(f"No broker xlsx found under {BROKER_DIR}")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def parse_broker_export(path: Path) -> tuple[dict[str, dict], str, dict[str, float]]:
    """Return (symbol -> broker row, snapshot_date, totals dict)."""
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))

    snapshot_date = "unknown"
    invested_total = current_total = pnl_total = 0.0
    for row in rows:
        if not row:
            continue
        first = row[0]
        if isinstance(first, str):
            if first.startswith("Holdings statement for stocks as on"):
                snapshot_date = first.split("as on")[-1].strip()
            elif first == "Invested Value" and len(row) > 1 and row[1] is not None:
                invested_total = float(row[1])
            elif first == "Closing Value" and len(row) > 1 and row[1] is not None:
                current_total = float(row[1])
            elif first == "Unrealised P&L" and len(row) > 1 and row[1] is not None:
                pnl_total = float(row[1])

    header_idx = None
    for i, row in enumerate(rows):
        if row and row[0] == "Stock Name":
            header_idx = i
            break
    if header_idx is None:
        raise ValueError(f"No header row found in {path.name}")

    holdings: dict[str, dict] = {}
    unmapped_isins: list[str] = []
    for row in rows[header_idx + 1:]:
        if not row or not row[1]:
            continue
        name, isin, qty, avg, invested, close, current, pnl = row[:8]
        sym = ISIN_TO_SYMBOL.get(str(isin).strip())
        if not sym:
            unmapped_isins.append(f"{isin} ({name})")
            continue
        holdings[sym] = {
            "name": name,
            "isin": isin,
            "qty": float(qty),
            "avg": float(avg),
            "close": float(close),
            "invested": float(invested),
            "current": float(current),
            "pnl": float(pnl),
        }

    if unmapped_isins:
        print(f"⚠ Unmapped ISINs in broker export ({len(unmapped_isins)}):")
        for u in unmapped_isins:
            print(f"    {u}")
        print("  → Add to ISIN_TO_SYMBOL in src/refresh_portfolio.py")

    totals = {"invested": invested_total, "current": current_total, "pnl": pnl_total}
    return holdings, snapshot_date, totals


# ---------- row patching ----------
def patch_row(row_inner: str, qty: int, avg: float, cmp_price: float | None) -> tuple[str, list[str], dict | None]:
    """Update qty/avg/CMP/derived cells. Return new body, diffs, and per-row stats."""
    cells = list(TD_RE.finditer(row_inner))
    if len(cells) < 10:
        return row_inner, [f"only {len(cells)} cells"], None

    invested = qty * avg

    targets: list[tuple[int, str, str, str | None]] = [
        (2, fmt_qty(qty), "qty", None),
        (3, fmt_avg(avg), "avg", None),
        (6, fmt_money(invested), "invested", None),
    ]

    stats = None
    if cmp_price is not None and qty > 0:
        delta = cmp_price - avg
        current = qty * cmp_price
        pl_abs = current - invested
        pl_pct = (pl_abs / invested) * 100 if invested else 0.0
        targets.extend([
            (4, fmt_cmp(cmp_price), "cmp", None),
            (5, fmt_signed_avg(delta), "delta/share", pl_class(delta)),
            (7, fmt_money(current), "current", None),
            (8, fmt_signed_money(pl_abs), "p&l", pl_class(pl_abs)),
            (9, fmt_pct(pl_pct), "p&l%", pl_class(pl_pct)),
        ])
        # Pull base-case target from cell 11 (if it parses as a price).
        target_price = None
        if len(cells) >= 12:
            target_price = parse_price(cells[11].group(2))
        stats = {
            "qty": qty,
            "avg": avg,
            "cmp": cmp_price,
            "current": current,
            "invested": invested,
            "pnl": pl_abs,
            "target": target_price,
        }

    diffs: list[str] = []
    out = row_inner
    for cell_idx, new_val, label, new_cls in sorted(targets, key=lambda t: -t[0]):
        cells = list(TD_RE.finditer(out))
        if cell_idx >= len(cells):
            continue
        m = cells[cell_idx]
        old_val = m.group(2).strip()
        old_open = m.group(1)
        new_open = replace_classes(old_open, new_cls) if new_cls else old_open
        if old_val == new_val and new_open == old_open:
            continue
        if old_val != new_val:
            diffs.append(f"{label}: {old_val!r} → {new_val!r}")
        out = out[:m.start()] + new_open + new_val + m.group(3) + out[m.end():]
    return out, diffs, stats


# ---------- snapshot block ----------
def render_snapshot_block(
    invested: float,
    current: float,
    pnl: float,
    pnl_pct: float,
    weighted_cagr: float,
    cagr_coverage_pct: float,
    snapshot_date: str,
    num_holdings: int,
    horizon_years: int,
) -> str:
    pnl_color = "#166534" if pnl >= 0 else "#991b1b"
    pnl_sign = "+" if pnl >= 0 else ""
    cagr_color = "#1e40af" if weighted_cagr >= 0 else "#991b1b"
    return f'''<!-- BEGIN_PORTFOLIO_SNAPSHOT -->
<div id="portfolio-snapshot" style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:18px 22px;margin:14px auto 24px;max-width:1200px;font-family:-apple-system,BlinkMacSystemFont,sans-serif">
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px;flex-wrap:wrap;gap:8px">
    <h2 style="margin:0;font-size:1.05rem;font-weight:700;color:#1a1a2e">Portfolio Snapshot</h2>
    <span style="color:#64748b;font-size:0.82rem">as of {snapshot_date} · {num_holdings} holdings</span>
  </div>
  <div style="display:flex;gap:28px;flex-wrap:wrap;font-size:0.93rem;line-height:1.6">
    <div><span style="color:#64748b">Invested:</span> <b>₹{invested/100000:.2f}L</b></div>
    <div><span style="color:#64748b">Current:</span> <b>₹{current/100000:.2f}L</b></div>
    <div><span style="color:#64748b">P&amp;L:</span> <b style="color:{pnl_color}">{pnl_sign}₹{pnl/1000:.2f}K ({pnl_pct:+.2f}%)</b></div>
    <div><span style="color:#64748b">Expected {horizon_years}yr CAGR (base case):</span> <b style="color:{cagr_color}">{weighted_cagr:+.1f}%</b> <span style="color:#94a3b8;font-size:0.82rem">({cagr_coverage_pct:.0f}% coverage)</span></div>
  </div>
</div>
<!-- END_PORTFOLIO_SNAPSHOT -->'''


def insert_snapshot(html: str, block: str) -> str:
    """Replace existing block, or insert just before the table view comment."""
    if SNAPSHOT_RE.search(html):
        return SNAPSHOT_RE.sub(block, html)
    anchor = "<!-- ═══════════ TABLE VIEW ═══════════ -->"
    if anchor in html:
        return html.replace(anchor, block + "\n\n  " + anchor)
    # Fallback: after </h1>
    return html.replace("</h1>", "</h1>\n" + block, 1)


# ---------- stale Status header detection ----------
STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+)$", re.MULTILINE)
EXIT_TOKENS = ("EXIT", "EXITED", "WATCHLIST", "AVOID", "SOLD")


def find_stale_research_files(held_symbols: set[str]) -> list[tuple[str, str]]:
    """Return [(symbol, current Status line)] for files where Status says
    EXITED/WATCHLIST/SOLD but portfolio.csv shows the symbol is still held."""
    stale = []
    for sym in held_symbols:
        path = RESEARCH_DIR / f"{sym}.md"
        if not path.exists():
            continue
        text = path.read_text()
        m = STATUS_RE.search(text)
        if not m:
            continue
        status = m.group(1).strip()
        if any(tok in status.upper() for tok in EXIT_TOKENS) and "OWNED" not in status.upper() and "HOLD" not in status.upper():
            stale.append((sym, status[:120]))
    return stale


# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="apply changes to index.html")
    ap.add_argument("--horizon", type=int, default=DEFAULT_HORIZON_YEARS, help="years for expected CAGR (default 3)")
    args = ap.parse_args()

    # 1. Load broker export + CSV.
    broker_path = find_latest_broker_export()
    print(f"Broker export: {broker_path.relative_to(ROOT)}")
    holdings, snapshot_date, broker_totals = parse_broker_export(broker_path)
    print(f"Snapshot date: {snapshot_date}  |  {len(holdings)} holdings parsed")

    csv_rows = load_csv()
    if set(csv_rows) != set(holdings):
        only_csv = sorted(set(csv_rows) - set(holdings))
        only_broker = sorted(set(holdings) - set(csv_rows))
        if only_csv:
            print(f"⚠ In CSV but not broker: {only_csv}")
        if only_broker:
            print(f"⚠ In broker but not CSV: {only_broker}")

    # 2. Walk index.html rows, patch each held one with broker close.
    html = HTML_PATH.read_text()
    update_log: list[str] = []
    seen: set[str] = set()
    per_stock_stats: list[dict] = []

    def replace_block(m):
        opener, body, closer = m.group(1), m.group(2), m.group(3)
        sym = extract_symbol(opener, body)
        if sym is None or sym not in holdings:
            return m.group(0)
        if sym in seen:
            return m.group(0)  # skip duplicates
        seen.add(sym)
        h = holdings[sym]
        new_body, diffs, stats = patch_row(body, int(h["qty"]), h["avg"], h["close"])
        if stats:
            stats["symbol"] = sym
            per_stock_stats.append(stats)
        if diffs:
            update_log.append(f"  {sym}: {'; '.join(diffs)}")
        return opener + new_body + closer

    new_html = ROW_RE.sub(replace_block, html)

    missing_in_html = sorted(set(holdings) - seen)
    if missing_in_html:
        print(f"⚠ Symbols in broker but no held row in index.html: {missing_in_html}")

    # 3. Compute snapshot totals + weighted CAGR from row stats.
    invested_sum = sum(s["invested"] for s in per_stock_stats)
    current_sum = sum(s["current"] for s in per_stock_stats)
    pnl_sum = current_sum - invested_sum
    pnl_pct = (pnl_sum / invested_sum * 100) if invested_sum else 0.0

    weighted_value = 0.0
    cagr_covered_value = 0.0
    for s in per_stock_stats:
        if s["target"] and s["target"] > 0 and s["cmp"] > 0:
            cagr = ((s["target"] / s["cmp"]) ** (1.0 / args.horizon) - 1.0) * 100
            weighted_value += cagr * s["current"]
            cagr_covered_value += s["current"]
    weighted_cagr = (weighted_value / cagr_covered_value) if cagr_covered_value else 0.0
    cagr_coverage_pct = (cagr_covered_value / current_sum * 100) if current_sum else 0.0

    # 4. Render + insert snapshot block.
    block = render_snapshot_block(
        invested=invested_sum,
        current=current_sum,
        pnl=pnl_sum,
        pnl_pct=pnl_pct,
        weighted_cagr=weighted_cagr,
        cagr_coverage_pct=cagr_coverage_pct,
        snapshot_date=snapshot_date,
        num_holdings=len(per_stock_stats),
        horizon_years=args.horizon,
    )
    new_html = insert_snapshot(new_html, block)

    # 5. Print snapshot to stdout (always, regardless of write flag).
    print()
    print("─" * 76)
    print(f"PORTFOLIO SNAPSHOT  ·  as of {snapshot_date}  ·  {len(per_stock_stats)} holdings")
    print("─" * 76)
    print(f"  Invested:        ₹{invested_sum/100000:,.2f}L  ({fmt_money(invested_sum)})")
    print(f"  Current:         ₹{current_sum/100000:,.2f}L  ({fmt_money(current_sum)})")
    sign = "+" if pnl_sum >= 0 else ""
    print(f"  Unrealised P&L:  {sign}₹{pnl_sum/1000:,.2f}K  ({pnl_pct:+.2f}%)")
    print(f"  Expected {args.horizon}yr CAGR (weighted, base case):  {weighted_cagr:+.1f}%   coverage: {cagr_coverage_pct:.0f}% of current value")

    # Per-stock CAGR breakdown sorted by position size.
    print()
    print(f"  {'Symbol':<14}{'Wt%':>6}{'CMP':>10}{'Target':>10}{'CAGR':>8}{'P&L%':>9}")
    for s in sorted(per_stock_stats, key=lambda x: -x["current"]):
        wt = (s["current"] / current_sum * 100) if current_sum else 0
        cagr_str = "—"
        if s["target"] and s["target"] > 0 and s["cmp"] > 0:
            cagr = ((s["target"] / s["cmp"]) ** (1.0 / args.horizon) - 1.0) * 100
            cagr_str = f"{cagr:+.1f}%"
        pnl_p = ((s["cmp"] - s["avg"]) / s["avg"] * 100) if s["avg"] else 0
        target_str = f"₹{s['target']:,.0f}" if s["target"] else "—"
        print(f"  {s['symbol']:<14}{wt:>5.1f}%{s['cmp']:>10,.2f}{target_str:>10}{cagr_str:>8}{pnl_p:>+8.1f}%")
    print("─" * 76)

    # 6. Stale research file Status: headers.
    held_symbols = {sym for sym, h in holdings.items() if h["qty"] > 1}
    stale = find_stale_research_files(held_symbols)
    if stale:
        print()
        print(f"⚠ Stale research files ({len(stale)}) — held but Status says EXITED/WATCHLIST:")
        for sym, status in stale:
            print(f"    {sym}: {status}")

    # 7. Diff summary + write.
    print()
    print(f"index.html: {len(update_log)} rows would change")
    if update_log:
        print("Per-row diffs:")
        print("\n".join(update_log[:10]))
        if len(update_log) > 10:
            print(f"  ... +{len(update_log) - 10} more")

    if args.write:
        if new_html != html:
            HTML_PATH.write_text(new_html)
            print(f"✓ Wrote {HTML_PATH.relative_to(ROOT)}")
        else:
            print("No HTML changes to write.")
    else:
        print("\n(dry-run; pass --write to apply)")


if __name__ == "__main__":
    main()
