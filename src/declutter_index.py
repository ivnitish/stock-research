#!/usr/bin/env python3
"""
One-shot declutter pass for output/html/index.html.

Three changes in a single transform:
  1. Remove 15 meta-doc rows now living in library.html (linked separately in nav).
  2. Remove 14 watchlist rows that have neither research nor a holding (no-thesis cruft).
  3. Wire 5 invisible-link rows (DREDGECORP existing research + 4 newly-created monitor stubs).

Idempotent — safe to re-run. Reports counts for each operation. Does NOT touch any
other file. Column-trim (16 -> 7) is handled by a separate script.
"""
import re
import sys
from pathlib import Path

PATH = Path("output/html/index.html")

# 1. Meta-doc rows: identified by their onclick target. Already moved to library.html.
META_TARGETS = {
    "IRAN_WAR_V2.html",
    "MARKET_NOTE_MAR2026.html",
    "NIFTY20K_WATCHLIST.html",
    "WATCHLIST_SCREEN_MAR2026.html",
    "CONCENTRATION_STRATEGY.html",
    "PORTFOLIO_OVERVIEW.html",
    "VALUATION_FRAMEWORK.html",
    "SECTOR_NUCLEAR_INDIA.html",
    "LOSERS_ANALYSIS.html",
    "GROWW_vs_ICICIAMC.html",
    "DECISION_LOG.html",
    "NIFTY_VALUATION.html",
    "MACRO_NOTES.html",
    "2026-W11.html",
    "Kamayaka_Research_Value_Investing_summary.html",
}

# 2. No-thesis tickers: identified by their td-ticker text. No research + not a holding.
NO_THESIS_TICKERS = {
    "KPITTECH", "BRIGADE", "FABTECH", "NIPPOBATRY", "TTKHLTCARE",
    "SAGILITY", "URBANCO", "POLICYBZR", "IZMO", "NDTV",
    "CGCL", "VSTIND", "NETWEB", "SATIN",
}

# 3. Wire onclick handlers: ticker text -> target HTML.
WIRE_ONCLICK = {
    "DREDGECORP": "DREDGECORP.html",
    "ATHERENERG": "ATHERENERG.html",
    "BHEL": "BHEL.html",
    "ZENTEC": "ZENTEC.html",
    "SOUTHWEST": "SOUTHWEST.html",
}


def split_into_rows(html: str):
    """Yield (kind, text) tuples — kind is 'row' for tr.stock-row, 'other' for everything else."""
    pattern = re.compile(
        r'(\s*<tr class="stock-row"[^>]*>.*?</tr>\s*)',
        re.DOTALL,
    )
    last = 0
    for m in pattern.finditer(html):
        if m.start() > last:
            yield ("other", html[last:m.start()])
        yield ("row", m.group(0))
        last = m.end()
    if last < len(html):
        yield ("other", html[last:])


def row_onclick_target(row_html: str):
    m = re.search(r"onclick=\"go\('([^']+)'\)\"", row_html)
    return m.group(1) if m else None


def row_ticker(row_html: str):
    m = re.search(r'<div class="td-ticker">([^<]+)<', row_html)
    return m.group(1).strip() if m else None


def main():
    html = PATH.read_text()
    n_meta_removed = 0
    n_no_thesis_removed = 0
    n_wired = 0

    out_parts = []
    for kind, text in split_into_rows(html):
        if kind == "other":
            out_parts.append(text)
            continue

        target = row_onclick_target(text)
        ticker = row_ticker(text)

        # Skip moved meta-docs.
        if target in META_TARGETS:
            n_meta_removed += 1
            continue

        # Skip no-thesis cruft.
        if ticker in NO_THESIS_TICKERS:
            n_no_thesis_removed += 1
            continue

        # Wire missing onclick handlers.
        if ticker in WIRE_ONCLICK and target is None:
            new_target = WIRE_ONCLICK[ticker]
            # Insert onclick after data-grade attribute. Match the existing pattern.
            new_text = re.sub(
                r'(<tr class="stock-row" data-section="[^"]+" data-grade="[^"]+")(>)',
                rf'\1 onclick="go(\'{new_target}\')"\2',
                text,
                count=1,
            )
            if new_text != text:
                n_wired += 1
                text = new_text

        out_parts.append(text)

    new_html = "".join(out_parts)
    PATH.write_text(new_html)

    print(f"Meta-doc rows removed (now in library.html):      {n_meta_removed}/15")
    print(f"No-thesis cruft rows removed:                     {n_no_thesis_removed}/14")
    print(f"Invisible-link rows wired with onclick handler:   {n_wired}/5")
    print()
    print(f"index.html: {len(html):,} -> {len(new_html):,} bytes")
    print(f"            line delta: {html.count(chr(10))} -> {new_html.count(chr(10))}")

    # Sanity: any stock-rows still without onclick?
    leftover = []
    for kind, text in split_into_rows(new_html):
        if kind != "row":
            continue
        if "onclick=" not in text:
            tk = row_ticker(text)
            leftover.append(tk)
    if leftover:
        print()
        print(f"Remaining stock-rows without onclick ({len(leftover)}):")
        for tk in leftover:
            print(f"  - {tk}")


if __name__ == "__main__":
    main()
