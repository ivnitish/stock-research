#!/usr/bin/env python3
"""Local runner for the fintwitter-finds daily pipeline.

Usage:
  python3 scripts/fintwitter_finds.py              # dry-run (no Telegram)
  python3 scripts/fintwitter_finds.py --full       # Claude + Telegram + PDF
  python3 scripts/fintwitter_finds.py --refresh    # skip Claude, refresh metrics/PDF/Telegram
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RUN_SH = REPO / "scripts" / "run_fintwitter_daily.sh"


def main() -> int:
    full = "--full" in sys.argv
    refresh = "--refresh" in sys.argv
    env = os.environ.copy()

    if refresh:
        cmd = ["/bin/zsh", str(RUN_SH), "--skip-claude"]
    elif full:
        cmd = ["/bin/zsh", str(RUN_SH)]
    else:
        env["FINTWITTER_DRY_RUN"] = "1"
        cmd = ["/bin/zsh", str(RUN_SH)]

    label = "REFRESH" if refresh else ("FULL" if full else "DRY-RUN")
    print(f"Running fintwitter pipeline ({label})...")
    proc = subprocess.run(cmd, cwd=str(REPO), env=env)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())