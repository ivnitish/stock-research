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

   **Continuity (added 2026-07-18):** before writing themes, read the last 2-3 dated entries in `docs/MACRO_THREAD.md`. Today's themes must connect to that running narrative — say whether a thread is continuing, strengthening, reversing, or new ("crude's third down day — rupee pressure easing", not a context-free headline). After the brief is written, prepend today's dated entry (3-5 theme lines) to `docs/MACRO_THREAD.md`, newest first. This file is the persistent macro narrative the Telegram digest is a window into.

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

6. **Buy-at alerts** — read the buy-at table from `docs/HANDOVER.md`, fetch each CMP from Tickertape via WebFetch (never Screener/Yahoo for CMP; no broker MCPs). Add a `## Buy-at Alerts` section to the brief listing each stock, CMP, trigger level, and whether it is INSIDE or outside its zone. (Formalized 2026-07-18 — this was previously an ad-hoc post-run step.)

7. **If dry-run**, print the brief to stdout and exit here.

8. **If full mode:**
   a. Open a GitHub issue in the current repo titled `Morning News YYYY-MM-DD` with the brief as the body. GitHub emails the user automatically (no SMTP setup needed). This is the primary notification — must succeed.
   b. **Telegram daily message — threads, taught (format decided 2026-07-18, depth rule relaxed same day).** If the `TELEGRAM_BOT_TOKEN` env var is set, POST ONE plain-text message to chat ID **1679797853**. Teach every macro thread that *genuinely matters* to the portfolio that day — 1 on quiet days, 2-3 on busy days — each with the full Feynman treatment: every causal link spelled out in plain language, no jargon without explanation, ending in what it means for the user's holdings. **Depth is non-negotiable, count is flexible:** never compress a thread into a headline to fit more in — if it earns a slot it gets the full chain; if not, it goes in the side notes.

      **The so-what filter (user feedback 2026-07-18):** a thread earns full treatment ONLY if its conclusion changes something for the user — how to read his holdings, a price level to act on, a risk that got bigger or smaller. If the honest ending is "net-net nothing changes for us," it was never a thread — one side-note line, done. Titles state the mechanism plainly ("Oil & the rupee"), never editorial hooks ("the story just flipped" — banned style, see .claude/rules/writing-quality.md). Budget: up to ~3,800 chars, but always ONE message — never chunk. Format:

      ```
      <Thread 1 title> — YYYY-MM-DD

      <3-5 short paragraphs teaching the thread:
       the fact → the mechanism, step by step, in
       plain words → the portfolio consequence.
       A reader with zero context must be able to
       follow every link in the chain.>

      <Thread 2 title>                (only if the day earns it)

      <same treatment>

      Also today: <1-2 one-line side notes on remaining threads>

      Alerts: <SYMBOL ₹CMP INSIDE zone (<trigger)> | "none in zone"
      Full brief: <issue URL>
      ```

      Thread selection uses `docs/MACRO_THREAD.md` continuity (Step 4): a continuing thread teaches the *next layer* or *what changed* — never re-explain yesterday's mechanism verbatim; a new thread gets taught from scratch. Reference example (user-approved 2026-07-18): oil past $80 → India imports ~85% of crude → more dollars needed → rupee falls → imports pricier → feeds CPI already above 4% → RBI can't cut → higher rates compress smallcap P/Es → "that's our real exposure — not oil stocks, the multiple on everything we hold." No metrics blocks, no PDFs, no multi-part digests. If the env var is missing or empty, skip silently — do not fail the routine.

   c. **Per-stock news snapshots (event-driven, added 2026-07-18).** If any *covered* holding (has a `research/SYMBOL.md`) had genuinely hard news today — quarterly results, large order/contract, regulatory action, management change, dilution/fundraise — run the `stock-snapshot` skill for it: a structured Investment Snapshot (verdict, financials, drivers, risks, takeaway) sent as its own Telegram message, news event as the lead line. **Max 2 snapshots per day**, hardest news first; everything else stays a line in the theme digest. Days without hard news send the theme digest alone — the "one daily message" baseline still holds; snapshots fire only on real events.

## Notes

- Use UTC date for `YYYY-MM-DD` in the filename and issue title.
- Group multiple sources reporting the same event into a single line.
- The skill is read-only on `portfolio.csv`. Never rewrite it.
- Cost basis ranking is intentional — no price lookups, fully offline-friendly for the ranking step.
