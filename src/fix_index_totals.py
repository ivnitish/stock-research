#!/usr/bin/env python3
"""
Reconcile output/html/index.html with data/portfolio.csv (the source of truth).

Three operations in one pass:
  1. Clear holding cells (qty/avg/CMP/Δ-share/invested/current/P&L₹/P&L%)
     in any row whose ticker is NOT in portfolio.csv but is currently in
     a held section (grade-a/b/c india, tracking india). Re-tag action as
     "Exited". Keep onclick to research file intact. Move row's data-section
     to "watch india" so it falls out of the held bucket.
  2. Recompute India invested + current + P&L from the surviving held rows
     and update the header pf-strip (Invested / Current / P&L) and the
     footer TOTAL PORTFOLIO row.
  3. Bump the "Updated:" timestamp in the pf-strip to today's date.

Run with --write to apply. Default is dry-run.
"""
import argparse
import csv
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "portfolio.csv"
HTML_PATH = ROOT / "output" / "html" / "index.html"

HELD_INDIA_SECTIONS = {"grade-a india", "grade-b india", "grade-c india", "tracking india"}

DASH = "—"


def fmt_money(v: float, prefix: str = "₹") -> str:
    if v >= 1_00_00_000:
        return f"{prefix}{v/1_00_00_000:.2f}Cr"
    if v >= 1_00_000:
        return f"{prefix}{v/1_00_000:.2f}L"
    if v >= 10_000:
        return f"{prefix}{v/1_000:.2f}K"
    return f"{prefix}{v:,.0f}"


def parse_money(s: str) -> float:
    if not s or s.strip() in ("", "—"):
        return 0.0
    m = re.search(r"([\d.,]+)", s)
    if not m:
        return 0.0
    v = float(m.group(1).replace(",", ""))
    if "Cr" in s:
        v *= 1_00_00_000
    elif "L" in s:
        v *= 1_00_000
    elif "K" in s:
        v *= 1_000
    return v


def load_csv_symbols() -> set[str]:
    out = set()
    with open(CSV_PATH) as f:
        for r in csv.DictReader(f):
            sym = r["symbol"].replace(".NS", "").replace(".BO", "")
            out.add(sym)
    return out


def row_section(row: str) -> str:
    m = re.search(r'data-section="([^"]+)"', row)
    return (m.group(1).strip() if m else "")


def row_ticker(row: str) -> str:
    m = re.search(r'<div class="td-ticker">([^<]+)<', row)
    return (m.group(1).strip() if m else "")


def clear_row(row: str) -> str:
    """Reset all holding cells to '—' and re-tag action as Exited.
    Keeps cell structure so other scripts that index by td-position still work."""
    cells = re.findall(r"<td[^>]*>.*?</td>", row, re.DOTALL)
    if len(cells) < 16:
        return row

    def reset_cell(i: int, content: str = DASH, klass: str = "col-hide-sm num-cell num-dim") -> str:
        return f'<td class="{klass}">{content}</td>'

    new_cells = list(cells)
    # td[0] ticker — keep
    # td[1] grade — keep
    new_cells[2] = reset_cell(2)       # qty
    new_cells[3] = reset_cell(3)       # avg
    new_cells[4] = reset_cell(4)       # CMP
    new_cells[5] = reset_cell(5)       # Δ/share
    new_cells[6] = reset_cell(6)       # invested
    new_cells[7] = reset_cell(7)       # current
    new_cells[8] = reset_cell(8)       # P&L ₹
    new_cells[9] = '<td class="num-cell pl-none">—</td>'  # P&L %
    new_cells[10] = '<td class="col-hide-sm"><span class="action-tag act-exit">Exited</span></td>'
    # td[11] Target — keep
    # td[12] CMP/Ref — keep
    # td[13] Buy zone — keep
    # td[14] Upside — keep
    # td[15] arrow — keep

    # Rebuild row by slot-replacing each original cell with the new one in order
    new_row = row
    for old, new in zip(cells, new_cells):
        if old != new:
            new_row = new_row.replace(old, new, 1)

    # Move section to "watch india" + downgrade grade
    new_row = re.sub(r'data-section="[^"]+"', 'data-section="watch india"', new_row, count=1)
    new_row = re.sub(r'data-grade="[abc]"', 'data-grade="w"', new_row, count=1)
    # Remove data-action if any
    new_row = re.sub(r' data-action="[^"]+"', "", new_row, count=1)
    return new_row


def collect_held_rows(html: str, held_symbols: set[str]):
    """Return list of (ticker, invested, current) for surviving India held rows."""
    out = []
    pattern = re.compile(r'<tr class="stock-row" data-section="[^"]+"[^>]*>(.*?)</tr>', re.DOTALL)
    for m in pattern.finditer(html):
        row = m.group(0)
        sec = row_section(row)
        if sec not in HELD_INDIA_SECTIONS:
            continue
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
        if len(cells) < 16:
            continue
        sym = row_ticker(row)
        if sym not in held_symbols:
            continue
        inv_text = re.sub(r"<[^>]+>", "", cells[6]).strip()
        cur_text = re.sub(r"<[^>]+>", "", cells[7]).strip()
        inv = parse_money(inv_text)
        cur = parse_money(cur_text)
        if inv > 0:
            out.append((sym, inv, cur))
    return out


def update_pf_strip(html: str, invested: float, current: float, holdings_n: int, date_str: str) -> str:
    pnl = current - invested
    pnl_pct = (pnl / invested * 100) if invested > 0 else 0.0
    pnl_color = "pf-red" if pnl < 0 else "pf-green"
    pnl_sign = "" if pnl < 0 else "+"

    new_strip = (
        f'  <div class="pf-strip">\n'
        f'    <div class="pf-item">Invested: <span>{fmt_money(invested)}</span></div>\n'
        f'    <div class="pf-item">Current: <span>{fmt_money(current)}</span></div>\n'
        f'    <div class="pf-item">P&amp;L: <span class="{pnl_color}">{pnl_sign}{fmt_money(abs(pnl))} ({pnl_sign}{pnl_pct:.2f}%)</span></div>\n'
        f'    <div class="pf-item">Holdings: <span>{holdings_n}</span></div>\n'
        f'    <div class="pf-item">Updated: <span>{date_str}</span></div>\n'
        f"  </div>"
    )
    return re.sub(
        r'  <div class="pf-strip">.*?</div>\s*</div>',
        new_strip + "\n",
        html,
        count=1,
        flags=re.DOTALL,
    )


def update_footer_total(html: str, invested: float, current: float) -> str:
    pnl = current - invested
    pnl_pct = (pnl / invested * 100) if invested > 0 else 0.0
    pnl_sign = "" if pnl < 0 else "+"
    pnl_color = "#f87171" if pnl < 0 else "#22c55e"

    # Try to update the existing TOTAL PORTFOLIO row's three big cells (invested / current / P&L)
    # Pattern: TOTAL PORTFOLIO ... ₹X.XXL India ... ₹X.XXL India ...
    def repl_inv(m):
        prefix = m.group(1)
        return f"{prefix}{fmt_money(invested)} India"

    def repl_cur(m):
        prefix = m.group(1)
        return f"{prefix}{fmt_money(current)} India"

    def repl_pnl(m):
        prefix = m.group(1)
        return f"{prefix}{pnl_sign}{fmt_money(abs(pnl))} India"

    def repl_pct(m):
        prefix = m.group(1)
        return f"{prefix}{pnl_sign}{pnl_pct:.2f}%"

    # Find the TOTAL PORTFOLIO row and update its India number cells.
    total_re = re.compile(r"(TOTAL PORTFOLIO.*?</tr>)", re.DOTALL)
    m = total_re.search(html)
    if not m:
        return html
    block = m.group(1)
    # Invested cell
    block_new = re.sub(
        r"(text-align:right;[^>]*line-height:1\.5;\">)₹[\d.,KLCr]+\s*India",
        lambda mm: f"{mm.group(1)}{fmt_money(invested)} India",
        block,
        count=1,
    )
    # Current cell
    block_new = re.sub(
        r"(font-weight:700; color:white; line-height:1\.5;\">)₹[\d.,KLCr]+\s*India",
        lambda mm: f"{mm.group(1)}{fmt_money(current)} India",
        block_new,
        count=1,
    )
    # P&L cell
    block_new = re.sub(
        r"(line-height:1\.5;\">)[+-]?₹[\d.,KLCr]+\s*India",
        lambda mm: f"{mm.group(1)}{pnl_sign}{fmt_money(abs(pnl))} India",
        block_new,
        count=1,
    )
    # P&L pct cell
    block_new = re.sub(
        r"(font-weight:700; color:#[a-f0-9]+;[^>]*line-height:1\.5;\">)[+-]?[\d.]+%",
        lambda mm: f"{mm.group(1)}{pnl_sign}{pnl_pct:.2f}%",
        block_new,
        count=1,
    )
    return html.replace(block, block_new, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    csv_syms = load_csv_symbols()
    html = HTML_PATH.read_text()

    # Step 1: clear rows in held sections whose ticker is NOT in CSV
    pattern = re.compile(r'<tr class="stock-row" data-section="[^"]+"[^>]*>.*?</tr>', re.DOTALL)
    cleared = []
    new_html = html
    for m in pattern.finditer(html):
        row = m.group(0)
        sec = row_section(row)
        if sec not in HELD_INDIA_SECTIONS:
            continue
        sym = row_ticker(row)
        if not sym or sym in csv_syms:
            continue
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
        if len(cells) < 16:
            continue
        inv_text = re.sub(r"<[^>]+>", "", cells[6]).strip()
        if parse_money(inv_text) == 0:
            continue  # already clean
        new_row = clear_row(row)
        cleared.append(sym)
        new_html = new_html.replace(row, new_row, 1)

    # Step 2: recompute totals from surviving held rows
    held = collect_held_rows(new_html, csv_syms)
    inv_sum = sum(h[1] for h in held)
    cur_sum = sum(h[2] for h in held)

    # CSV invested as cross-check
    csv_inv = 0.0
    with open(CSV_PATH) as f:
        for r in csv.DictReader(f):
            csv_inv += float(r["quantity"]) * float(r["avg_buy_price"])

    # Step 3: update header strip + footer + timestamp
    today = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%d-%b-%Y")
    new_html = update_pf_strip(new_html, inv_sum, cur_sum, len(held), today)
    new_html = update_footer_total(new_html, inv_sum, cur_sum)

    print(f"Cleared {len(cleared)} stale held rows: {cleared}")
    print(f"Surviving held India rows: {len(held)}")
    print(f"HTML invested (sum of rows): {fmt_money(inv_sum)}")
    print(f"CSV invested (cross-check):  {fmt_money(csv_inv)}")
    print(f"HTML current (sum of rows):  {fmt_money(cur_sum)}")
    print(f"HTML P&L: {fmt_money(cur_sum - inv_sum)} ({(cur_sum-inv_sum)/inv_sum*100:+.2f}%)")
    print(f"Timestamp set to: {today}")

    if abs(inv_sum - csv_inv) > 100:
        print(f"\n⚠ Invested mismatch — HTML rows sum {fmt_money(inv_sum)} vs CSV {fmt_money(csv_inv)}")
        print("  Likely rounding in HTML cells. Use --write to lock in HTML row sum as the displayed total.")

    if args.write:
        HTML_PATH.write_text(new_html)
        print(f"\n✓ Wrote {HTML_PATH}")
    else:
        print(f"\n(dry-run; pass --write to apply)")


if __name__ == "__main__":
    main()
