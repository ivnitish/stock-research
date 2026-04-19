#!/usr/bin/env python3
"""
render_all.py — Re-render all research Markdown files to HTML.

Run this after changing render_plan.py to apply updates to all existing files.

Usage:
  python3 src/render_all.py
"""

import subprocess, sys
from pathlib import Path

BASE     = Path(__file__).parent.parent
RESEARCH = BASE / "research"
OUT_HTML = BASE / "output" / "html"
SRC      = BASE / "src" / "render_plan.py"
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
    OUT_HTML.mkdir(parents=True, exist_ok=True)

    md_files = sorted(RESEARCH.glob("*.md")) + sorted(RESEARCH.glob("us/*.md"))
    doc_files = [DOCS / f for f in DOCS_FILES if (DOCS / f).exists()]

    all_files = md_files + doc_files
    print(f"\nRe-rendering {len(all_files)} files → {OUT_HTML}/\n")

    for md in all_files:
        render(md, OUT_HTML)

    print(f"\nDone. {len(all_files)} files rendered.")

if __name__ == "__main__":
    main()
