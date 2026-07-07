#!/bin/zsh
# Full fintwitter daily pipeline: Claude scan → Screener fetch → Telegram + PDF
#
# Usage:
#   scripts/run_fintwitter_daily.sh              # full (Claude + Python)
#   scripts/run_fintwitter_daily.sh --skip-claude  # refresh metrics/PDF/Telegram only
#   FINTWITTER_DRY_RUN=1 scripts/run_fintwitter_daily.sh  # no Telegram

set -euo pipefail

REPO="/Users/nitish/stocks automation"
LOG_DIR="$REPO/data/logs"
PROMPT_FILE="$REPO/.claude/skills/fintwitter-finds/references/SCAN_PROMPT.md"
VENV="$REPO/venv/bin/python3"
TODAY=$(date '+%Y-%m-%d')

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
mkdir -p "$LOG_DIR" "$REPO/output/pdf"

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

log "building Telegram summary..."
"$VENV" scripts/build_telegram_summary.py >> "$LOG_DIR/fintwitter_finds.log" 2>&1

log "building PDF..."
"$VENV" scripts/build_fintwitter_finds_pdf.py >> "$LOG_DIR/fintwitter_finds.log" 2>&1

PDF="$REPO/output/pdf/FINTWITTER_FINDS_${TODAY}.pdf"
if [[ ! -f "$PDF" ]]; then
  # fallback: latest pdf in dir
  PDF=$(ls -t "$REPO/output/pdf"/FINTWITTER_FINDS_*.pdf 2>/dev/null | head -1)
fi

# --- Step 3: Telegram ---
if [[ "${FINTWITTER_DRY_RUN:-}" == "1" ]]; then
  log "dry-run — skipping Telegram"
  "$VENV" scripts/send_telegram_digest.py docs/FINTWITTER_FINDS.md --dry-run
  exit 0
fi

if [[ -z "${PDF:-}" || ! -f "$PDF" ]]; then
  log "ERROR: PDF not found"
  exit 1
fi

log "sending Telegram (text + PDF)..."
"$VENV" scripts/send_telegram_digest.py docs/FINTWITTER_FINDS.md --pdf "$PDF" \
  >> "$LOG_DIR/fintwitter_finds.log" 2>&1

log "pipeline complete"
exit 0