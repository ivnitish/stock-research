#!/bin/zsh
# Daily portfolio news brief — runs Claude Code headlessly via launchd.
# Schedule: weekdays 08:42 IST. Mac must be awake (launchd runs missed jobs on wake).
#
# Permission note: bypassPermissions is required for unattended runs (WebSearch,
# file writes, gh issue, Telegram ping all need it). Scope of damage is limited
# to this repo; review the prompt below before changing it.

REPO="/Users/nitish/stocks automation"
LOG_DIR="$REPO/data/logs"
mkdir -p "$LOG_DIR"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

PROMPT='Run the morning-news skill in full-run mode (last-24h news per holding;
on Mondays cover the weekend too).

Then add a "Watchlist Entry Zones" section to docs/MORNING_BRIEF.md: read the
watchlist table in docs/HANDOVER.md, fetch current CMP for each watchlist stock
from Tickertape or the Google Finance card via web search (do NOT use Groww MCP
or Kite MCP — they are on-demand only and unreliable headless; never use
Screener.in or Yahoo Finance for CMP), and flag any stock trading inside its
entry zone.

Follow all repo rules in CLAUDE.md and .claude/rules/. Never fabricate prices —
if a CMP cannot be fetched, write "data unavailable".'

{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') daily news brief ====="
  cd "$REPO" && claude -p "$PROMPT" --permission-mode bypassPermissions
  echo "===== done: exit $? ====="
} >> "$LOG_DIR/daily_news.log" 2>&1
