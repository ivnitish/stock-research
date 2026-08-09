#!/bin/zsh
# Weekly re-score of logged recommendation calls against the latest bhavcopy.
# Pure Python (no Claude) — reads data/call_tracker.csv, rewrites the
# auto-scorecard block in docs/CALL_POSTMORTEM.md. Scheduled via launchd.
set -e
REPO="/Users/nitish/01_github_repo/stocks_automation"
LOG_DIR="$REPO/data/logs"
mkdir -p "$LOG_DIR"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
cd "$REPO"
"$REPO/venv/bin/python3" scripts/update_call_tracker.py \
  >> "$LOG_DIR/call_tracker.log" 2>&1
echo "$(date '+%Y-%m-%d %H:%M') done" >> "$LOG_DIR/call_tracker.log"
