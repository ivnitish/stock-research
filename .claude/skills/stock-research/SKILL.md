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
6. **Writing quality:** Bull/bear/compounding sections must read as analyst narratives — weave numbers into cause-effect explanations, not formulaic template-filling. WRITE to the `no-ai-slop` house style from the first draft (`.claude/skills/no-ai-slop/SKILL.md`) — it is the writing standard, not a cleanup step. Before finalising, verify with a detect pass on EVERY prose section — summary verdict, bull/bear, second-order stress test, peer-lens conclusions, recommendation, research log. Only tables, data blocks, and framework checklists are exempt.
7. **Recommendations carry prices, never "tracking".** The allowed set is BUY / BUY REDUCED / BUY AT ₹X / HOLD / TRIM / EXIT / SPECULATIVE / AVOID (see CLAUDE.md Phase 5.3). TRACKING POSITION and bare WATCHLIST are not recommendations.

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

### Step 2.5 — Segment & Insider Depth Pull (always)

Three additional fetches, produced as artifacts BEFORE analysis begins. The framework requires computing segment ROIC, checking insider activity, and watching promoter movement — these get skipped when there's no explicit fetch step producing them first.

1. **Segment data, 3 years.** Annual report segment note — segment revenue and segment PBIT broken out separately. Often at the back of the AR under "Segment Reporting." The consolidated P&L is not a substitute.
2. **Insider trading disclosures, 12 months.** BSE corporate filings → Insider Trading Disclosure section. Pull all transactions, classify as ESOP / open-market buy / open-market sell / pledge change / off-market transfer.
3. **Promoter shareholding, 8 quarters.** BSE shareholding pattern history. Track the trajectory and reconcile any quarter-on-quarter movement above 2% to a stated reason.

### Step 2.6 — Distribution / Capability Density Pull (conditional)

**Run when the thesis is forward-driven** — capex absorbing margin, mix shift in early innings, distribution still building — i.e., any candidate for the CLAUDE.md Phase 0.6 trigger. Skip otherwise.

Three additional fetches:

1. **Investor presentations, latest 4 quarters.** Look specifically for:
   - Dealer / distributor / outlet count (Astral, Cera, KEI report this)
   - Geographic territory or store count (Varun Beverages bottling lines, retail businesses)
   - Capacity utilization percentage and CWIP details
2. **Segment mix percentage, 5 years.** From AR segment notes — specialty/commodity, premium/standard, retail/institutional, export/domestic. Compute year-over-year change in basis points.
3. **Capex commissioning timeline.** From concall transcripts — when does CWIP convert to operating capacity, and what is the expected ROIC on the deployed capital based on prior cycles.

Compute three rates:
- Distribution density growth rate (YoY % change)
- Mix-shift rate (bps per year for last 3 years)
- Capacity utilization trajectory (rising / plateaued / declining)

Record in the research log. If any rate is below the Phase 4.5.5 kill signal threshold, flag immediately.

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

#### A. Every research note, always

- [ ] CMP is real ₹ number with date — NOT from Screener.in or Yahoo Finance
- [ ] Every figure has `[Source: URL, date]` tag
- [ ] Quality scorecard has notes for every dimension
- [ ] DuPont decomposition run and interpreted
- [ ] At least 2 of 3 valuation methods used
- [ ] Reverse DCF: "market prices in X% growth"
- [ ] Bull/Base/Bear scenarios present
- [ ] Research log entry with today's date added
- [ ] Bull/bear sections read as narratives, not formula-filling
- [ ] `no-ai-slop` detect pass run on every prose section of the file (not just bull/bear), flags fixed
- [ ] Second-order stress test completed (5-Whys + world-state at 2 and 5 years)
- [ ] 3-year segment revenue CAGR computed separately from consolidated headline (Pattern 6)
- [ ] 5-year promoter holding trajectory reviewed; movements >2% reconciled with stated reason
- [ ] 5-year ROIC trend pulled (not just current)
- [ ] 3-year operating margin trend pulled — to detect permanent compression vs capex absorption vs one-time recovery
- [ ] Pre-existing capability named: the specific physical thing (plant, license, certification, code, brand) already built that the thesis depends on
- [ ] Market label written explicitly: what consensus calls this, what we call it, what flips the label
- [ ] Kill signals checked (insider distribution, structural margin compression, active bear-case root cause, prior capex sub-10% ROIC, single-customer >40%, pledge >50%, audit qualification)
- [ ] Recommendation is one of BUY / BUY REDUCED / BUY AT ₹X / HOLD / TRIM / EXIT / SPECULATIVE / AVOID, with explicit price levels (entry, add-below, trim/sell target, thesis-break exit). No TRACKING POSITION, no bare WATCHLIST, no "interesting, worth watching"

#### B. Any BUY or BUY AT ₹X candidate (Multi-Bagger Pattern checklist, from multibagger_patterns.md)

- [ ] Organized market share in sub-segment computed (not just total market share)
- [ ] Pending regulatory equalizer identified (GST-type, BIS, FSSAI, licensing) or confirmed absent
- [ ] Bear case root cause verified: does it apply to the *current* business model or a prior one?
- [ ] For capex-heavy businesses: prior capex cycle ROIC verified before treating flat PAT as structural
- [ ] Operator prior domain experience checked (not just current company tenure)

#### C. Premium-quality compounder pattern only (Phase 0.6 entries — requires Step 2.6 done)

- [ ] Distribution density growth rate computed (>20% / 15-20% / <15% / declining)
- [ ] Mix-shift rate computed in basis points per year (>200bps / 100-200bps / <100bps / flat or reversing)
- [ ] Capacity utilization current % + CWIP trajectory noted
- [ ] If trailing P/E uninformative, forward PEG computed with defended forward EPS CAGR
- [ ] Phase 4.5.5 kill signals checked

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

---

## CHANGELOG

- **2026-07-06:** Applied v2 (user-approved): re-integrated the 2026-05-05/2026-05-10 "PROMOTED ACTIVE" additions into the main flow (Steps 2.5/2.6, Step 6 blocks A-C; one duplicate item merged). TRACKING POSITION removed from the recommendation set — replaced by BUY AT ₹X price alerts and mandatory price ladders (pre-flight rule 7, Step 6-A final item). See docs/proposals/SKILL_stock-research_v2.md.
