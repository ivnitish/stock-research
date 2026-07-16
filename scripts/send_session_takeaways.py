#!/usr/bin/env python3
"""Send a free-form session takeaways message to the configured Telegram bot.

Usage:
  ./venv/bin/python3 scripts/send_session_takeaways.py "message text"
  ./venv/bin/python3 scripts/send_session_takeaways.py --file /path/to/msg.txt
  echo "msg" | ./venv/bin/python3 scripts/send_session_takeaways.py --stdin

Reads TELEGRAM_BOT_TOKEN + TELEGRAM_ALLOWED_CHAT_ID from repo .env.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

REPO = Path(__file__).resolve().parent.parent
load_dotenv(REPO / ".env")
TELEGRAM_MAX = 4000


def split_chunks(text: str, limit: int = TELEGRAM_MAX) -> list[str]:
    chunks: list[str] = []
    while text:
        if len(text) <= limit:
            chunks.append(text)
            break
        cut = text.rfind("\n", 0, limit)
        if cut <= 0:
            cut = limit
        chunks.append(text[:cut].rstrip())
        text = text[cut:].lstrip("\n")
    return chunks


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "usage: send_session_takeaways.py <text> | --file PATH | --stdin",
            file=sys.stderr,
        )
        return 1

    if sys.argv[1] == "--stdin":
        text = sys.stdin.read().strip()
    elif sys.argv[1] == "--file":
        text = Path(sys.argv[2]).read_text(encoding="utf-8").strip()
    else:
        text = " ".join(sys.argv[1:]).strip()

    if not text:
        print("empty message", file=sys.stderr)
        return 1

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_ALLOWED_CHAT_ID", "").strip()
    if not token or not chat_id:
        print("TELEGRAM_BOT_TOKEN or TELEGRAM_ALLOWED_CHAT_ID missing", file=sys.stderr)
        return 1

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    for chunk in split_chunks(text):
        r = requests.post(
            url,
            json={
                "chat_id": int(chat_id),
                "text": chunk,
                "disable_web_page_preview": True,
            },
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        if not data.get("ok"):
            print(data, file=sys.stderr)
            return 1
        print("sent message_id=", data["result"]["message_id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
