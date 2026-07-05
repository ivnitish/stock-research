#!/bin/zsh
# Nightly BSE filings fetch — runs via system cron, zero Claude tokens.
# Fetches filings for all portfolio companies into data/filings/{SYMBOL}/.
# Cron: weekdays 21:12 IST (after evening filing window).

REPO="/Users/nitish/stocks automation"
LOG_DIR="$REPO/data/logs"
mkdir -p "$LOG_DIR"

{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') nightly filings fetch ====="
  cd "$REPO" && venv/bin/python3 src/fetch_bse_filings.py ALL
  echo "===== done: exit $? ====="
} >> "$LOG_DIR/nightly_filings.log" 2>&1

# Keep the log from growing unbounded (last ~2000 lines)
tail -n 2000 "$LOG_DIR/nightly_filings.log" > "$LOG_DIR/nightly_filings.log.tmp" \
  && mv "$LOG_DIR/nightly_filings.log.tmp" "$LOG_DIR/nightly_filings.log"
