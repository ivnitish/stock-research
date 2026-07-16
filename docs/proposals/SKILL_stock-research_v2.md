# PROPOSAL — stock-research SKILL.md v2 (re-integration)

**Status: APPLIED 2026-07-06 (user-approved, commit `65ff3ca`).** This document is kept as the historical record of the change. The live skill at `.claude/skills/stock-research/SKILL.md` now contains this content plus Addendum A (price-ladder recommendations); Addendum B (template consolidation) went into `research/_TEMPLATE.md` in the same commit.

## What this changes (and what it doesn't)

Zero new framework content. This is a reorganization of existing, already-validated content so a fresh forked skill context executes every step in order, instead of having to discover binding steps in an appendix after the step list ends.

1. **Step 2.5 (segment & insider depth pull) moves into the main flow** between Step 2 and Step 3 — verbatim content from the appendix.
2. **Step 2.6 (distribution/capability density pull) moves in right after it**, with its conditional trigger stated at the top.
3. **Step 6 checklist restructured into three blocks:** (A) every note, always; (B) any BUY or TRACKING candidate; (C) premium-quality compounder pattern only (Phase 0.6 entries). Same items, grouped by when they actually apply.
4. **The "SKILL ADDITIONS — PROMOTED ACTIVE" appendix is deleted** — everything in it now lives in the flow. A one-line changelog replaces it.
5. **One dedupe:** "segment revenue CAGR computed separately from consolidated headline" appeared twice (base pattern checklist + appendix additions). Kept once, in block A, with the 3-year specificity. No other item removed.

Approve → I copy the content below over the live SKILL.md and commit. Reject/edit → tell me what to change.

**Addenda (added 2026-07-06, also awaiting approval):** Addendum A (kill TRACKING POSITION, price-ladder recommendations) and Addendum B (template consolidation — the "junk reduction") at the bottom of this document.

---

# PROPOSED SKILL.md CONTENT

```
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
```

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
- [ ] Second-order stress test completed (5-Whys + world-state at 2 and 5 years)
- [ ] 3-year segment revenue CAGR computed separately from consolidated headline (Pattern 6)
- [ ] 5-year promoter holding trajectory reviewed; movements >2% reconciled with stated reason
- [ ] 5-year ROIC trend pulled (not just current)
- [ ] 3-year operating margin trend pulled — to detect permanent compression vs capex absorption vs one-time recovery
- [ ] Pre-existing capability named: the specific physical thing (plant, license, certification, code, brand) already built that the thesis depends on
- [ ] Market label written explicitly: what consensus calls this, what we call it, what flips the label
- [ ] Kill signals checked (insider distribution, structural margin compression, active bear-case root cause, prior capex sub-10% ROIC, single-customer >40%, pledge >50%, audit qualification)

#### B. Any BUY or TRACKING POSITION candidate (Multi-Bagger Pattern checklist, from multibagger_patterns.md)

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

- **2026-07-05:** Re-integrated the 2026-05-05/2026-05-10 "PROMOTED ACTIVE" additions (validated via NCDEX, MSEI, ADOR) into the main flow: Steps 2.5/2.6 into the India workflow, checklist additions into Step 6 blocks A-C. No content changes; one duplicate checklist item merged.

---

# ADDENDUM A — Recommendation format: no tracking positions (user directive 2026-07-05)

Applies to CLAUDE.md Phase 5.3, the _TEMPLATE.md Recommendation block, and Step 6 of this skill.

**TRACKING POSITION is removed as an allowed recommendation.** The user's direction: every note ends in a decision with explicit prices — either buy now, or name the price at which to buy; for held positions, name the price at which to add and the price/condition at which to sell. No 1-2% toehold positions.

**New recommendation set (replaces the Phase 5.3 matrix rows):**

| Situation | Recommendation | Required price levels |
|-----------|---------------|----------------------|
| Grade A/B + asymmetry >3x + MOS >20% | **BUY** (5-8%) | Entry now at ≤₹CMP; add-below price; sell/trim target at base-case fair value; thesis-break exit condition |
| Grade A/B + asymmetry 2-3x + MOS 10-20% | **BUY REDUCED** (3-5%) | Same four levels |
| Grade A/B, price too high (asymmetry <2x) | **BUY AT ₹X** (0% now, price alert) | The specific price where asymmetry ≥2x + MOS threshold is met; recompute after each quarterly print |
| Held position, thesis intact | **HOLD** | Add-below price; trim-above price (base-case fair value); exit condition |
| Held position, price ≥ bull case or thesis degraded | **TRIM / EXIT at ₹Y** | Specific level or condition |
| Grade C + MOS >40% | **SPECULATIVE** (1% max, hard exit rules) | Entry, stop, target |
| Grade C/D otherwise | **AVOID** | — |

The old matrix's argument for tracking positions ("watchlist means you'll never buy") is answered by BUY AT ₹X being a standing order with a concrete trigger, not a vague "wait for a better price" — every BUY AT ₹X must appear in the index and the watchlist table with its price, and the daily/weekly loops check it.

Related memory updates: `feedback_no_default_tracking` becomes "no tracking positions at all — BUY / BUY AT price / HOLD with targets / TRIM / EXIT / AVOID only."

---

# ADDENDUM B — Template consolidation ("junk reduction"), for _TEMPLATE.md

The template has grown to ~1,100 lines and reports duplicate the same content in 3-4 places. Proposed merges — no analytical content lost, each fact stated once:

**1. Scenario/valuation math: 4 places → 2.** Multi-Bagger Math (Summary) stays as the single scenario table. Section 4b (Outlook base + sensitivity) MERGES into Section 5 — its "primary driver" derivation becomes the input to 5.4's models instead of a parallel scenario exercise. The 5.4 Synthesis table absorbs 4b's sensitivity rows. One derivation chain: driver → models → scenario table.

**2. Reverse DCF: 3 places → 1.** Currently in Summary ("What does the market think"), 5.1 ("Quick reverse DCF"), and 5.2. Keep the math once in 5.2; Summary keeps only the one-paragraph conclusion (implied X% vs our Y%, the gap is the edge).

**3. Quarterly trend table: 2 places → 1.** Exact duplicate in Summary Key Metrics AND Section 4. Delete the Section 4 copy. Section 4's "CAGRs" table also derivable from the Summary P&L table — delete.

**4. Exit conditions: 2 places → 1.** Summary "When do I sell?" and Section 8 "Exit Triggers" are the same list twice. Keep Summary; Section 8 deleted.

**5. Risks: 4 places → 2.** Concerns (Summary) + Q4 "what breaks the thesis" + 5.2 risk table + Section 7 risk table. Keep Concerns (summary highlights) and ONE risk table (Section 7, absorbing 5.2's bear-case-value column). Q4 stays but as a single sentence + leading indicator (it already is).

**6. Market-label tables: 2 → 1.** The appendix "universal" label table supersedes the turnaround-only "What was true at the bottom" table (same rows plus two). Keep the universal one inside the Stress Test; delete the turnaround variant and the template appendix (same treatment as the SKILL appendix).

**7. Logs: 3 → 2.** Decision History (trades) stays. Research Log and Update History merge into one dated Research Log — each entry can carry a "changed: grade/reco/price" line where relevant.

**8. Action table gains the price ladder.** The Summary Action table becomes the Addendum A ladder (add-below / hold band / trim-above / exit condition) — and 5.3's duplicate "Action" line is deleted, pointing there instead.

**Net effect:** ~30-35% shorter reports, every number stated once, Summary Verdict remains the decision layer and Detailed Analysis the evidence layer. Sections kept as-is: Deep Dives, Compounding Q&A (Q0-Q5), Downside Framework, Growth Trigger Scan, Competitive Landscape, Glossary.
