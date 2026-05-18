#!/usr/bin/env python3
"""
Rebuild the "INDIAN HOLDINGS" block of output/html/index.html so it contains
EXACTLY the 23 rows in data/portfolio.csv, sorted by current value desc.

Anything currently sitting inside the held block (between the INDIAN HOLDINGS
banner and the US section banner) whose ticker is NOT in portfolio.csv gets
evicted to the "watch india" section as a research-only row.

Anything that IS in portfolio.csv but currently lives outside the held block
gets relocated into the held block.

Idempotent. Pass --write to apply.
"""
import argparse
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "output" / "html" / "index.html"
CSV_PATH = ROOT / "data" / "portfolio.csv"
BACKUP = Path("/tmp/index.html.pretrim")

INDIAN_HOLDINGS_BANNER_RE = re.compile(
    r"<tr class=\"section-row\"[^>]*>\s*<td[^>]*>INDIAN HOLDINGS.*?</td>\s*</tr>",
    re.DOTALL,
)
US_BANNER_RE = re.compile(r'<tr class="section-row" data-section="us"')
WATCH_BANNER_RE = re.compile(
    r'<tr class="section-row" data-section="watch"[^>]*>\s*<td[^>]*>↓ RESEARCH WATCHLIST',
    re.DOTALL,
)
ROW_RE = re.compile(r"<tr class=\"stock-row\"[^>]*>.*?</tr>", re.DOTALL)


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


def ticker_of(row: str) -> str:
    m = re.search(r'<div class="td-ticker">([^<]+)<', row)
    return m.group(1).strip() if m else ""


def load_csv_syms() -> set[str]:
    out = set()
    with open(CSV_PATH) as f:
        for r in csv.DictReader(f):
            sym = r["symbol"].replace(".NS", "").replace(".BO", "")
            out.add(sym)
    return out


def load_pretrim_currents() -> dict[str, float]:
    if not BACKUP.exists():
        return {}
    pre = BACKUP.read_text()
    out: dict[str, float] = {}
    for m in re.finditer(r'<tr class="stock-row"[^>]*>.*?</tr>', pre, re.DOTALL):
        row = m.group(0)
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
        if len(cells) < 16:
            continue
        sym = ticker_of(row)
        if sym:
            out[sym] = parse_money(strip_tags(cells[7]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    html = HTML_PATH.read_text()
    csv_syms = load_csv_syms()
    currents = load_pretrim_currents()

    pf_match = INDIAN_HOLDINGS_BANNER_RE.search(html)
    if not pf_match:
        print("INDIAN HOLDINGS banner not found.")
        return
    us_match = US_BANNER_RE.search(html, pos=pf_match.end())
    watch_match = WATCH_BANNER_RE.search(html)

    held_block_start = pf_match.end()
    held_block_end = us_match.start()
    held_block = html[held_block_start:held_block_end]

    # All stock-rows in the current held block
    in_block_rows = ROW_RE.findall(held_block)
    in_block_syms = {ticker_of(r) for r in in_block_rows}

    # All stock-rows anywhere in the file
    all_rows = ROW_RE.findall(html)
    all_by_sym = {}
    for r in all_rows:
        s = ticker_of(r)
        if s and s not in all_by_sym:
            all_by_sym[s] = r

    # Compute movements
    evict_syms = sorted(s for s in in_block_syms if s not in csv_syms)
    pull_in_syms = sorted(s for s in csv_syms if s not in in_block_syms and s in all_by_sym)
    keep_syms = sorted(s for s in csv_syms if s in in_block_syms)
    missing_syms = sorted(s for s in csv_syms if s not in all_by_sym)

    print(f"CSV holdings: {len(csv_syms)}")
    print(f"Currently in held block: {len(in_block_syms)}")
    print(f"Keep (CSV ∩ block): {len(keep_syms)}")
    print(f"Pull in to block (CSV but outside): {pull_in_syms}")
    print(f"Evict from block (not in CSV): {evict_syms}")
    if missing_syms:
        print(f"⚠ CSV symbols with no row anywhere in HTML: {missing_syms}")

    # Build the new held block: all CSV rows sorted by current value desc
    final_syms = list(csv_syms & set(all_by_sym.keys()))
    final_syms.sort(key=lambda s: (-currents.get(s, 0.0), s))

    # Normalize each row's data-section to held-india (grade-X india or tracking india).
    # We keep whatever data-section it already has if it's a held one; otherwise set
    # data-section to "grade-b india" as a sensible default for held research.
    # Also remove any "Exited" or "Watch" action tags — these are held.
    def normalize_row(row: str, sym: str) -> str:
        sec_m = re.search(r'data-section="([^"]+)"', row)
        cur_section = sec_m.group(1) if sec_m else ""
        if cur_section not in {"grade-a india", "grade-b india", "grade-c india", "tracking india"}:
            # was 'watch india' or similar — restore a held section
            # Default to "tracking india" for tiny positions (no thesis yet)
            cur = currents.get(sym, 0.0)
            new_sec = "tracking india" if cur < 5000 else "grade-b india"
            row = re.sub(r'data-section="[^"]+"', f'data-section="{new_sec}"', row, count=1)
        return row

    held_rows_html = []
    for sym in final_syms:
        held_rows_html.append(normalize_row(all_by_sym[sym], sym))

    new_held_block_inner = "\n        " + "\n        ".join(held_rows_html) + "\n"

    # Build the evict block (rows we're moving to watch india section)
    evict_rows_html = []
    for sym in evict_syms:
        row = all_by_sym[sym]
        # Tag as watch india
        row = re.sub(r'data-section="[^"]+"', 'data-section="watch india"', row, count=1)
        row = re.sub(r'data-grade="[a-c]"', 'data-grade="w"', row, count=1)
        evict_rows_html.append(row)

    # Compose new HTML:
    # 1. Strip out every row that is going into either the held block or the evict pile.
    # 2. Replace held block with new sorted block.
    # 3. Insert evict pile right after the WATCHLIST banner.
    relocate_syms = set(final_syms) | set(evict_syms)
    new_html = html

    # Remove each relocate row from its current position
    for sym in relocate_syms:
        row = all_by_sym[sym]
        # row appears exactly once; replace with empty
        new_html = new_html.replace(row, "", 1)

    # Now re-locate the banners in the (modified) new_html
    pf_match2 = INDIAN_HOLDINGS_BANNER_RE.search(new_html)
    us_match2 = US_BANNER_RE.search(new_html, pos=pf_match2.end())
    held_start = pf_match2.end()
    held_end = us_match2.start()

    # Replace held block (which now contains only banner-free whitespace + any leftover non-relocate rows)
    # We'll keep any non-CSV non-evict rows that were in held block (there shouldn't be any but safe).
    leftover = new_html[held_start:held_end]
    leftover_rows = ROW_RE.findall(leftover)
    leftover_kept = [r for r in leftover_rows if ticker_of(r) not in relocate_syms]
    if leftover_kept:
        print(f"Warning: {len(leftover_kept)} unexpected rows left in held block: {[ticker_of(r) for r in leftover_kept]}")
        new_held_block_inner += "\n        " + "\n        ".join(leftover_kept) + "\n"

    new_html = new_html[:held_start] + new_held_block_inner + new_html[held_end:]

    # Now insert evict rows after the WATCHLIST banner
    watch_match2 = WATCH_BANNER_RE.search(new_html)
    if watch_match2 and evict_rows_html:
        insertion_point = watch_match2.end()
        # Find end of the banner tr (close </tr>)
        close_re = re.compile(r"</tr>")
        cm = close_re.search(new_html, pos=insertion_point)
        if cm:
            insertion_point = cm.end()
        evict_html = "\n        " + "\n        ".join(evict_rows_html)
        new_html = new_html[:insertion_point] + evict_html + new_html[insertion_point:]

    if not args.write:
        print(f"\nDry-run. Final held block would have {len(final_syms)} rows.")
        print(f"Evict pile (now in watchlist): {len(evict_rows_html)} rows.")
        return

    HTML_PATH.write_text(new_html)
    print(f"\n✓ Wrote {HTML_PATH}")
    print(f"  Held block: {len(final_syms)} rows in current-value desc order")
    print(f"  Evicted to watchlist: {len(evict_rows_html)} rows ({evict_syms})")


if __name__ == "__main__":
    main()
