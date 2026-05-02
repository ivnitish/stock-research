---
name: stock-research
description: >
  Use whenever analysing any stock for investment — Indian (NSE/BSE) or US.
  Triggers on: "analyse [stock]", "thesis for [stock]", "should I buy/sell/hold [stock]",
  "quality score for [stock]", "research [stock]", or any stock analysis request.
  Also triggers when user names a ticker and asks "what do you think?"
  Merges data sourcing discipline (Tickertape CMP, Screener.in financials,
  anti-hallucination rules) with Munger 5-dimension quality scorecard,
  P/B-ROE justified valuation, reverse DCF, and single-file research log format.
context: fork
---

# Stock Research — Full Framework

Institutional-quality, Munger-philosophy research for stocks. Combines:
- **Data discipline** (source verification, anti-hallucination, CMP fetching)
- **Munger quality scorecard** (5-dimension, 1-5 each, /25 total)
- **P/B-ROE justified valuation** (not just P/E)
- **Reverse DCF** ("what growth is the market pricing in?")
- **Single-file research log** with dated entries

---

## MANDATORY PRE-FLIGHT RULES

1. **Never hallucinate figures.** Every number must come from a fetched source.
2. **Never use Screener.in for CMP.** It shows stale cached prices — use Tickertape or Google Finance.
3. **Never use Yahoo Finance for Indian CMP.** It shows US-session delayed prices, off by 10-15%.
4. **Every number must carry an inline source tag** `[Source: URL, date]`.
5. If a number cannot be sourced after 2 attempts, write "data unavailable" — never estimate.
6. **Writing quality:** Bull/bear/compounding sections must read as analyst narratives — weave numbers into cause-effect explanations, not formulaic template-filling.

---

## MARKET DETECTION

- **Indian stocks:** No suffix, or ends in .NS/.BO/.BSE → use India workflow (Screener.in + BSE)
- **US stocks:** Standard US tickers (NVDA, GOOGL, etc.) → use US workflow (Alpha Vantage MCP + SEC)
- If ambiguous, ask the user.

---

## INDIA WORKFLOW

### Step 0 — Identify and Resolve
- Resolve company name → NSE ticker (e.g., KAYNES, GROWW, NESCO)
- NSE preferred, BSE fallback (prefix `BSE:`)

### Step 1 — Fetch Live CMP (MANDATORY FIRST)

> Screener.in and Yahoo Finance are BLOCKED for CMP. Both show stale/wrong prices.

**CMP fetch procedure:**
1. `web_search: "[TICKER] NSE share price [MONTH YEAR]"` — read price from Google Finance card
2. If unclear → `web_fetch: https://www.tickertape.in/stocks/[company-slug]-[TICKER]`
3. Fallback → `web_fetch: https://www.5paisa.com/stocks/[company-name]-share-price`
4. Record as: `CMP: ₹[X.XX] [Source: Tickertape/Google Finance, DD-Mon-YYYY]`
5. Must be from most recent trading day. If >3 days old, flag explicitly.

**Do not proceed until you have a real ₹ number with a date.**

### Step 2 — Fetch All Data

| Data | Primary Source | Fallback |
|------|---------------|---------|
| Historical financials (P&L, BS, CF) | `screener.in/company/[TICKER]/consolidated/` | Tickertape |
| Key ratios (P/E, P/B, ROE, ROCE, D/E) | Screener.in (same page) | Trendlyne |
| Promoter & institutional shareholding | Screener.in shareholding tab | BSE filings |
| Quarterly results + commentary | `bseindia.com` corporate filings | NSE |
| Concall transcripts | Screener.in concall tab | `web_search` |
| BSE filings (concalls, results PDFs) | `python3 src/fetch_bse_filings.py [TICKER]` | — |
| News (last 90 days) | ET Markets, Mint, Business Standard | CNBCTV18, Moneycontrol |
| Peer comparison (≥3 peers) | `trendlyne.com/equity/[TICKER]/` peers section | Screener.in |
| Analyst consensus target | Trendlyne analyst section | `web_search` |

### Step 3 — Analysis

#### 3A. MUNGER QUALITY SCORECARD

Rate each dimension 1-5. Calculate total /25. Assign grade.

| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| MOAT | | Type: cost/switching/network/intangible. Width/durability. |
| Management | | Promoter holding %, skin in game, capital allocation, pledging, governance |
| Financials | | ROCE%, ROE%, margins, debt, CFO/PAT ratio, FCF |
| Growth Runway | | TAM size, penetration, 3-5Y revenue CAGR potential, sector tailwinds |
| Valuation | | P/E vs growth (PEG), P/B vs ROE (justified P/B), DCF, vs peers |
| **Total** | **/25** | |

**Grade:** A (20-25) = High Conviction | B (15-19) = Moderate | C (10-14) = Watch | D (<10) = Avoid

**Scoring guides:** See `gotchas.md` for detailed 1-5 criteria per dimension.

#### 3B. DUPONT ROE DECOMPOSITION

```
ROE = Net Profit Margin × Asset Turnover × Equity Multiplier
```

| Component | FY[T-2] | FY[T-1] | FY[T] | Trend | Interpretation |
|---|---|---|---|---|---|
| Net Profit Margin (%) | | | | ↑/↓ | Pricing power / cost efficiency |
| Asset Turnover (x) | | | | ↑/↓ | Capital efficiency |
| Equity Multiplier (x) | | | | ↑/↓ | Leverage (watch if rising) |
| **ROE (%)** | | | | | |

- ROE rising from margins = quality (sustainable)
- ROE rising from leverage = risk (don't pay premium)
- ROE rising from asset turnover = efficiency (good, check utilization limits)

#### 3C. MULTI-BAGGER FRAMEWORK (Phases 0-4)

Run the full framework from CLAUDE.md:
- **Phase 0:** Threshold checks (accounting, capital structure, business viability)
- **Phase 1:** Compounding engine (incremental ROIC, unit economics, source of high ROIC)
- **Phase 2:** Reinvestment runway (TAM, reinvestment rate, capital allocation, runway duration)
- **Phase 3:** Competitive position (market share trend, widening vs narrowing advantage)
- **Phase 4:** Management quality (skin in game, communication, capital allocation philosophy)

#### 3D. SECOND-ORDER STRESS TEST

The standard framework answers "is this business good and is it cheap?" The stress test answers "what does the world look like if I'm right, and what could I be missing?" Two short drills — fill the corresponding subsection in `_TEMPLATE.md`.

**5-Whys on the ROIC engine.** Drill five layers from the first-order explanation ("ROIC is high because X") down to the systemic cause. If the fifth answer is something the company controls, the moat is fragile. If it's something structural about the industry or geography, it's durable.

**Base-case world-state at 2 years and 5 years.** If the thesis plays out, what does the company look like, what new things does management have to execute, and what new risks does success itself create? Most large losses come from theses that were correct on direction but missed what success triggered — new competitors, regulatory attention, margin compression from scale, capital allocation mistakes when cash starts flowing.

### Step 4 — Valuation (use all 3 methods)

#### Method 1: P/E Re-rating
- TTM EPS + forward EPS
- Target P/E = 5-year median or peer median (justify)
- Bull/Base/Bear scenarios with sensitivity table

#### Method 2: P/B-ROE (Justified Price-to-Book)
```
Justified P/B = (Sustainable ROE - g) / (Ke - g)
where: Ke = 10Y G-Sec + Beta × ERP (6%), g = 5-6% for India
```
Run 3 scenarios. Key question: What ROE does the current P/B imply?

#### Method 3: Reverse DCF
```
Back-solve FCF growth rate that justifies current market cap
at 12% discount rate and 5% terminal growth.
```
State: "At current price, market is pricing in [X]% FCF CAGR for 5 years."

#### Valuation Summary Table (mandatory)

| Model | Bear | Base | Bull | vs CMP |
|-------|------|------|------|--------|
| P/E Re-rating | ₹X | ₹X | ₹X | |
| P/B-ROE Justified | ₹X | ₹X | ₹X | |
| Reverse DCF implies: | X% CAGR | | | |
| Analyst consensus | ₹X | | | [Source] |
| **Our verdict** | | ₹X | | |

### Step 5 — Write Research File

Save to `research/[TICKER].md` using `research/_TEMPLATE.md` as structural guide.

**Required sections:** Business Summary, Quality Score, Why This Could Be a Multi-Bagger, Key Metrics, Valuation (all methods + summary table), Risks, Exit Triggers, Review Schedule, Decision History, Research Log.

### Step 6 — Quality Checklist (mandatory before delivering)

- [ ] CMP is real ₹ number with date — NOT from Screener.in or Yahoo Finance
- [ ] Every figure has `[Source: URL, date]` tag
- [ ] Quality scorecard has notes for every dimension
- [ ] DuPont decomposition run and interpreted
- [ ] At least 2 of 3 valuation methods used
- [ ] Reverse DCF: "market prices in X% growth"
- [ ] Bull/Base/Bear scenarios present
- [ ] Research log entry with today's date added
- [ ] Bull/bear sections read as narratives, not formula-filling
- [ ] Second-order stress test completed (5-Whys + world-state at 2 and 5 years)

---

## US WORKFLOW

### Step 1 — Fetch Data
- Use Alpha Vantage MCP for: fundamentals, earnings, income statement, balance sheet, cash flow
- `web_search` for: SEC filings (10-K, 10-Q), analyst consensus, competitive landscape
- CMP: Alpha Vantage MCP `get_ltp` or `web_search: "[TICKER] stock price"`

### Step 2 — Analysis
- Same quality scorecard (adjust governance for US context — institutional ownership, insider buying)
- Same DuPont decomposition
- Same multi-bagger framework

### Step 3 — Valuation
- DCF with US WACC (risk-free = 10Y Treasury, ERP = 5%, Beta from Alpha Vantage)
- P/E re-rating with US peer medians
- Reverse DCF

### Step 4 — Write to `research/us/[TICKER].md`

---

## GENERAL INSTRUCTIONS

1. **Always show your math.** ROIC = show numerator + denominator. Runway = show TAM + penetration numbers.
2. **Be specific with numbers.** Not "margins are healthy" — "EBITDA margin 18.5%, up from 14.2% three years ago, driven by operating leverage on 38% revenue CAGR."
3. **Distinguish facts from inferences.** Label opinions explicitly.
4. **For earnings call transcripts:** Extract KEY numbers and management claims first, then evaluate through the multi-bagger lens.
5. **When data is insufficient**, say so and state exactly what additional data would help.
6. **Be skeptical of management narratives.** Cross-reference against financials.
7. **For Indian small/mid caps:** Pay extra attention to promoter quality, related party transactions, and cash flow vs reported profits.
8. **Do not default to positive conclusions.** Base rate for multi-baggers is low. Your job is to find reasons to REJECT.
