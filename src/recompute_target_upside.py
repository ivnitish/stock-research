#!/usr/bin/env python3
"""
Rewrite the combined Target·Mult cell in every stock-row of index.html to a
consistent "₹Target · +X%" format computed from CMP and target.

The original "Upside" column was inconsistent: some values were return
multiples (1.2x meaning +20% over horizon), some were multi-bagger potentials
(4.6x over many years), and Raymond's was outright wrong (0.31x with target
above CMP). Standardising to simple "% upside from CMP to Target" fixes all of
them and makes the column genuinely comparable across rows.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "output" / "html" / "index.html"

ROW_RE = re.compile(r"<tr class=\"stock-row\"[^>]*>.*?</tr>", re.DOTALL)
TD_RE = re.compile(r"<td[^>]*>.*?</td>", re.DOTALL)


def parse_price(s: str) -> float | None:
    """Parse '₹530' / '$1,210' / '₹5,500-6,200' (use mid) / '—'."""
    if not s or "—" in s:
        return None
    s = re.sub(r"[<>]", "", s)
    range_match = re.match(r"[₹$]([\d,]+)\s*-\s*[₹$]?([\d,]+)", s)
    if range_match:
        a = float(range_match.group(1).replace(",", ""))
        b = float(range_match.group(2).replace(",", ""))
        return (a + b) / 2
    m = re.search(r"[₹$]([\d,]+(?:\.\d+)?)", s)
    if not m:
        return None
    return float(m.group(1).replace(",", ""))


def main():
    html = HTML_PATH.read_text()
    fixed = 0
    skipped = 0
    rows_examined = 0
    sample = []

    new_html = html
    for m in ROW_RE.finditer(html):
        row = m.group(0)
        rows_examined += 1
        tds = TD_RE.findall(row)
        if len(tds) != 7:
            skipped += 1
            continue

        ticker_match = re.search(r'<div class="td-ticker">([^<]+)<', tds[0])
        ticker = ticker_match.group(1).strip() if ticker_match else "?"
        cmp_text = re.sub(r"<[^>]+>", "", tds[3]).strip()
        cell6 = tds[5]
        cell6_inner = re.sub(r"<[^>]+>", "", cell6).strip()

        # Parse target out of the existing combined cell.
        # Format is either "₹530 · 0.31x" / "₹530" / "—"
        target_part = cell6_inner.split("·")[0].strip()
        target_v = parse_price(target_part)
        cmp_v = parse_price(cmp_text)

        if target_v is None or cmp_v is None or cmp_v == 0:
            # Keep cell as-is — no valid pair to compute
            continue

        upside_pct = (target_v / cmp_v - 1.0) * 100
        # Format
        is_usd = "$" in cmp_text or "$" in target_part
        cur = "$" if is_usd else "₹"
        # Use the original target's display format
        target_display = target_part if target_part.startswith(cur) else f"{cur}{target_v:,.0f}"
        sign = "+" if upside_pct >= 0 else ""
        new_inner = f"{target_display} · {sign}{upside_pct:.0f}%"

        # Color: green for >+10%, neutral for -10 to +10, red for <-10%
        if upside_pct >= 10:
            color = "color:#166534;font-weight:600"
        elif upside_pct >= -5:
            color = "color:#666"
        else:
            color = "color:#991b1b;font-weight:600"

        new_cell = f'<td class="col-hide-sm num-cell" style="{color}">{new_inner}</td>'

        if new_cell != cell6:
            new_row = row.replace(cell6, new_cell, 1)
            new_html = new_html.replace(row, new_row, 1)
            fixed += 1
            if len(sample) < 8:
                sample.append((ticker, cmp_text, target_part, cell6_inner, new_inner))

    HTML_PATH.write_text(new_html)
    print(f"Rows examined: {rows_examined}")
    print(f"Rows updated:  {fixed}")
    print(f"Rows skipped (no valid CMP+Target pair, or wrong shape): {rows_examined - fixed}")
    print()
    print("Sample changes:")
    for tk, cmp_, tgt, old, new in sample:
        print(f"  {tk:<14} CMP={cmp_:<10} | old={old!r:<30} | new={new!r}")


if __name__ == "__main__":
    main()
