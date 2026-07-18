#!/usr/bin/env python3
"""Compose the SHORT weekly fintwitter Telegram ping (stdout).

The rich per-pick report lives in the GitHub issue; Telegram gets one small
message (user directive 2026-07-18: no PDFs, no multi-chunk digests).

Usage:
    build_fintwitter_weekly_ping.py [ISSUE_URL]

Reads data/fintwitter_finds_metrics.json (active picks + verdicts) and the
"New mentions" section of docs/FINTWITTER_FINDS.md (symbols added this run).
Pipe the output to send_session_takeaways.py --stdin.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JSON_PATH = REPO / "data" / "fintwitter_finds_metrics.json"
MD_PATH = REPO / "docs" / "FINTWITTER_FINDS.md"
MAX_LEN = 900  # single lock-screen-readable message


def new_symbols_from_md() -> list[str]:
    """Symbols under the '## New mentions' heading of the current report."""
    try:
        text = MD_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    m = re.search(r"^## New mentions.*?$(.*?)(?=^## |\Z)", text,
                  re.MULTILINE | re.DOTALL)
    if not m:
        return []
    # Picks appear as "### Company Name (NSE SYMBOL)" / "(BSE 515008)" headings;
    # fall back to ALL-CAPS tokens at line starts for older formats.
    body = m.group(1)
    syms = re.findall(r"^### .*?\((?:NSE|BSE)\s+([A-Z0-9&\-]{2,15})\)",
                      body, re.MULTILINE)
    if not syms:
        syms = re.findall(r"^(?:### )?\*{0,2}([A-Z][A-Z0-9&\-]{2,15})\*{0,2}\s*[—:-]",
                          body, re.MULTILINE)
    seen: list[str] = []
    for s in syms:
        if s not in seen:
            seen.append(s)
    return seen


def main() -> int:
    issue_url = sys.argv[1] if len(sys.argv) > 1 else ""

    try:
        picks = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except Exception:
        picks = {}

    tier1 = [v.get("symbol") or k for k, v in picks.items()
             if "TIER 1" in (v.get("verdict") or "").upper()]
    new = new_symbols_from_md()

    lines = [f"Fintwitter Weekly — {date.today():%d %b %Y}",
             f"{len(picks)} active picks"
             + (f", new: {', '.join(new[:5])}" if new else ", no new adds")]
    if tier1:
        lines.append("Tier-1: " + ", ".join(tier1[:8]))
    if issue_url:
        lines.append(f"Full report: {issue_url}")

    msg = "\n".join(lines)
    if len(msg) > MAX_LEN:
        msg = msg[:MAX_LEN].rsplit("\n", 1)[0]
    print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
