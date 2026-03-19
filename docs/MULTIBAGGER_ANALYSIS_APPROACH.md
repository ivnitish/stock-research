# Multi-Bagger Factor Analysis — Approach Document

**Status:** APPROACH ONLY — do not execute yet. This document defines the methodology.
**Created:** 2026-03-19
**Purpose:** Understand what actually drove historical multi-baggers so we can identify similar patterns in current holdings and watchlist.

---

## The Question

What were the 5x, 10x, 20x stocks in India over 3, 5, and 10-year lookback periods, and which specific factors drove those returns? Is it primarily:
- Earnings growth (revenue CAGR, margin expansion)?
- Multiple re-rating (P/E expansion from 10x → 40x)?
- A combination — and in what proportion?
- Was there a single inflection point (order win, policy change, capacity unlock) or slow compounding?

Answering this shapes how we score new ideas. If 70% of multi-bagger return comes from P/E re-rating rather than earnings growth, then the quality score's Valuation dimension (currently 1 of 5) deserves much more weight.

---

## Proposed Sample

### 3-Year Lookback (Mar 2023 → Mar 2026, 3x+ returns)
India candidates: Kaynes Technology, KERNEX, Lloyds Metals, Waaree Energies, Authum Invest, KPITTECH, Cochin Shipyard, Mazagon Dock, Waaree Solar, PGEL, Trent, Zomato (Eternal)

### 5-Year Lookback (Mar 2021 → Mar 2026, 5x+ returns)
India candidates: Tata Power, Suzlon, Adani Green, ABB India, Dixon Technologies, CAMS, Deepak Nitrite, Polycab, APL Apollo, Data Patterns, Paras Defence, MTAR Tech

### 10-Year Lookback (Mar 2016 → Mar 2026, 10x+ returns)
India candidates: Avenue Supermarts (DMart), PI Industries, Astral, Laurus Labs, Navin Fluorine, Alkyl Amines, Vaibhav Global, Page Industries, Bajaj Finance, Titan, Divis Labs

### US Comparison (for international lens)
Nvidia (2019→2026), ServiceNow, Celsius Holdings, Axon Enterprise, NuScale (SMTD)

---

## Data Points to Collect Per Stock

For each multi-bagger, capture at the start-date snapshot (not today's view):

### Price / Return Data
- CMP at start date
- CMP at end date
- Total return multiple (Nx)
- CAGR

### Earnings Decomposition (separate the two return drivers)
- P/E at start date
- P/E at end date
- P/E expansion multiple = End P/E / Start P/E → this is the "sentiment" return
- EPS at start date
- EPS at end date
- EPS growth multiple = End EPS / Start EPS → this is the "fundamental" return
- **Check:** P/E expansion × EPS growth = Total return multiple (should reconcile)

### Quality at Purchase Point (what did the stock look like THEN, not now)
- Revenue CAGR last 3 years (at start date)
- OPM at start date
- ROCE at start date
- D/E at start date
- Promoter holding at start date
- Market cap at start date (size filter: was it a micro/small/mid/large cap?)
- P/E at start date (were they cheap, fair, or expensive?)

### Catalyst Identification
- What was the specific inflection point? (policy, order, capacity, management change, new product)
- Was it visible at the start date or became visible later?
- How many quarters before/after the catalyst did the major re-rating happen?

### Red Flags Present at Start (false negatives we would have screened out)
- Would we have bought at the start date given our current framework?
- What would our quality score have been at start date?
- What were the thesis risks that DIDN'T play out?

---

## Analysis Framework

### Decomposition Table (per stock)

| Stock | Lookback | Start Price | End Price | Return | EPS Start | EPS End | EPS Multiple | P/E Start | P/E End | P/E Multiple | Key Catalyst | Visible at start? |
|-------|----------|-------------|-----------|--------|-----------|---------|-------------|-----------|---------|-------------|-------------|-------------------|
| | | | | | | | | | | | | |

### Factor Attribution

After collecting data for 15-20 multi-baggers, run attribution:

1. **Earnings-led multi-baggers** (EPS grew 8x, P/E flat or slight expansion) — these are the Bajaj Finance / Titan type. Thesis: buy quality at any reasonable price and wait.

2. **Re-rating-led multi-baggers** (EPS grew 2x, P/E expanded 5x) — these are the Adani Green / Mazagon Dock type. Thesis: find ignored sectors before the narrative shifts. Risk: re-rating reverses fast.

3. **Combined** (EPS 3x, P/E 3x = 9x total) — the sweet spot. Thesis: earnings growth + narrative/sector re-rating.

### Pattern Questions to Answer

1. What was the average P/E at the start date for India 5x+ stocks? (Were multi-baggers cheap or fairly priced at purchase?)
2. What ROCE threshold separated winners from losers? (Hypothesis: ROCE > 15% at start date is a necessary condition)
3. Were multi-baggers already showing revenue acceleration at start date, or did the acceleration come after?
4. What sectors produced the most multi-baggers in each period? (3yr: defence/EMS/renewables; 5yr: chemicals/capital goods?)
5. What was the size at start date? (Hypothesis: most 10x stocks were <₹2,000 Cr market cap at entry)

---

## Output Deliverables (when executed)

1. `data/multibagger_dataset.csv` — raw data for all stocks, all time periods
2. `docs/MULTIBAGGER_FINDINGS.md` — key patterns and conclusions
3. Updated scoring framework — if P/E re-rating is responsible for >50% of returns, the Valuation score needs higher weight or a separate "narrative timing" score

---

## How This Connects to Current Portfolio

After the analysis, map current holdings against the identified patterns:

| Pattern | Historical examples | Current portfolio match |
|---------|--------------------|-----------------------|
| ROCE >20% + <15x P/E + sector tailwind | DIxon early days, CAMS | ICICIAMC, KERNEX |
| Capacity doubling + order book 10x+ revenue | Mazagon Dock | KERNEX |
| Ignored monopoly/near-monopoly | CAMS, KFin early | ICICIAMC, KERNEX |
| Govt policy beneficiary (defence PLI, railways) | Cochin Shipyard, MTAR | KERNEX, KAYNES |

---

## Pre-requisites Before Executing

- [ ] Decide on data source: Yahoo Finance API (yfinance) for historical prices + Screener for historical fundamentals, OR manual collection
- [ ] Decide on 7 decision points from `docs/AUTORESEARCH_APPROACH.md` (PGEL-style backtesting context)
- [ ] Confirm stock list (do we include PSU defence stocks? Do we include pure commodity cycles like Adani Green?)
- [ ] Build Python script to automate price + earnings collection via yfinance for the snapshot dates

---

*"The purpose is not to find the pattern that explains the past. It is to find the pattern that is present NOW in a current holding or watchlist stock."*
