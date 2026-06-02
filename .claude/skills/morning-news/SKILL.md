---
name: morning-news
description: >
  Generate the daily morning news brief for portfolio holdings.
  Triggers on: "morning news", "morning brief", "run morning news",
  "today's brief", "news on my holdings", "what's happening in my portfolio today".
  Reads data/portfolio.csv, ranks by cost basis, scans last-24h news for each
  holding, plus India + US macro headlines. Writes to docs/MORNING_BRIEF.md.
  In full-run mode, also opens a GitHub issue and pings Telegram.
context: fork
---

# Morning News — Daily Holdings Brief

This skill is invoked by:
- The cloud `/schedule` daily routine (full mode)
- The local dry-runner `scripts/morning_news.py`
- The Telegram bridge when the user asks (defaults to dry-run unless the user says "for real" / "full run")
- Any direct invocation in a Claude Code session

## Behaviour switch

If the environment variable `MORNING_NEWS_DRY_RUN=1` is set, run in **dry-run mode**: produce the brief and stop. Do NOT create a GitHub issue or POST to Telegram.

Otherwise, run in **full mode**: produce the brief, create the GitHub issue, send the Telegram notification.

## Steps

1. **Read `data/portfolio.csv`** — local file only. Never call Groww, Kite, or any broker API in this skill.

2. **Rank by cost basis** — compute `quantity × avg_buy_price` for each row, sort descending. No live price lookups required.

3. **For each holding**, web-search the last 24 hours for **material** news. Material means:
   - Quarterly / annual results
   - Regulatory action, orders, approvals, penalties
   - Management changes, board changes
   - Large orders, contracts, capex announcements
   - Rating actions, analyst downgrades / upgrades from major houses
   - Promoter activity, insider trades, pledge changes
   - Acquisitions, divestitures, fundraises

   **Skip:** price moves, generic market commentary, social-media chatter, broker pump-and-dump, anything without a hard event.

4. **Macro scan** — top 5 India and top 3 US macro headlines from the last 24 hours. Skip noise; keep only items that could move the user's holdings or change positioning.

5. **Write `docs/MORNING_BRIEF.md`** (overwrite each run). Use this structure:

   ```
   # Morning Brief — YYYY-MM-DD

   ## Holdings news
   (only stocks with material news, in cost-basis order — skip silent ones)

   ### SYMBOL
   - headline 1 — source
   - headline 2 — source

   ## Macro
   ### India
   - ...
   ### US
   - ...
   ```

   If no holding has material news AND macro is quiet, write the whole body as: `Markets quiet — no material news today.` Don't pad.

6. **If dry-run**, print the brief to stdout and exit here.

7. **If full mode:**
   a. Open a GitHub issue in the current repo titled `Morning News YYYY-MM-DD` with the brief as the body. GitHub emails the user automatically (no SMTP setup needed). This is the primary notification — must succeed.
   b. **Telegram ping is optional.** If the `TELEGRAM_BOT_TOKEN` env var is set, POST a message to chat ID **1679797853** with body `Morning News ready: <issue URL>`. If the env var is missing or empty, skip silently — do not fail the routine. The local bridge already handles ad-hoc Telegram interaction; the cloud routine doesn't depend on Telegram.

## Notes

- Use UTC date for `YYYY-MM-DD` in the filename and issue title.
- Group multiple sources reporting the same event into a single line.
- The skill is read-only on `portfolio.csv`. Never rewrite it.
- Cost basis ranking is intentional — no price lookups, fully offline-friendly for the ranking step.
