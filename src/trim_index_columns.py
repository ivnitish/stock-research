#!/usr/bin/env python3
"""
Trim output/html/index.html from 16 columns to 7.

Keeps: Ticker, Grade, Action, CMP, P&L%, Target·Mult (combined), Arrow.
Drops: Qty, Avg, Δ/share, Invested, Current, P&L₹, CMP/Ref, Buy-Zone.

Idempotent — if every row already has ≤8 td cells, exits without writing.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "output" / "html" / "index.html"

# 0-indexed positions in the original 16-cell layout
TICKER, GRADE, QTY, AVG, CMP, DELTA, INV, CUR, PNL_INR, PNL_PCT, ACTION, TARGET, REF, BUYZONE, UPSIDE, ARROW = range(16)

# Order in the new 7-cell layout
NEW_ORDER = [TICKER, GRADE, ACTION, CMP, PNL_PCT, "TARGET_COMBINED", ARROW]


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def split_td(row: str):
    """Return list of full <td>...</td> matches preserving inner markup."""
    return re.findall(r"<td[^>]*>.*?</td>", row, re.DOTALL)


def combine_target_upside(target_cell: str, upside_cell: str) -> str:
    """Combine '₹620' (target) + '~2.0x' (upside) into one cell: '₹620 · 2.0x'.
    If either is em-dash, show only the non-dash one. If both, show '—'."""
    t = strip_tags(target_cell)
    u = strip_tags(upside_cell)
    t_has = t and t != "—"
    u_has = u and u != "—"
    if t_has and u_has:
        # Preserve target's color styling
        style_match = re.search(r'style="([^"]+)"', target_cell)
        style = style_match.group(1) if style_match else "color:#166534;font-weight:600"
        return f'<td class="col-hide-sm num-cell" style="{style}">{t} · {u}</td>'
    if t_has:
        style_match = re.search(r'style="([^"]+)"', target_cell)
        style = style_match.group(1) if style_match else "color:#166534;font-weight:600"
        return f'<td class="col-hide-sm num-cell" style="{style}">{t}</td>'
    if u_has:
        return f'<td class="col-hide-sm num-cell num-dim">{u}</td>'
    return '<td class="col-hide-sm num-cell num-dim">—</td>'


def trim_row(row: str) -> str | None:
    tds = split_td(row)
    if len(tds) == 7:
        return None  # already trimmed
    if len(tds) != 16:
        return None  # unexpected shape — skip

    new_tds = []
    for slot in NEW_ORDER:
        if slot == "TARGET_COMBINED":
            new_tds.append(combine_target_upside(tds[TARGET], tds[UPSIDE]))
        else:
            new_tds.append(tds[slot])

    # Rebuild row: preserve the opening <tr ...> and closing </tr>, replace inner cells.
    open_m = re.match(r"\s*(<tr[^>]*>)", row)
    if not open_m:
        return None
    opener = open_m.group(1)
    indent = "          "
    body = "\n".join(indent + td for td in new_tds)
    return f"{opener}\n{body}\n        </tr>"


def trim_thead(html: str) -> str:
    """Replace the main table's thead (15 th + implicit arrow) with the new 6 th."""
    new_thead = """      <thead>
        <tr>
          <th style="min-width:130px">Ticker</th>
          <th class="col-hide-sm">Grade</th>
          <th class="col-hide-sm">Action</th>
          <th class="col-hide-sm num">CMP ₹</th>
          <th class="num">P&amp;L %</th>
          <th class="col-hide-sm num">Target · Mult</th>
          <th></th>
        </tr>
      </thead>"""
    # The first <thead>...</thead> in the file is the one we want.
    return re.sub(
        r"      <thead>.*?</thead>",
        new_thead,
        html,
        count=1,
        flags=re.DOTALL,
    )


def trim_footer(html: str) -> str:
    """The TOTAL PORTFOLIO row had ~16 cells too. Collapse it to 7-cell layout
    with the totals positioned under their new columns. We move the existing
    Invested+Current+P&L+P&L% display into the new wider middle/last cells."""
    # Locate the tfoot block
    m = re.search(r"      <tfoot>.*?</tfoot>", html, flags=re.DOTALL)
    if not m:
        return html
    tfoot = m.group(0)

    # Extract the three big numeric tokens (invested, current, P&L abs, pct)
    inv_m = re.search(r'text-align:right;[^>]*line-height:1\.5;">(₹[\d.,KLCr]+)\s*India', tfoot)
    cur_m = re.search(r'font-weight:700; color:white;[^>]*line-height:1\.5;">(₹[\d.,KLCr]+)\s*India', tfoot)
    pnl_m = re.search(r'font-weight:700; color:#f87171;[^>]*line-height:1\.5;">([+-]?₹[\d.,KLCr]+)\s*India', tfoot) or \
            re.search(r'font-weight:700; color:#22c55e;[^>]*line-height:1\.5;">([+-]?₹[\d.,KLCr]+)\s*India', tfoot)
    pct_m = re.search(r"font-weight:700; color:#[a-f0-9]+;[^>]*line-height:1\.5;\">([+-]?[\d.]+%)", tfoot)

    inv = inv_m.group(1) if inv_m else "—"
    cur = cur_m.group(1) if cur_m else "—"
    pnl = pnl_m.group(1) if pnl_m else "—"
    pct = pct_m.group(1) if pct_m else "—"

    pnl_color = "#f87171" if pnl.startswith("-") else "#22c55e"

    new_tfoot = f"""      <tfoot>
        <tr style="background:#1a1a2e; color:white; border-top:2px solid #e0e4f0;">
          <td style="padding:11px 12px; font-size:0.82rem; font-weight:700;">TOTAL PORTFOLIO</td>
          <td class="col-hide-sm" style="color:#9090b0;font-size:0.75rem">India</td>
          <td class="col-hide-sm" style="text-align:right;font-size:0.75rem;color:#9090b0;line-height:1.4">Invested<br><b style="color:white;font-size:0.9rem">{inv}</b></td>
          <td class="col-hide-sm" style="text-align:right;font-size:0.75rem;color:#9090b0;line-height:1.4">Current<br><b style="color:white;font-size:0.9rem">{cur}</b></td>
          <td style="text-align:right;font-size:0.82rem;font-weight:700;color:{pnl_color};line-height:1.4">{pct}<br><span style="font-size:0.7rem;font-weight:400">{pnl}</span></td>
          <td class="col-hide-sm" style="font-size:0.7rem;color:#9090b0;text-align:right">India live<br>18:35 IST</td>
          <td></td>
        </tr>
      </tfoot>"""

    return html.replace(tfoot, new_tfoot, 1)


def main():
    html = HTML_PATH.read_text()

    rows_changed = 0
    rows_skipped = 0
    rows_already_trimmed = 0

    pattern = re.compile(r'<tr class="stock-row"[^>]*>.*?</tr>', re.DOTALL)
    new_html = html
    for m in pattern.finditer(html):
        row = m.group(0)
        tds = split_td(row)
        if len(tds) == 7:
            rows_already_trimmed += 1
            continue
        if len(tds) != 16:
            rows_skipped += 1
            continue
        new_row = trim_row(row)
        if new_row and new_row != row:
            new_html = new_html.replace(row, new_row, 1)
            rows_changed += 1

    if rows_changed == 0 and rows_already_trimmed > 0:
        print(f"Already trimmed ({rows_already_trimmed} rows have 7 cells). Nothing to do.")
        return

    new_html = trim_thead(new_html)
    new_html = trim_footer(new_html)

    # Update colspan on the "US Portfolio — Live" banner row (was colspan=16, now 7)
    new_html = re.sub(r'<td colspan="16">', '<td colspan="7">', new_html)

    HTML_PATH.write_text(new_html)

    print(f"Rows trimmed:           {rows_changed}")
    print(f"Rows already trimmed:   {rows_already_trimmed}")
    print(f"Rows skipped (shape):   {rows_skipped}")
    print(f"thead updated, footer updated, colspans normalized.")
    print(f"Wrote {HTML_PATH}")

    # Verify
    final = HTML_PATH.read_text()
    weird = []
    for m in re.finditer(r'<tr class="stock-row"[^>]*>.*?</tr>', final, re.DOTALL):
        n_cells = len(split_td(m.group(0)))
        if n_cells != 7:
            tk_match = re.search(r'<div class="td-ticker">([^<]+)<', m.group(0))
            weird.append((tk_match.group(1) if tk_match else "?", n_cells))
    if weird:
        print(f"\n⚠ {len(weird)} rows still don't have 7 cells:")
        for tk, n in weird[:10]:
            print(f"  {tk}: {n} cells")
    else:
        print("\n✓ Every stock-row now has exactly 7 cells.")


if __name__ == "__main__":
    main()
