---
name: india-equity-report-composite
description: >
  Composite India equity research skill. Use whenever analysing any Indian stock for investment.
  Merges vishalmdi's data sourcing discipline (Tickertape CMP, Screener.in financials,
  anti-hallucination rules) with Nitish's custom frameworks: Munger 5-dimension quality scorecard,
  P/B-ROE justified valuation, reverse DCF, and the single-file dated research log format.
  Triggers on: "analyse [stock]", "thesis for [stock]", "should I hold/buy/sell [stock]",
  "quality score for [stock]", or any stock analysis request for NSE/BSE-listed companies.
---

# India Equity Research — Composite Skill

Institutional-quality, Munger-philosophy research for NSE/BSE stocks. Combines:
- **vishalmdi's data workflow** (source discipline, anti-hallucination, CMP fetching)
- **Nitish's quality scorecard** (5-dimension, 1-5 each, /25 total)
- **P/B-ROE justified valuation** (not just P/E)
- **Reverse DCF** ("what growth is the market pricing in?")
- **Single-file research log** with dated entries

---

## MANDATORY PRE-FLIGHT RULES

1. **Never hallucinate figures.** Every number must come from a fetched source.
2. **Never use Screener.in for CMP.** It shows stale cached prices — use Tickertape or Google Finance.
3. **Never use Yahoo Finance for Indian CMP.** It shows US-session delayed prices, off by 10-15%.
4. **Every number in the report must carry an inline source tag** `[Source: URL, date]`.
5. If a number cannot be sourced after 2 attempts, write "data unavailable" — never estimate.

---

## STEP 0 — Identify and Resolve the Stock

- Resolve company name → NSE ticker (e.g., KAYNES, GROWW, NESCO)
- Confirm: NSE preferred, BSE fallback (prefix `BSE:`)
- Ambiguous? Ask the user before proceeding.

---

## STEP 1 — Fetch Live CMP (MANDATORY FIRST — before everything else)

> ⚠️ Screener.in and Yahoo Finance are BLOCKED for CMP. Both show stale/wrong prices.

**CMP fetch procedure:**
1. `web_search: "[TICKER] NSE share price [MONTH YEAR]"` — read price from Google Finance card in search snippet
2. If unclear → `web_fetch: https://www.tickertape.in/stocks/[company-slug]-[TICKER]`
3. Fallback → `web_fetch: https://www.5paisa.com/stocks/[company-name]-share-price`
4. Record as: `CMP: ₹[X.XX] [Source: Tickertape/Google Finance, DD-Mon-YYYY]`
5. Must be from most recent trading day. If >3 days old, flag explicitly.

**Do not proceed until you have a real ₹ number with a date.**

---

## STEP 2 — Fetch All Data (in this order)

| Data | Primary Source | Fallback |
|------|---------------|---------|
| Historical financials (P&L, BS, CF) | `screener.in/company/[TICKER]/consolidated/` | Tickertape |
| Key ratios (P/E, P/B, ROE, ROCE, D/E) | Screener.in (same page) | Trendlyne |
| Promoter & institutional shareholding | Screener.in shareholding tab | BSE filings |
| Quarterly results + commentary | `bseindia.com` corporate filings | NSE |
| Concall transcripts | Screener.in concall tab | `web_search: "[COMPANY] Q[N] FY[YY] concall transcript"` |
| News (last 90 days) | ET Markets, Mint, Business Standard | CNBCTV18, Moneycontrol |
| Peer comparison (≥3 peers) | `trendlyne.com/equity/[TICKER]/` peers section | Screener.in peer comparison |
| Analyst consensus target | Trendlyne analyst section | `web_search: "[TICKER] analyst target price 2026"` |
| Technical analysis | `web_search: "[TICKER] technical analysis tradingview 2026"` | Chartink |

---

## STEP 3A — MUNGER QUALITY SCORECARD (OUR ADDITION)

Rate each dimension 1-5. Calculate total /25. Assign grade.

| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| MOAT | | Type: cost/switching/network/intangible. Width: narrow/wide. Durability. |
| Management | | Promoter holding %, skin in game, capital allocation track record, pledging, governance |
| Financials | | ROCE%, ROE%, margins, debt, CFO/PAT ratio, FCF |
| Growth Runway | | TAM size, penetration, 3-5Y revenue CAGR potential, sector tailwinds |
| Valuation | | P/E vs growth (PEG), P/B vs ROE (justified P/B), DCF, vs peers |
| **Total** | **/25** | |

**Grade:** A (20-25) = High Conviction | B (15-19) = Moderate | C (10-14) = Watch | D (<10) = Avoid

**MOAT scoring guide:**
- 5: Wide, durable moat (monopoly, patent-backed, network effect + switching cost together)
- 4: Clear competitive advantage that will persist 5+ years
- 3: Advantage present but narrow or replicable in 3-5 years
- 2: Weak advantage, mainly scale or geography
- 1: No moat — pure commodity business

**Management scoring guide:**
- 5: Founder-led, 50%+ promoter holding, no pledging, excellent capital allocation, honest concall tone
- 4: Strong management, 40-50% promoter, minor concerns
- 3: Average — some concerns (low holding, pledging, or capital allocation misses)
- 2: Weak — promoter selling, high pledging, or governance red flags
- 1: Red flags — SEBI actions, fraud signals, or major governance issues

**Financials scoring guide:**
- 5: ROCE > 25%, ROE > 20%, net margin > 15%, CFO > PAT, D/E < 0.5, 3Y FCF positive
- 4: ROCE > 18%, ROE > 15%, decent margins, manageable debt
- 3: ROCE 12-18%, average margins, D/E 0.5-1.5
- 2: ROCE < 12%, thin margins, high debt or negative FCF
- 1: Loss-making or balance sheet at risk

---

## STEP 3B — DUPOINT ROE DECOMPOSITION (vishalmdi addition)

Always run 3-factor DuPont to understand WHY ROE is high or low.

```
ROE = Net Profit Margin × Asset Turnover × Equity Multiplier
```

| Component | FY[T-2] | FY[T-1] | FY[T] | Trend | What It Means |
|---|---|---|---|---|---|
| Net Profit Margin (%) | | | | ↑/↓ | Pricing power / cost efficiency |
| Asset Turnover (x) | | | | ↑/↓ | Capital efficiency |
| Equity Multiplier (x) | | | | ↑/↓ | Leverage (watch if rising) |
| **ROE (%)** | | | | | |

**Interpretation:**
- ROE rising due to higher margins = quality (sustainable, price it)
- ROE rising due to leverage = risk (don't pay premium for leverage-driven ROE)
- ROE rising due to asset turnover = efficiency (good, but check utilization limits)

---

## STEP 3C — FINANCIAL HEALTH SCORECARD (from vishalmdi analysis-frameworks)

Run every metric. Flag issues.

| Metric | Value | Flag if... | Status |
|--------|-------|-----------|--------|
| Revenue growth 3Y CAGR | | < 8% for growth stock | |
| EBITDA margin trend | | Declining 3 consecutive Qs | |
| ROE | | < 15% | |
| ROCE | | < 15% | |
| D/E | | > 1.5x (non-BFSI) | |
| Interest coverage | | < 3x | |
| CFO/PAT | | < 0.8 (earnings quality concern) | |
| Working capital trend | | Receivable days rising | |
| Promoter pledging | | Rising QoQ | |

---

## STEP 4 — VALUATION (use all 3 methods, explain disagreements)

### Method 1: P/E Re-rating
- TTM EPS (from Screener.in) and forward EPS (from analyst consensus or management guidance)
- Target P/E = 5-year median P/E OR peer median P/E (justify choice)
- Target Price = Forward EPS × Target P/E
- Show: Bull / Base / Bear scenarios

### Method 2: P/B-ROE (Justified Price-to-Book) — OUR ADDITION
The fundamental insight: a business that earns ROE above cost of equity deserves P/B > 1.

```
Justified P/B = (Sustainable ROE - g) / (Ke - g)
where:
  Ke = 10Y G-Sec yield + Beta × ERP (use 5.5-6.5% ERP)
  g = long-term terminal growth (5-6% for India)
```

Run 3 scenarios (bear/base/bull) with different sustainable ROE assumptions.

**Key question:** What ROE does the current P/B imply? (Implied ROE = Current P/B × (Ke - g) + g)
If implied ROE >> actual ROE: market is pricing in improvement you must verify.

### Method 3: Reverse DCF — OUR ADDITION
Don't just build a DCF — answer "what growth is the market already pricing in?"

```
Reverse DCF: Back-solve the FCF growth rate that justifies the current market cap
at a 12% discount rate and 5% terminal growth.
```

State: "At current price, market is pricing in [X]% FCF CAGR for 5 years."
Then judge: Is that achievable? Conservative? Aggressive?

### Method 4 (optional): EV/EBITDA
For capital-intensive or cyclical businesses.
EV = Market Cap + Net Debt
Target = (Sector median EV/EBITDA × Forward EBITDA) − Net Debt / Shares

### Sensitivity Table (mandatory for Method 1)
Build 2-variable sensitivity: EPS × P/E. Highlight base case.

---

## STEP 5 — VALUATION SUMMARY TABLE

Always include this:

| Model | Bear | Base | Bull | vs CMP |
|-------|------|------|------|--------|
| P/E Re-rating | ₹X | ₹X | ₹X | |
| P/B-ROE Justified | ₹X | ₹X | ₹X | |
| Reverse DCF says market prices in: | X% CAGR | | | |
| Analyst consensus (if available) | ₹X | | | [Source] |
| **Our verdict** | | ₹X | | |

If models disagree: explain WHY (e.g., "DCF is bearish because it doesn't capture high ROE; P/B-ROE is bullish because it rewards capital efficiency"). Identify which assumption drives the disagreement.

---

## STEP 6 — WRITE THE RESEARCH FILE

Save to `research/[TICKER].md` (one file per stock, NO separate files).

### Required sections:
```
# [Company Name] ([TICKER].NS) — Investment Thesis

**Status:** [OWNED/WATCHING/AVOIDED] ([shares], ₹[amount] invested, [%] of portfolio)
**Quality Score:** [X]/25 (Grade [A/B/C/D]: [label])
**Last Updated:** [Date]
**Data Source:** [sources used]

## 1. Business Summary
## 2. Quality Score (table)
## 3. Why This Could Be a Multi-Bagger (or Why It May Not)
## 4. Key Metrics (annual + quarterly tables)
## 5. Valuation (all 3 methods + summary table)
## 6. Risks (table: Risk | Probability | Impact | Mitigation)
## 7. Exit Triggers (checkboxes)
## 8. Review Schedule
## 9. Decision History (table)
## 10. Research Log (dated entries, newest first)
```

**Research Log format:** Every update appended with date header. Git tracks full history.
**SEBI disclaimer:** Add at bottom for formal reports.

---

## STEP 7 — QUALITY CHECKLIST (mandatory before delivering)

### 7a. Price & Source Check
- [ ] CMP is a real ₹ number with date — NOT from Screener.in price field or Yahoo Finance
- [ ] Every financial figure has `[Source: URL, date]` inline tag
- [ ] No analyst targets invented — only from Trendlyne/news if fetched

### 7b. Scorecard Check
- [ ] Quality scorecard has notes for every dimension (not just numbers)
- [ ] DuPont decomposition run and interpreted
- [ ] CFO/PAT ratio computed (earnings quality check)
- [ ] Promoter holding + pledging trend noted

### 7c. Valuation Check
- [ ] At least 2 of 3 valuation methods used
- [ ] Reverse DCF computed: "market is pricing in X% growth"
- [ ] P/B-ROE: implied ROE at current P/B computed and commented
- [ ] Bull/Base/Bear scenarios for primary method
- [ ] Sensitivity table included

### 7d. Research Log Check
- [ ] New entry added with today's date
- [ ] Key finding from this research summarized in 2-3 bullets
- [ ] Any thesis change explicitly called out ("thesis intact" or "thesis weakening because...")

---

## DATA SOURCE QUICK REFERENCE

**For CMP (live price):**
1. Web search: "[TICKER] NSE share price [Month Year]" → Google Finance card
2. Tickertape: `tickertape.in/stocks/[slug]-[TICKER]`
3. 5Paisa: `5paisa.com/stocks/[company-name]-share-price`

**For financials:**
- Screener.in: `screener.in/company/[TICKER]/consolidated/` — best for India

**For peers + analyst targets:**
- Trendlyne: `trendlyne.com/equity/[TICKER]/`

**BLOCKED:** Yahoo Finance (Indian CMP), Reddit/Twitter (financial data)

**India WACC defaults:**
- Risk-free rate: Current 10Y G-Sec (fetch from RBI, typically 6.8-7.2%)
- ERP: 5.5-6.5% (use 6%)
- Beta: Fetch from Trendlyne or compute from Screener price history
- Cost of equity (Ke): typically 12-14% for India mid/large cap

---

*Composite skill combining vishalmdi/india-equity-report-skill (data sourcing, anti-hallucination, report structure) + Nitish's custom frameworks (Munger quality scorecard, P/B-ROE, reverse DCF, research log format). Version 1.0 — 2026-03-12.*
