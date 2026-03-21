# Research System — Data & Analysis Approach

*Last updated: 2026-03-21 | Philosophy: Charles Munger — read a lot, analyze deeply, hold long*

---

## Overview

A personal fundamental research system for identifying 5x–10x multi-baggers in 3–5 years.
**Target: 25% IRR.** Primary market: India (NSE/BSE) + selective US positions.

Everything is on-demand — we research when a stock needs a decision, not on a schedule.

---

## Part 1 — Data Sources & How We Get Them

### 1.1 Financial Data (Quantitative)

| Source | What We Get | How |
|--------|-------------|-----|
| **Screener.in** | P&L, Balance Sheet, Cash Flows (10yr), Quarterly trends, Peers, Key ratios | Claude → WebFetch → screener.in/company/SYMBOL (automatic in session) |
| **BSE API** | Quarterly results PDFs, annual reports, concall transcripts, investor presentations | Claude runs `python3 src/fetch_bse_filings.py SYMBOL [--days 365]` |
| **Groww MCP** | Live CMP, fundamentals summary, historical candles | Claude tool: `mcp__growwmcp__fetch_stocks_fundamental_data` |
| **Kite MCP** | Portfolio holdings, avg buy price, P&L, positions | Claude tool: `mcp__kite__get_holdings` |

**BSE fetcher details:**
- Saves to: `data/filings/{SYMBOL}/{YYYYMMDD}_{CATEGORY}_{HEADLINE}.pdf`
- Relevant categories: Quarterly Results, Annual Report, Earnings Call Transcript, Investor Presentation, Analyst Meet
- Run: `python3 scripts/fetch_bse_filings.py KERNEX` → downloads last 365 days
- Run: `python3 scripts/fetch_bse_filings.py ALL` → all 20 portfolio stocks
- 404s on old files are expected (BSE CDN only hosts recent PDFs)

### 1.2 Qualitative Data

| Source | What We Get | How |
|--------|-------------|-----|
| **Earnings call transcripts** | Management tone, specific guidance, claims to verify | From BSE fetcher or `data/filings/` |
| **YouTube transcripts** | Analyst views, concall replays, deep dives | Saved to `data/transcripts/` — pasted as MD |
| **Annual report** | Business overview, risk factors, related-party transactions, capex plans | From BSE fetcher PDF |
| **Investor presentations** | Management's own version of numbers, order book, capacity | From BSE fetcher PDF |
| **Web search** | Competitor data, industry TAM, sector news | Claude WebSearch / WebFetch |

### 1.3 Peer / Competitive Data

- Screener.in peers tab → copy competitor ratios
- BSE filings for competitor concalls
- Industry reports via web search

### 1.4 Portfolio & Market Data

| Need | Tool |
|------|------|
| My holdings, avg price, P&L | `mcp__kite__get_holdings` |
| Live prices | `mcp__kite__get_ltp` or `mcp__growwmcp__get_ltp` |
| Market overview / movers | `mcp__growwmcp__fetch_market_movers_and_trending_stocks_funds` |

---

## Part 2 — Research Workflow (Per Stock)

### Step 1: Data Gathering (all done by Claude, no manual steps)

1. Claude runs BSE fetcher → downloads concalls, results, presentations to `data/filings/SYMBOL/`
2. Claude → WebFetch → screener.in/company/SYMBOL → extracts 4-year P&L, balance sheet, quarterly data
3. Claude reads the downloaded concall transcript PDF
4. Claude → WebFetch → screener.in peers tab → extracts competitor multiples

### Step 2: Kill Filter (5 min — stop here if any fails)

Answer these 6 questions with data from Screener:

| # | Question | Hard Stop |
|---|----------|-----------|
| 1 | Is ROCE > 15% (or on clear trajectory to >15%)? | Fail = reject |
| 2 | Is promoter holding stable / not pledged heavily (>20% pledge = red flag)? | Fail = reject |
| 3 | Is Operating Cash Flow positive in 3 of last 4 years? | Fail = reject |
| 4 | Is debt manageable (D/E < 1x, or interest coverage > 3x)? | Fail = reject |
| 5 | No serious related-party transaction issues? | Fail = reject |
| 6 | Is revenue/earnings growing (not declining trend)? | Fail = reject |

### Step 3: Compounding Engine Q&A (30-45 min — the core analysis)

Answer these questions with specific numbers (not opinions):

**Q1: Is ROIC structurally high or artificially high?**
- Show: ROIC = NOPAT / Invested Capital (break down numerator + denominator)
- Is it driven by real competitive advantages or one-time factors?

**Q2: Is there a long reinvestment runway?**
- TAM estimate + current penetration
- Capacity utilization vs expansion plans
- Order book / backlog as revenue coverage years

**Q3: Does the math work?**
- Sustainable growth = Reinvestment Rate × ROIC
- Owner Earnings = PAT + Depreciation – Maintenance Capex
- If ROIC 20%, reinvestment 60% → sustainable g = 12%. Does this match mgmt guidance?

**Q4: What are the kill conditions?**
- Specific data points that would break the thesis (not vague "competition")
- E.g.: "If aerospace revenue growth falls below 20% for 2 consecutive quarters, thesis is broken"

### Step 4: Management & Financial Quality (20 min)

- Cross-reference management claims vs actual numbers (make a table)
- Check: capital allocation history (acquisitions, capex discipline)
- Red flags: promoter selling, related-party transactions, auditor changes
- Working capital trends (receivables/inventory stretching = warning)

### Step 5: Competitive Landscape (20 min)

- Who are the 3-4 closest competitors? Get their P/E, EV/EBITDA, ROCE
- Is the company's competitive position widening or narrowing?
- Industry tailwind: growing, stable, or in structural decline?
- Customer/supplier concentration risk

### Step 6: Valuation (20 min)

**Three-scenario DCF:**

```
g = Reinvestment Rate × ROIC      (sustainable growth rate)
n = runway duration (from Step 3) (years of high-growth phase)
r = 12-15%                        (required return for Indian equities)

Year-n Earnings = Current Earnings × (1+g)^n
Terminal Value  = Year-n Earnings × Terminal PE
                  (15-20x if still growing; 10-12x if mature/commodity)
PV              = PV of interim CFs + Terminal Value / (1+r)^n
```

**Quick reverse DCF check:**
- At current price, what P/E does the market imply at Year-5?
- If current P/E = 30x and Terminal PE = 15x, market expects 0% earnings growth
- If justified by DCF terminal PE > current implied terminal PE → undervalued

**Margin of Safety:**
- Implied growth rate at current price (reverse DCF)
- Bear case: biggest risk materializes → what is value?
- Minimum required: bear case ≥ 30% above buy price

### Step 7: Summary Verdict

Fill the Summary Verdict table at the top of the research file:

| Dimension | Score | Quick Note |
|---|---|---|
| Kill Filter | PASS/FAIL | |
| MOAT | /5 | |
| Management | /5 | |
| Financials | /5 | |
| Growth Runway | /5 | |
| Valuation | /5 | |
| **Total** | **/25** | **Grade A/B/C/D** |

**Grade thresholds:**
- A (20-25): Strong buy
- B (15-19): Core holding / selective add
- C (10-14): Watch / hold only
- D (<10): Exit or pass

---

## Part 3 — Research Template

All research files live in `research/SYMBOL.md`. Template at `research/_TEMPLATE.md`.

**Template structure (new format as of 2026-03-21):**

```
# Summary Verdict (fill LAST, read FIRST)
# Bull Case (3 sentences)
# Bear Case (3 sentences)
# Key Monitorables
# Data Gaps
# Quick Summary + Action Table
---
Section 1: Business Structure
Section 2: Kill Filter
Section 3: Compounding Engine Q&A
Section 4: Financial History (4yr + TTM, 6 quarters)
Section 5: Management & Financials
Section 5.1: Valuation
Section 5.2: Margin of Safety
Section 5.3: Position Sizing (Phase 1-4 score)
Section 6: Competitive Landscape
```

**Status of research files:**
- New template format: _TEMPLATE.md (reference only)
- Old format (pre-2026-03-21): most existing research files (RAYMOND, KERNEX, KAYNES, etc.)
- TODO: Update existing files to new format when next reviewing that stock

---

## Part 4 — Output & Viewing

All research files are rendered to HTML and viewable at `output/html/`:

```bash
# Render a single file
python3 /tmp/render_plan.py research/SYMBOL.md
# → creates research/SYMBOL.html (or opens from output/html/SYMBOL.html)

# View index
open output/html/index.html
```

GitHub Pages: https://ivnitish.github.io/stock-research (auto-updated on push)

---

## Part 5 — Automation (What Runs on Its Own)

| Job | Schedule | Script | What it does |
|-----|----------|--------|-------------|
| Portfolio price update | Daily 7pm | `src/portfolio_price_update.py` | Fetches CMP via Alpha Vantage, updates index.html prices |
| Red flag monitor | Weekly Mon 8am | `src/red_flag_monitor.py` | Checks ROCE declining, promoter pledging, etc. |

**On-demand (run manually when researching):**
- BSE filings: `python3 scripts/fetch_bse_filings.py SYMBOL`
- Full portfolio BSE fetch: `python3 scripts/fetch_bse_filings.py ALL`
- Render MD to HTML: `python3 /tmp/render_plan.py research/SYMBOL.md`

---

## Part 6 — Portfolio Decision Framework

| Score | Action |
|-------|--------|
| A (20-25) | 5-10% position |
| B (15-19) | 2-5% position |
| C (10-14) | 1-2% or watchlist |
| D (<10) | Pass or exit |

**Three rules that override the score:**
1. Never hold more than 10% in a C-grade stock (regardless of past performance)
2. Exit any stock where the Kill Filter now fails (even if previously passed)
3. Cash is a position — a B-grade at 30% premium to fair value is worse than waiting

---

*"The job is to find reasons to REJECT, not believe. If a company survives skepticism, that is a meaningful signal."*
