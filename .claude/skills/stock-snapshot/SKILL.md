---
name: stock-snapshot
description: >
  Compose and send a per-stock Telegram "Investment Snapshot" from an existing
  research file. Triggers on: "snapshot SYMBOL", "send snapshot", after creating
  or materially updating any research/SYMBOL.md, or when material news breaks on
  a covered stock. Event-driven, not scheduled — fires only when something real
  happened (new research, research update, or hard news).
context: fork
---

# Stock Snapshot — per-stock Telegram update

## When this fires

1. **New research** — a research/SYMBOL.md was just created.
2. **Research update** — an existing note was materially updated (new quarter,
   verdict change, price-ladder change). Cosmetic edits do not fire.
3. **News update** — hard news broke on a covered stock (results, large order,
   regulatory action, management change, dilution). The snapshot leads with the
   news, then restates the current verdict from the research file.
4. **On demand** — user says "snapshot SYMBOL".

## Rules

- Every number comes from `research/SYMBOL.md` (or the just-verified news
  source). Never fabricate; never pull stale numbers that the update superseded.
- Plain text, no emoji, no markdown formatting (Telegram plain message).
- Under 3,500 chars — ONE message, never chunked.
- Send via: compose to stdout → `venv/bin/python3 scripts/send_session_takeaways.py --stdin`
  (loads TELEGRAM_BOT_TOKEN from .env; skip silently if missing).
- Link always points to the rendered page:
  `https://ivnitish.github.io/stock-research/SYMBOL.html`

## Format

Header line: `SYMBOL | <New Research | Research Update | News: one-line event> — DD Mon YYYY`

Then sections, each a short header followed by tight bullets (numbers embedded,
one fact per line). Pick 4-6 sections that fit the stock — typical set:

```
SYMBOL | Research Update — 18 Jul 2026

Verdict
- <action + size + trigger price from the recommendation block>
- <grade + classification, one line>

Why
- <2-3 lines: the physical earnings mechanism>

Financials
- <3-4 lines: the numbers that carry the thesis>

Growth Drivers        (or: Valuation / Capacity / Order Book — whatever the note leads with)
- ...

Risks
- <2-4 lines from Concerns, sharpest first>

Takeaway
- <2-3 sentences max, from the Summary Verdict — what to do and what breaks it>

Full note: https://ivnitish.github.io/stock-research/SYMBOL.html
```

Section choice follows the research note's actual emphasis — an IPO note gets
Valuation + Listing details; a capex story gets Capacity + Triggers; a
turnaround gets Margin trajectory. Do not force all sections on every stock.

## What this is NOT

- Not a replacement for the daily theme digest (morning-news Step 8b) — that
  remains the one scheduled daily message. Snapshots are event-driven extras.
- Not buy/sell advice broadcast — it is the user's own research, summarized for
  their own channel.
- Not a news scraper — the research file is the source of truth; news triggers
  only add a dated lead line on top of the existing verdict.
