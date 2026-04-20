#!/usr/bin/env python3
"""
render_all.py — Re-render all research Markdown files to HTML, then generate PDFs.

Run this after changing render_plan.py or any research files to rebuild everything.

Usage:
  python3 src/render_all.py           # render HTML + generate PDFs
  python3 src/render_all.py --no-pdf  # render HTML only (faster)
  python3 src/render_all.py NEWGEN    # render + PDF for a single stock
"""

import subprocess, sys
from pathlib import Path

BASE     = Path(__file__).parent.parent
RESEARCH = BASE / "research"
OUT_HTML = BASE / "output" / "html"
SRC      = BASE / "src" / "render_plan.py"
GEN_PDF  = BASE / "src" / "generate_pdfs.py"
DOCS     = BASE / "docs"

# Also render docs that have HTML output
DOCS_FILES = ["TODO.md", "DECISION_LOG.md", "VALUATION_FRAMEWORK.md",
              "MULTIBAGGER_ANALYSIS_APPROACH.md", "AUTORESEARCH_APPROACH.md"]

def render(md_path: Path, out_dir: Path):
    result = subprocess.run(
        [sys.executable, str(SRC), str(md_path), str(out_dir)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"  ✓  {md_path.name}")
    else:
        print(f"  ✗  {md_path.name} — {result.stderr[:100]}")

def main():
    args = sys.argv[1:]
    no_pdf = "--no-pdf" in args
    single = next((a for a in args if not a.startswith("--")), None)
    if single:
        single = single.upper()

    OUT_HTML.mkdir(parents=True, exist_ok=True)

    if single:
        # Single stock: find the md file and render it
        md_path = RESEARCH / f"{single}.md"
        if not md_path.exists():
            md_path = RESEARCH / "us" / f"{single}.md"
        if not md_path.exists():
            print(f"No research file found for: {single}")
            sys.exit(1)
        print(f"\nRendering {single} → {OUT_HTML}/\n")
        render(md_path, OUT_HTML)
        if not no_pdf:
            print(f"\nGenerating PDF for {single}...\n")
            subprocess.run([sys.executable, str(GEN_PDF), single])
        return

    md_files = sorted(RESEARCH.glob("*.md")) + sorted(RESEARCH.glob("us/*.md"))
    doc_files = [DOCS / f for f in DOCS_FILES if (DOCS / f).exists()]
    all_files = md_files + doc_files

    print(f"\nRe-rendering {len(all_files)} files → {OUT_HTML}/\n")
    for md in all_files:
        render(md, OUT_HTML)

    if not no_pdf:
        print(f"\nGenerating PDFs...\n")
        subprocess.run([sys.executable, str(GEN_PDF)])
    else:
        print(f"\nDone. {len(all_files)} files rendered. (PDFs skipped)")

if __name__ == "__main__":
    main()
