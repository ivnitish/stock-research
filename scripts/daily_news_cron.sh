#!/bin/zsh
# Daily portfolio news brief — headless Claude via launchd, with retry-until-success.
# Schedule: weekdays 08:42, then retry slots 11:42 / 14:42 / 17:42 / 20:42 IST.
# Each run no-ops if today's brief already succeeded (stamp file), so the brief
# is delivered exactly once per day even if early runs die on the session limit.
#
# Permission note: bypassPermissions is required for unattended runs (WebSearch,
# file writes, gh issue, Telegram ping all need it). Scope of damage is limited
# to this repo; review the prompt below before changing it.

REPO="/Users/nitish/stocks automation"
LOG_DIR="$REPO/data/logs"
STAMP="$LOG_DIR/daily_news_last_success"
LOCK="$LOG_DIR/daily_news.lock"
mkdir -p "$LOG_DIR"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

# Load .env so TELEGRAM_BOT_TOKEN reaches the headless Claude run.
# (Missing before 2026-07-18 — the Telegram digest silently never sent.)
if [[ -f "$REPO/.env" ]]; then
  set -a; source "$REPO/.env"; set +a
fi

TODAY=$(date '+%Y-%m-%d')

# Already delivered today → nothing to do.
if [[ -f "$STAMP" && "$(cat "$STAMP")" == "$TODAY" ]]; then
  exit 0
fi

# Cloud routine may have already delivered today's brief (full-mode
# morning-news opens a GitHub issue "Morning News YYYY-MM-DD"). If the issue
# exists, stamp and stand down — local slots are only the fallback.
CLOUD_ISSUE=$(gh issue list --repo ivnitish/stock-research \
  --search "Morning News $TODAY in:title" --state all --json number --jq 'length' 2>/dev/null)
if [[ "$CLOUD_ISSUE" == <-> && "$CLOUD_ISSUE" -ge 1 ]]; then
  echo "$TODAY" > "$STAMP"
  echo "$(date '+%Y-%m-%d %H:%M:%S') cloud brief already delivered today (issue found) — standing down" >> "$LOG_DIR/daily_news.log"
  exit 0
fi

# Another instance still running (e.g. overlapping retry slot) → skip.
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') skipped: another run in progress" >> "$LOG_DIR/daily_news.log"
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

PROMPT='Run the morning-news skill in full-run mode (last-24h news per holding;
on Mondays cover the weekend too). The skill itself covers the Buy-at Alerts
section and the single Telegram theme digest — follow its steps exactly:
exactly ONE short Telegram message, never more.

Follow all repo rules in CLAUDE.md and .claude/rules/. Never fabricate prices —
if a CMP cannot be fetched, write "data unavailable".'

{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') daily news brief (attempt) ====="
  cd "$REPO" && claude -p "$PROMPT" --permission-mode bypassPermissions
  RC=$?
  echo "===== done: exit $RC ====="
  if [[ $RC -eq 0 ]]; then
    echo "$TODAY" > "$STAMP"
    echo "===== stamped success for $TODAY ====="
  fi
} >> "$LOG_DIR/daily_news.log" 2>&1
