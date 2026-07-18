#!/bin/zsh
# Weekly fintwitter finds — launchd entry point (Saturdays; converted from daily 2026-07-18).
# Runs full pipeline once per Saturday; retries evening slot if morning failed.

REPO="/Users/nitish/stocks automation"
LOG_DIR="$REPO/data/logs"
STAMP="$LOG_DIR/fintwitter_finds_last_success"
LOCK="$LOG_DIR/fintwitter_finds.lock"
mkdir -p "$LOG_DIR"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

TODAY=$(date '+%Y-%m-%d')

if [[ -f "$STAMP" && "$(cat "$STAMP")" == "$TODAY" ]]; then
  exit 0
fi

if ! mkdir "$LOCK" 2>/dev/null; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') skipped: another run in progress" >> "$LOG_DIR/fintwitter_finds.log"
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') fintwitter weekly cron ====="
  "$REPO/scripts/run_fintwitter_weekly.sh"
  RC=$?
  if [[ $RC -eq 0 ]]; then
    echo "$TODAY" > "$STAMP"
    echo "===== stamped success for $TODAY ====="
  else
    echo "===== pipeline failed: exit $RC ====="
  fi
} >> "$LOG_DIR/fintwitter_finds.log" 2>&1

exit ${RC:-0}
