"""Telegram bridge: forward chat messages to Claude Code running in this repo.

Reads TELEGRAM_BOT_TOKEN and TELEGRAM_ALLOWED_CHAT_ID from .env in repo root.
Only messages from TELEGRAM_ALLOWED_CHAT_ID are processed; everything else is dropped.

Run: caffeinate -dims python3 scripts/telegram_bridge.py
"""

from __future__ import annotations

import asyncio
import logging
import os
import shlex
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ALLOWED_CHAT_ID = int(os.environ["TELEGRAM_ALLOWED_CHAT_ID"])
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "/opt/homebrew/bin/claude")
LOG_FILE = REPO_ROOT / "scripts" / "telegram_bridge.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("bridge")

TELEGRAM_MAX = 4000  # leave headroom under the 4096 hard limit
SESSION_STATE: dict[int, bool] = {}  # chat_id -> has_prior_session


def _split_for_telegram(text: str) -> list[str]:
    chunks: list[str] = []
    while text:
        if len(text) <= TELEGRAM_MAX:
            chunks.append(text)
            break
        cut = text.rfind("\n", 0, TELEGRAM_MAX)
        if cut == -1:
            cut = TELEGRAM_MAX
        chunks.append(text[:cut])
        text = text[cut:].lstrip("\n")
    return chunks


async def _run_claude(prompt: str, resume: bool) -> str:
    cmd = [CLAUDE_BIN, "-p", prompt, "--dangerously-skip-permissions"]
    if resume:
        cmd.insert(1, "--continue")
    log.info("spawning: %s", " ".join(shlex.quote(c) for c in cmd))

    try:
        proc = await asyncio.wait_for(
            asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(REPO_ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ),
            timeout=10,
        )
    except asyncio.TimeoutError:
        log.error("claude failed to spawn within 10s")
        return "[claude spawn timeout]"

    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=600)
    except asyncio.TimeoutError:
        proc.kill()
        log.error("claude run timed out after 600s")
        return "[claude run timeout after 10 min]"

    log.info("claude exited with code %s, stdout=%d bytes, stderr=%d bytes",
             proc.returncode, len(stdout), len(stderr))
    if proc.returncode != 0:
        err = stderr.decode("utf-8", errors="replace").strip()
        log.error("claude stderr: %s", err[:500])
        return f"[claude exited {proc.returncode}]\n{err or '(no stderr)'}"
    return stdout.decode("utf-8", errors="replace").strip() or "(empty response)"


def _authorized(update: Update) -> bool:
    return update.effective_chat is not None and update.effective_chat.id == ALLOWED_CHAT_ID


async def on_start(update: Update, _ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _authorized(update):
        return
    await update.message.reply_text(
        "Claude Code bridge online. Send any message to invoke `claude -p` in the repo.\n"
        "Commands: /new (start fresh session), /whoami (debug)."
    )


async def on_new(update: Update, _ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _authorized(update):
        return
    SESSION_STATE[update.effective_chat.id] = False
    await update.message.reply_text("Session reset. Next message starts fresh.")


async def on_whoami(update: Update, _ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    await update.message.reply_text(
        f"chat_id={chat.id if chat else '?'} allowed={ALLOWED_CHAT_ID} match={_authorized(update)}"
    )


async def on_message(update: Update, _ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not _authorized(update):
        log.warning("dropping message from chat_id=%s (not whitelisted)",
                    update.effective_chat.id if update.effective_chat else "?")
        return
    msg = update.message.text or ""
    if not msg.strip():
        return

    chat_id = update.effective_chat.id
    log.info("incoming message len=%d: %r", len(msg), msg[:100])
    await _ctx.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    await update.message.reply_text("thinking...")

    resume = SESSION_STATE.get(chat_id, False)
    try:
        output = await _run_claude(msg, resume=resume)
    except FileNotFoundError:
        await update.message.reply_text(
            f"claude binary not found at {CLAUDE_BIN}. Set CLAUDE_BIN in .env."
        )
        return
    except Exception as exc:  # noqa: BLE001
        log.exception("bridge error")
        await update.message.reply_text(f"bridge error: {exc!r}")
        return

    SESSION_STATE[chat_id] = True
    log.info("replying with %d chars", len(output))
    for chunk in _split_for_telegram(output):
        await update.message.reply_text(chunk)


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", on_start))
    app.add_handler(CommandHandler("new", on_new))
    app.add_handler(CommandHandler("whoami", on_whoami))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    log.info("Bridge starting. repo=%s allowed_chat=%s claude=%s",
             REPO_ROOT, ALLOWED_CHAT_ID, CLAUDE_BIN)
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
