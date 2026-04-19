#!/usr/bin/env python3
"""
generate_pdfs.py — Generate PDFs from all research HTML files.

Portfolio data (Entry price, P&L, Decision History) is hidden in PDFs
via @media print CSS. Safe to share with others.

Usage:
  python3 src/generate_pdfs.py              # generate all PDFs
  python3 src/generate_pdfs.py NEWGEN       # generate single stock PDF

Output:
  output/pdf/NEWGEN_2026-04-19.pdf
  (old PDFs for the same stock are deleted before generating new one)

Requirements:
  Google Chrome installed at default Mac location.
  Run render_all.py first if research files have changed since last render.
"""

import sys, subprocess, os, glob
from pathlib import Path
from datetime import datetime

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HTML_DIR = Path(__file__).parent.parent / "output" / "html"
PDF_DIR  = Path(__file__).parent.parent / "output" / "pdf"

# Files to skip (not individual research reports)
SKIP = {
    "index.html", "auth.html", "_TEMPLATE.html",
    "CONCENTRATION_STRATEGY.html", "GROWW_vs_ICICIAMC.html",
    "KCP_raw_data.html", "LOSERS_ANALYSIS.html",
    "MACRO_NOTES.html", "MARKET_NOTE_MAR2026.html",
    "MULTIBAGGER_ANALYSIS_APPROACH.html",
    "AUTORESEARCH_APPROACH.html", "VALUATION_FRAMEWORK.html",
}

def generate_pdf(html_path: Path, pdf_dir: Path, date_str: str) -> bool:
    symbol = html_path.stem  # e.g. "NEWGEN"
    pdf_name = f"{symbol}_{date_str}.pdf"
    pdf_path = pdf_dir / pdf_name

    # Remove old PDFs for this symbol
    for old in pdf_dir.glob(f"{symbol}_*.pdf"):
        old.unlink()

    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        f"file://{html_path.absolute()}",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    if pdf_path.exists() and pdf_path.stat().st_size > 1000:
        size_kb = pdf_path.stat().st_size // 1024
        print(f"  ✓  {pdf_name}  ({size_kb} KB)")
        return True
    else:
        print(f"  ✗  {symbol} — failed. stderr: {result.stderr[:120]}")
        return False


def main():
    if not Path(CHROME).exists():
        print(f"Chrome not found at: {CHROME}")
        print("Update CHROME path in this script.")
        sys.exit(1)

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Determine which files to process
    single = sys.argv[1].upper() if len(sys.argv) > 1 else None

    html_files = sorted(HTML_DIR.glob("*.html"))
    if single:
        html_files = [f for f in html_files if f.stem.upper() == single]
        if not html_files:
            print(f"No HTML found for: {single}")
            sys.exit(1)
    else:
        html_files = [f for f in html_files if f.name not in SKIP]

    print(f"\nGenerating {len(html_files)} PDF(s) → {PDF_DIR}/\n")

    ok = fail = 0
    for f in html_files:
        if generate_pdf(f, PDF_DIR, date_str):
            ok += 1
        else:
            fail += 1

    print(f"\nDone: {ok} generated, {fail} failed.")
    print(f"PDFs saved to: {PDF_DIR}/")


if __name__ == "__main__":
    main()
