#!/bin/zsh
# One-off queue for tonight (2026-07-06, after 22:10 limit reset), run sequentially
# so git pushes never race: (1) today's news brief, (2) BANCOINDIA v2 research,
# (3) index dashboard mockups. Runs headless via launchd — no Claude session needed,
# Mac just has to be awake. Safe to re-run: news step no-ops once stamped.

REPO="/Users/nitish/stocks automation"
LOG="$REPO/data/logs/oneoff_tonight.log"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

{
  echo "########## $(date '+%Y-%m-%d %H:%M:%S') oneoff queue start ##########"

  echo "----- 1/3 news brief -----"
  "$REPO/scripts/daily_news_cron.sh"
  tail -2 "$REPO/data/logs/daily_news.log"

  echo "----- 2/3 BANCOINDIA v2 research -----"
  cd "$REPO" && claude -p "$(cat scripts/prompts/banco_v2.txt)" --permission-mode bypassPermissions
  echo "banco exit: $?"

  echo "----- 3/3 dashboard mockups -----"
  cd "$REPO" && claude -p "$(cat scripts/prompts/dashboard_v2.txt)" --permission-mode bypassPermissions
  echo "dashboard exit: $?"

  echo "########## done $(date '+%H:%M:%S') ##########"
} >> "$LOG" 2>&1
