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

# Rebuild the research index + portfolio page from research/*.md and
# portfolio.csv with fresh bhavcopy closes. Zero Claude tokens; runs every slot
# so the site never goes stale and new notes appear without hand-editing.
# Non-fatal on failure.
"$REPO/venv/bin/python3" "$REPO/scripts/build_site_index.py" \
  >> "$LOG_DIR/daily_news.log" 2>&1 || true
"$REPO/venv/bin/python3" "$REPO/scripts/build_portfolio_page.py" \
  >> "$LOG_DIR/daily_news.log" 2>&1 || true

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

# Pre-collect deterministic inputs (headlines, buy-at alerts, macro-thread
# context) so the Claude run only analyzes — zero-token data gathering.
INPUTS_FILE="$REPO/data/daily_inputs/$TODAY.md"
"$REPO/venv/bin/python3" "$REPO/scripts/collect_daily_inputs.py" \
  >> "$LOG_DIR/daily_news.log" 2>&1 || true

PROMPT="Run the morning-news skill in full-run mode (last-24h news per holding;
on Mondays cover the weekend too). The skill itself covers the Buy-at Alerts
section, the single Telegram theme digest (with macro-thread continuity), and
event-driven per-stock snapshots — follow its steps exactly: ONE theme digest,
plus at most 2 stock-snapshot messages and only when a covered holding has hard
news (results, large order, regulatory action, dilution). Quiet day = digest only.

Pre-collected inputs: read $INPUTS_FILE FIRST if it exists — it has per-holding
headlines, macro headlines, precomputed buy-at alerts, and macro-thread context.
Work from it instead of broad web searches; use at most 3 targeted
WebFetch/WebSearch calls for items that are material but unclear from headlines
(the file flags its own gaps). If the file is missing, fall back to the skill's
normal search steps.

Follow all repo rules in CLAUDE.md and .claude/rules/. Never fabricate prices —
if a CMP cannot be fetched, write \"data unavailable\"."

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
