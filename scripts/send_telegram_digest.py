#!/usr/bin/env python3
"""Send the Telegram summary block from a markdown brief to the configured bot.

Expects a section headed "## Telegram summary" (case-insensitive) until the next
## heading or EOF. Uses TELEGRAM_BOT_TOKEN + TELEGRAM_ALLOWED_CHAT_ID from .env.

Usage:
  python3 scripts/send_telegram_digest.py docs/FINTWITTER_FINDS.md
  python3 scripts/send_telegram_digest.py docs/FINTWITTER_FINDS.md --dry-run
  python3 scripts/send_telegram_digest.py docs/FINTWITTER_FINDS.md --pdf output/pdf/FINTWITTER_FINDS_2026-07-07.pdf
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

REPO = Path(__file__).resolve().parent.parent
load_dotenv(REPO / ".env")

TELEGRAM_MAX = 4000


def extract_telegram_section(text: str) -> str:
    m = re.search(
        r"^##\s*Telegram summary\s*\n(.*?)(?=^##\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not m:
        raise ValueError("no '## Telegram summary' section found")
    body = m.group(1).strip()
    if not body:
        raise ValueError("Telegram summary section is empty")
    return body


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
        print("usage: send_telegram_digest.py <markdown-file> [--dry-run]", file=sys.stderr)
        return 1

    path = Path(sys.argv[1])
    if not path.is_absolute():
        path = REPO / path
    dry_run = "--dry-run" in sys.argv

    text = path.read_text(encoding="utf-8")
    msg = extract_telegram_section(text)

    if dry_run:
        print(msg)
        return 0

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_ALLOWED_CHAT_ID", "").strip()
    if not token or not chat_id:
        print("TELEGRAM_BOT_TOKEN or TELEGRAM_ALLOWED_CHAT_ID missing — skip send", file=sys.stderr)
        return 0

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    chunks = split_chunks(msg)
    for i, chunk in enumerate(chunks):
        resp = requests.post(
            url,
            json={"chat_id": int(chat_id), "text": chunk},
            timeout=30,
        )
        resp.raise_for_status()
        print(f"sent chunk {i + 1}/{len(chunks)}")

    pdf_arg = None
    args = sys.argv[2:]
    for i, a in enumerate(args):
        if a == "--pdf" and i + 1 < len(args):
            pdf_arg = args[i + 1]
            break
        if a.endswith(".pdf"):
            pdf_arg = a
            break
    if pdf_arg:
        pdf_path = Path(pdf_arg)
        if not pdf_path.is_absolute():
            pdf_path = REPO / pdf_path
        if pdf_path.exists():
            doc_url = f"https://api.telegram.org/bot{token}/sendDocument"
            with pdf_path.open("rb") as fh:
                resp = requests.post(
                    doc_url,
                    data={"chat_id": int(chat_id), "caption": "Full report with thesis + Screener metrics per pick."},
                    files={"document": (pdf_path.name, fh, "application/pdf")},
                    timeout=60,
                )
            resp.raise_for_status()
            print(f"sent pdf {pdf_path.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())