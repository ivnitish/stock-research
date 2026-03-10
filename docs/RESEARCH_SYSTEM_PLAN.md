# Fundamental Research System — Plan

*Created: March 2026 | Philosophy: Charles Munger — read a lot, analyze deeply, hold long*

## Goal
Build a personal fundamental research system to identify 5x–10x multi-baggers in 3–5 years.
Target: **25% IRR**. Primary market: India (NSE/BSE). Not for trading — for deep conviction investing.

---

## Current Portfolio Snapshot (10-Mar-2026)
- Invested: ₹10.2L | Current: ₹9.3L | P&L: -₹90K (-8.9%)
- Core bets: GROWW (35%), KAYNES TECH (12%), EPACK PREFAB (10%), KERNEX MICROSYS (10%)
- Many single-share tracking positions for future research

---

## System Architecture (3 Layers)

### Layer 1: Research Engine — per stock
For every stock owned or being researched:

**1a. Quality Scorecard**
Munger-style checklist rated 1–5 each:
- Business MOAT (pricing power, switching costs, network effects, cost advantage)
- Management quality (capital allocation history, promoter integrity, skin in game)
- Financial quality (ROCE > 20% consistently, debt-free or low, working capital discipline)
- Growth runway (TAM, penetration, industry tailwinds)
- Valuation comfort (buying at reasonable price for great business)

**1b. Valuation Model**
- DCF (3 scenarios: base/bull/bear) with explicit assumptions
- Multiples (P/E, EV/EBITDA vs peers and history)
- "What needs to be true for 5x?" — reverse-engineer the assumptions

**1c. Investment Thesis (1-pager per stock)**
- Why this is a multi-bagger: specific catalysts
- Key risks that could kill the thesis
- Exit triggers (not price — fundamental: ROCE declining, management issue, thesis broken)
- Review milestones (what to check each quarter)

**1d. Red Flag Checklist**
Automatic alerts for: promoter pledging rising, ROCE declining 2+ quarters, unusual related-party transactions, management turnover

---

### Layer 2: Investment Journal

**2a. Decision Log**
Every buy/add/trim/exit decision documented:
- Date, stock, action, price
- Reasoning at the time (not post-hoc)
- What could prove me wrong
- Review date

**2b. Historical Review**
- Import Groww order history → reconstruct decisions
- For each past buy: was the reasoning sound? What happened? What did I learn?
- Pattern recognition: what types of bets have worked vs failed

**2c. Weekly Review (every Sunday)**
- Portfolio status vs benchmarks (Nifty, Nifty Smallcap)
- Upcoming events: results dates, AGMs, policy announcements
- Thesis changes: anything materially changed this week?
- New idea pipeline: 1–2 stocks worth deeper research

---

### Layer 3: Idea Generation

**3a. Screener Pipeline**
Quality filters to find candidates:
- ROCE > 20% for 5+ years
- Revenue growth > 15% CAGR
- Debt/Equity < 0.5
- Promoter holding > 50%, not declining
- PE < 30 or PEG < 1.5

**3b. Annual Report Analyzer (Claude-powered)**
- Drop annual report PDF → extract key trends, management tone, risks, capex plans
- Track YoY changes in language and numbers

**3c. Concall Summarizer**
- Paste concall transcript → extract: guidance changes, margin outlook, key risks management flagged
- Compare vs previous quarter's concall

**3d. Research Synthesis (Twitter/Substack)**
- Paste threads or articles → Claude extracts signal vs noise
- Build a "reading list" of quality analysts to follow

---

## Tech Stack

| Tool | Purpose | Cost |
|---|---|---|
| Python + yfinance | Price + basic fundamentals | Free |
| Screener.in | Deep Indian fundamentals, custom screens | Free (upgrade later) |
| NSE filings | Annual reports, concall transcripts | Free |
| Claude (CLI) | Research synthesis, thesis writing, modeling | Already using |
| Markdown files | Per-stock thesis, decision log | Free |
| Excel (Groww exports) | Portfolio data source | Free |

---

## File Structure (proposed)

```
stocks automation/
├── research/                    # Per-stock investment thesis
│   ├── _TEMPLATE.md
│   ├── GROWW.md
│   ├── KAYNES.md
│   └── ...
├── journal/
│   ├── decisions.md             # All buy/sell decisions with reasoning
│   └── weekly/                  # Weekly review notes
│       └── 2026-W11.md
├── screener/
│   ├── quality_filters.py       # Screener pipeline
│   └── exports/                 # Screener.in CSV exports
├── models/
│   ├── dcf_template.py          # Reusable DCF model
│   └── quality_scorecard.py     # Scoring framework
├── data/
│   └── [Groww Excel files]
└── docs/
    └── RESEARCH_SYSTEM_PLAN.md  # This file
```

---

## Research Process (to be defined)
*User to elaborate on current process — will form the basis of the workflow.*

Questions to answer:
1. When you find a new stock idea, what's step 1?
2. What's your current go-to for financial data (Screener, annual report, both)?
3. How long do you spend before deciding to buy?
4. What has made you exit a stock in the past?

---

## Open Questions / To Research
- [ ] GitHub repos for Indian stock research (for inspiration)
- [ ] Whether Screener.in has a free API or export format
- [ ] Best free sources for concall transcripts (NSE website, Tijori, etc.)
- [ ] Twitter API alternatives for thread research
