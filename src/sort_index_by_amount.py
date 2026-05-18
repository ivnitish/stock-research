#!/usr/bin/env python3
"""
Sort held India stock rows in output/html/index.html by current value descending.

Replaces the multi-banner Grade A / B+ / B / C / Tracking structure with a
single sorted block under one banner.

Idempotent — if the held block is already sorted (no Grade-N sub-banners
present), exits without writing.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "output" / "html" / "index.html"

# Sections that contain held India positions
HELD_INDIA = {"grade-a india", "grade-b india", "grade-c india", "tracking india"}


def parse_money(s: str) -> float:
    s = s.replace(",", "")
    m = re.search(r"([\d.]+)", s)
    if not m:
        return 0.0
    v = float(m.group(1))
    if "Cr" in s:
        v *= 1_00_00_000
    elif "L" in s:
        v *= 1_00_000
    elif "K" in s:
        v *= 1_000
    return v


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def row_current_from_pnl(row: str) -> float:
    """After column trim, the P&L % is column 5. Sort key: we'd prefer absolute
    current value, but the new 7-col layout doesn't expose it. We re-read the
    backup at /tmp/index.html.pretrim if present to get pre-trim current values.
    Otherwise fall back to ticker order."""
    return 0.0


def load_pretrim_currents() -> dict[str, float]:
    """Look up each ticker's current value from the pre-trim backup if available."""
    backup = Path("/tmp/index.html.pretrim")
    out: dict[str, float] = {}
    if not backup.exists():
        # Try git HEAD as second fallback
        return out
    pre = backup.read_text()
    pat = re.compile(r'<tr class="stock-row"[^>]*>(.*?)</tr>', re.DOTALL)
    for m in pat.finditer(pre):
        row = m.group(0)
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
        if len(cells) < 16:
            continue
        tk = re.search(r'<div class="td-ticker">([^<]+)<', cells[0])
        if not tk:
            continue
        sym = tk.group(1).strip()
        cur_text = strip_tags(cells[7])
        out[sym] = parse_money(cur_text)
    return out


def main():
    html = HTML_PATH.read_text()
    currents = load_pretrim_currents()
    if not currents:
        print("⚠ No pre-trim backup available. Sorting by ticker alphabetically.")

    # Find the held block boundaries: from the "PORTFOLIO HOLDINGS" banner
    # to just before the "us" section banner.
    pf_banner_re = re.compile(
        r"(<tr class=\"section-row\"[^>]*>\s*<td[^>]*>↓ PORTFOLIO HOLDINGS.*?</td>\s*</tr>)",
        re.DOTALL,
    )
    us_banner_re = re.compile(
        r'<tr class="section-row" data-section="us"',
    )

    pf_match = pf_banner_re.search(html)
    if not pf_match:
        print("Could not find PORTFOLIO HOLDINGS banner.")
        sys.exit(1)
    us_match = us_banner_re.search(html, pos=pf_match.end())
    if not us_match:
        print("Could not find US section banner.")
        sys.exit(1)

    held_block = html[pf_match.end():us_match.start()]

    # Extract all stock-rows in the held block
    row_re = re.compile(r"\s*<tr class=\"stock-row\"[^>]*>.*?</tr>", re.DOTALL)
    rows = row_re.findall(held_block)
    if not rows:
        print("No stock-rows in held block.")
        sys.exit(0)

    # Idempotency: if there are no Grade- sub-banners left, we've already sorted.
    if 'Grade A —' not in held_block and 'Grade B ·' not in held_block and 'Grade C —' not in held_block:
        print("Held block has no Grade sub-banners — already sorted. Skipping.")
        return

    print(f"Found {len(rows)} held-block stock-rows.")

    # Sort by current value desc; tie-break by ticker
    def key(row):
        tm = re.search(r'<div class="td-ticker">([^<]+)<', row)
        sym = tm.group(1).strip() if tm else "ZZZ"
        cur = currents.get(sym, 0.0)
        return (-cur, sym)

    rows_sorted = sorted(rows, key=key)

    # Build new held block
    new_banner = (
        '\n        <tr class="section-row" style="background:linear-gradient(90deg,#dcfce7,#bbf7d0);'
        'color:#14532d;border-top:2px solid #22c55e;border-bottom:2px solid #22c55e">\n'
        '          <td colspan="7" style="font-weight:700;letter-spacing:0.5px;text-align:center;padding:12px">'
        'INDIAN HOLDINGS — sorted by current value (largest first)'
        '</td>\n        </tr>'
    )

    new_held_block = new_banner + "".join(rows_sorted) + "\n"

    new_html = html[:pf_match.start()] + new_held_block + html[us_match.start():]

    HTML_PATH.write_text(new_html)
    print(f"Wrote {HTML_PATH}")
    print(f"Sort order (top 5): {[re.search(chr(60)+'div class=\"td-ticker\">([^<]+)<', r).group(1).strip() for r in rows_sorted[:5]]}")


if __name__ == "__main__":
    main()
