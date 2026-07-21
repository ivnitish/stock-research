#!/usr/bin/env python3
"""Post the day's macro-thread digest to Telegram — deterministically.

Why this exists: the morning-news skill composes a Telegram digest, but the
headless `claude -p --permission-mode bypassPermissions` run the cron uses does
NOT expose TELEGRAM_BOT_TOKEN to the skill's send step, so it skips silently
(logs "TELEGRAM_BOT_TOKEN isn't set in this environment"). This script runs
AFTER the brief in the cron, reads the top (newest) dated block the skill
prepended to docs/MACRO_THREAD.md, and POSTs it. It loads the token from .env
via python-dotenv, which works regardless of the headless run's environment.

Delivery is decoupled from the agent on purpose: the agent's job is to write
today's MACRO_THREAD.md entry; this script's job is to deliver it. In this
environment the skill's own inline send is a no-op, so there is no double-send.

Usage:
  venv/bin/python3 scripts/send_macro_digest.py            # send top block
  venv/bin/python3 scripts/send_macro_digest.py --dry-run  # print, don't send
  venv/bin/python3 scripts/send_macro_digest.py --require-today  # skip if the
        top block isn't dated today (guards against sending a stale entry when
        the skill failed to prepend a new one)
"""

from __future__ import annotations

import os
import re
import sys
from datetime import date
from pathlib import Path

import requests
from dotenv import load_dotenv

REPO = Path(__file__).resolve().parent.parent
load_dotenv(REPO / ".env")
THREAD = REPO / "docs" / "MACRO_THREAD.md"


def top_block() -> str:
    """The newest '## <date> ...' section, up to the next '## ' or EOF."""
    text = THREAD.read_text(encoding="utf-8")
    for block in re.split(r"\n(?=## )", text):
        if block.lstrip().startswith("## "):
            return block.strip()
    return ""


def parse_date(block: str) -> str:
    m = re.search(r"##\s*(\d{4}-\d{2}-\d{2})", block)
    return m.group(1) if m else ""


def format_msg(block: str) -> str:
    lines = block.splitlines()
    header = lines[0].lstrip("# ").strip()          # "2026-07-20 (Monday)"
    body = [re.sub(r"^\s*[-*]\s+", "• ", ln) for ln in lines[1:] if ln.strip()]
    return f"Macro threads — {header}\n\n" + "\n".join(body)


def main() -> int:
    block = top_block()
    if not block:
        print("no macro-thread entry found", file=sys.stderr)
        return 1

    if "--require-today" in sys.argv and parse_date(block) != date.today().isoformat():
        print(f"top block dated {parse_date(block)!r} != today — skip", file=sys.stderr)
        return 0

    msg = format_msg(block)
    if "--dry-run" in sys.argv:
        print(msg)
        return 0

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat = os.environ.get("TELEGRAM_ALLOWED_CHAT_ID", "").strip()
    if not token or not chat:
        print("TELEGRAM_BOT_TOKEN / TELEGRAM_ALLOWED_CHAT_ID missing — skip", file=sys.stderr)
        return 0

    resp = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": int(chat), "text": msg},
        timeout=30,
    )
    resp.raise_for_status()
    print("sent macro digest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
