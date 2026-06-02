"""Local dry-runner for the morning news routine.

Reads scripts/morning_news_prompt.md and executes it via `claude -p` in this repo.
Sets MORNING_NEWS_DRY_RUN=1 so the prompt skips the GitHub-issue + Telegram steps.

Usage:
  python3 scripts/morning_news.py          # dry-run, prints brief, no notifications
  python3 scripts/morning_news.py --full   # full run, creates issue + Telegram post
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROMPT_FILE = REPO / "scripts" / "morning_news_prompt.md"
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "/opt/homebrew/bin/claude")


def main() -> int:
    full = "--full" in sys.argv
    env = os.environ.copy()
    if not full:
        env["MORNING_NEWS_DRY_RUN"] = "1"

    prompt = (
        f"Read the file {PROMPT_FILE.relative_to(REPO)} in this repo "
        "and execute the instructions exactly as written."
    )

    print(f"Running morning news ({'FULL' if full else 'DRY-RUN'})...")
    proc = subprocess.run(
        [CLAUDE_BIN, "-p", prompt, "--dangerously-skip-permissions"],
        cwd=str(REPO),
        env=env,
    )
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
