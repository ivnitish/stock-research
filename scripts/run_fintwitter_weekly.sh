#!/bin/zsh
# Fintwitter WEEKLY pipeline: Claude scan → Screener fetch → GitHub issue → short Telegram ping
# (Converted from daily 2026-07-18, user directive: weekly cadence, report lives
#  on GitHub, Telegram gets ONE short message, no PDF.)
#
# Usage:
#   scripts/run_fintwitter_weekly.sh               # full (Claude + Python)
#   scripts/run_fintwitter_weekly.sh --skip-claude # refresh metrics/issue/ping only
#   FINTWITTER_DRY_RUN=1 scripts/run_fintwitter_weekly.sh  # no GitHub issue, no Telegram

set -euo pipefail

REPO="/Users/nitish/stocks automation"
LOG_DIR="$REPO/data/logs"
PROMPT_FILE="$REPO/.claude/skills/fintwitter-finds/references/SCAN_PROMPT.md"
VENV="$REPO/venv/bin/python3"
TODAY=$(date '+%Y-%m-%d')

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
mkdir -p "$LOG_DIR"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*" | tee -a "$LOG_DIR/fintwitter_finds.log"; }

SKIP_CLAUDE=0
for arg in "$@"; do
  [[ "$arg" == "--skip-claude" ]] && SKIP_CLAUDE=1
done

cd "$REPO"

# --- Step 1: Claude discovery ---
if [[ $SKIP_CLAUDE -eq 0 ]]; then
  if [[ ! -f "$PROMPT_FILE" ]]; then
    log "ERROR: missing $PROMPT_FILE"
    exit 1
  fi
  PROMPT=$(cat "$PROMPT_FILE")
  log "starting Claude scan..."
  if [[ "${FINTWITTER_DRY_RUN:-}" == "1" ]]; then
    export FINTWITTER_DRY_RUN=1
    PROMPT="FINTWITTER_DRY_RUN=1 — do NOT send Telegram.\n\n$PROMPT"
  fi
  claude -p "$PROMPT" --permission-mode bypassPermissions >> "$LOG_DIR/fintwitter_finds.log" 2>&1
  log "Claude scan done"
else
  log "skipping Claude (--skip-claude)"
fi

# --- Step 2: Python pipeline (always) ---
if [[ ! -f "$REPO/data/fintwitter_finds_metrics.json" ]]; then
  log "ERROR: missing fintwitter_finds_metrics.json"
  exit 1
fi

log "fetching Screener metrics..."
"$VENV" scripts/fetch_fintwitter_screener.py >> "$LOG_DIR/fintwitter_finds.log" 2>&1

log "building report summary..."
"$VENV" scripts/build_telegram_summary.py >> "$LOG_DIR/fintwitter_finds.log" 2>&1

if [[ "${FINTWITTER_DRY_RUN:-}" == "1" ]]; then
  log "dry-run — skipping GitHub issue and Telegram"
  "$VENV" scripts/build_fintwitter_weekly_ping.py
  exit 0
fi

# --- Step 3: GitHub issue (primary delivery — full report, emails the user) ---
log "creating GitHub issue..."
ISSUE_URL=$(gh issue create --repo ivnitish/stock-research \
  --title "Fintwitter Weekly $TODAY" \
  --body-file docs/FINTWITTER_FINDS.md 2>>"$LOG_DIR/fintwitter_finds.log" || true)
if [[ -z "$ISSUE_URL" ]]; then
  log "WARNING: GitHub issue creation failed — ping will go without a link"
fi

# --- Step 4: short Telegram ping (ONE message, no PDF) ---
log "sending Telegram weekly ping..."
"$VENV" scripts/build_fintwitter_weekly_ping.py "$ISSUE_URL" \
  | "$VENV" scripts/send_session_takeaways.py --stdin \
  >> "$LOG_DIR/fintwitter_finds.log" 2>&1

log "weekly pipeline complete"
exit 0
