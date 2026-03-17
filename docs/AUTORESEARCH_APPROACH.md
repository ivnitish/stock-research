# Autoresearch: Thesis Backtesting Engine — Approach Document

**Status:** PROPOSAL — awaiting review before implementation
**Inspired by:** [karpathy/autoresearch](https://github.com/karpathy/autoresearch)
**Created:** 2026-03-17

---

## The Core Idea

Karpathy's autoresearch loop: **hypothesis -> experiment -> metric -> iterate**

Translated to stock research: **thesis -> historical backtest -> outcome measurement -> calibrate the research process**

The goal is NOT to predict stock prices. The goal is to **measure and improve the quality of our own research framework** — our quality scorecard, DCF models, risk identification, and thesis construction.

---

## What Problem Does This Solve?

Right now we build theses for stocks we own. But we have no way to know:

1. **Is our quality scorecard predictive?** Do stocks scoring 18+ actually outperform stocks scoring 12?
2. **Are our DCFs systematically biased?** Do we consistently overestimate fair value by 30%? 50%?
3. **Which scorecard dimensions matter?** Maybe MOAT predicts returns but Management score is noise.
4. **Do our exit triggers fire early enough?** Or do we identify risks after the damage is done?
5. **What patterns separate winners from losers?** In our actual portfolio, NWIL is +52% and PARADEEP is -35%. What was different in the thesis?

Without backtesting, we're flying blind — we build theses that *feel* rigorous but we have no feedback loop on whether they're actually *predictive*.

---

## Architecture

```
autoresearch/
├── historical_data.py        # Fetch financials + price as of any historical date
├── historical_thesis.py      # Generate quality score + DCF using ONLY data available at date X
├── outcome_tracker.py        # What actually happened over next 6m / 12m / 24m
├── backtest_engine.py        # Run thesis generation + outcome tracking across portfolio
├── calibration_report.py     # Analyze patterns: what's predictive, what's noise?
├── screener_loop.py          # (Future) Run scorecard across 500 stocks overnight
└── findings/
    ├── portfolio_backtest.md  # Results for our 35 stocks
    └── calibration.md         # Framework adjustments based on findings
```

---

## Phase 1: Historical Thesis Generator

### Input
- Ticker (e.g., `GROWW.NS`)
- Historical date (e.g., `2025-03-17` — exactly 1 year ago)

### What It Does
Using ONLY data available on that date:

1. **Pull historical financials** from yfinance:
   - Quarterly P&L (revenue, net profit, OPM)
   - Balance sheet (debt, equity, book value)
   - Price on that date
   - Trailing ratios (P/E, P/B, ROE, ROCE, D/E)

2. **Run quality scorecard** programmatically:
   - MOAT: Use sector + margin consistency as proxy (not perfect, but measurable)
   - Management: Promoter holding trend, debt trajectory
   - Financials: ROE, ROCE, D/E, OPM, FCF generation
   - Growth: Revenue CAGR (3yr trailing), profit CAGR
   - Valuation: P/E vs sector median, P/B vs ROE-justified

3. **Run DCF** with historical data:
   - Base FCF from trailing year
   - Growth rates from historical CAGR (not forward-looking)
   - Same discount rate / terminal growth we use now (12% / 5%)

4. **Output**: Quality score, fair value range, buy/hold/sell signal

### Data Available from yfinance (free)
- Quarterly financials (income statement, balance sheet, cash flow) — last 4 quarters
- Historical daily prices — as far back as needed
- Basic ratios and metadata

### What's NOT Available (limitations)
- Promoter holding history (only current snapshot) — but BSE archives have this
- Screener.in historical data — not via API
- Peer comparison data at historical dates — would need to pull peers' yfinance data too
- Qualitative factors (management quality, moat strength) — we'd use proxies or skip

---

## Phase 2: Outcome Measurement

For each historical thesis, measure what actually happened:

| Metric | How to measure |
|--------|---------------|
| Absolute return (6m, 12m, 24m) | Price change from thesis date |
| Relative return vs Nifty Smallcap 250 | Stock return minus index return |
| Did buy signal work? | If thesis said BUY, did stock beat index? |
| Did sell signal work? | If thesis said SELL, did stock underperform? |
| DCF accuracy | Compare predicted fair value vs actual price 12m later |
| Risk prediction | Did identified risks actually materialize? |

---

## Phase 3: Calibration Analysis

This is where the real value is. Across all backtested theses:

### Question 1: Is the quality scorecard predictive?

Group stocks by quality score tier and check returns:

| Quality Tier | Avg 12m Return | vs Nifty SC250 | n (stocks) |
|---|---|---|---|
| A (20-25) | ? | ? | ? |
| B (15-19) | ? | ? | ? |
| C (10-14) | ? | ? | ? |
| D (<10) | ? | ? | ? |

**If A-tier consistently beats C-tier**, the scorecard works. If not, we need to redesign it.

### Question 2: Which dimensions are predictive?

Run correlation analysis:

| Dimension | Correlation with 12m return | Statistically significant? |
|---|---|---|
| MOAT score | ? | ? |
| Management score | ? | ? |
| Financials score | ? | ? |
| Growth score | ? | ? |
| Valuation score | ? | ? |

**Expected finding**: Valuation score is probably the most predictive (buying cheap works). MOAT is probably second. Management may be noise (hard to score accurately from public data alone).

**Action**: Reweight the scorecard. If Valuation and Financials explain 80% of return variance, make them 40% of the score (not 20% each).

### Question 3: DCF bias measurement

| Stock | DCF Fair Value (predicted) | Actual Price 12m Later | Error % |
|---|---|---|---|
| GROWW | ₹180 | ₹170 | -6% |
| KAYNES | ₹X | ₹Y | Z% |
| ... | ... | ... | ... |

**Systematic bias**: If we consistently overestimate by 25%, we can apply a "reality discount" to all future DCFs.

### Question 4: Risk prediction quality

For each risk we identified in historical theses:
- Did it actually happen?
- If it happened, did it impact the stock price as we predicted?
- Are there risks we missed that actually drove the stock?

**This trains us to focus on risks that matter vs risks that are just listed for completeness.**

---

## Phase 4: Screener Loop (Future — the "overnight research" vision)

Once the scoring framework is calibrated:

1. Pull list of NSE Smallcap 250 stocks (or top 500 by liquidity)
2. For each stock: fetch yfinance data, run calibrated scorecard, run DCF
3. Rank all 500 by quality-adjusted-value score
4. Output: top 20 stocks our model likes that we DON'T already own
5. Run this weekly via cron — zero interactive tokens

**This is the autoresearch loop**: the system generates research candidates overnight, and you come in to review only the top picks, adding qualitative judgment that the model can't do.

---

## Implementation Considerations

### What we need to build

| Module | Effort | Dependencies |
|---|---|---|
| `historical_data.py` (yfinance historical fetch) | Low | yfinance |
| Quality scorecard — programmatic version | Medium | Need to encode scoring rules as code, not just judgment |
| `historical_thesis.py` (combine data + score + DCF) | Medium | historical_data + scorecard + dcf_model |
| `outcome_tracker.py` | Low | yfinance prices |
| `backtest_engine.py` (orchestrate across portfolio) | Medium | All above |
| `calibration_report.py` (statistical analysis) | Medium | numpy/pandas |

### The hard part: programmatic scoring

Our current quality scorecard has qualitative components (MOAT, Management quality) that require human judgment. For backtesting, we need **quantitative proxies**:

| Dimension | Qualitative (current) | Quantitative proxy (for backtesting) |
|---|---|---|
| MOAT | "does this company have pricing power?" | OPM consistency (std dev over 3 years), OPM vs sector median |
| Management | "is management honest and capable?" | Promoter holding level + trend, debt trajectory, dividend consistency |
| Financials | "are the numbers clean?" | ROE, ROCE, D/E, FCF/PAT ratio, interest coverage |
| Growth | "is the runway long?" | Revenue CAGR 3yr, profit CAGR 3yr, capex/revenue ratio |
| Valuation | "is it cheap enough?" | P/E vs sector, P/B vs ROE-justified, earnings yield vs bond yield |

**Key insight**: The quantitative proxy won't be as good as human judgment for any single stock. But across 500 stocks, it should produce statistically meaningful signal vs noise measurement.

### Backtest period options

| Period | Pros | Cons |
|---|---|---|
| 1 year lookback (Mar 2025 → Mar 2026) | Recent, relevant to current market | Only one cycle, results may be noise |
| 3 year lookback (Mar 2023 → Mar 2026) | Covers bull run + correction | Bull market may inflate all scores |
| 5 year lookback (Mar 2021 → Mar 2026) | Covers COVID crash + recovery + correction | Older data may not reflect current business quality |

**Recommendation**: Start with 1-year for all 35 portfolio stocks (quick, relevant). Then expand to 3-year for calibration.

---

## Proposed Improvement Ideas (for discussion)

### 1. Sector-relative scoring instead of absolute
Instead of scoring MOAT 1-5 absolutely, score it relative to the sector. A 15% OPM in transformers might be average, but in fertilizers it's exceptional. This prevents systematic sector bias.

### 2. Momentum overlay
Add a "market perception" dimension: is the stock in an uptrend or downtrend at thesis date? Stocks with improving financials + price momentum tend to outperform. This is anti-Munger (he ignores price) but may be statistically valid.

### 3. Position sizing from conviction score
If backtesting shows quality score reliably predicts returns, use it for position sizing: A-tier stocks get 5-8% allocation, B-tier 2-4%, C-tier 1-2% or exit.

### 4. Regime detection
The backtesting engine should identify market regimes (bull/bear/sideways) and measure whether our scoring works differently in each. Maybe the scorecard excels in bear markets (quality shines) but fails in bull markets (everything goes up).

### 5. "What would Munger buy?" benchmark
Generate a Munger-style filter on the historical data: ROCE > 25%, D/E < 0.5, revenue CAGR > 15%, OPM > 20%, promoter > 50%. How does this simple filter compare to our more complex scorecard? If the simple filter beats us, our complexity is adding noise, not signal.

### 6. Paper portfolio tracking
Once the overnight screener (Phase 4) is running, maintain a "paper portfolio" of its top 20 picks. Track it for 3-6 months before committing real capital. This validates the system in real-time without financial risk.

---

## Decision Points (for Nitish to review)

1. **Scope**: Start with 35 portfolio stocks or go wider (NSE 500)?
2. **Lookback period**: 1 year or 3 years?
3. **Scorecard**: Keep qualitative dimensions (human judgment) or go fully quantitative (proxies)?
4. **DCF calibration**: Worth the effort or skip and just use scorecard?
5. **Overnight screener**: Build now or after calibration proves the scorecard works?
6. **Improvement ideas**: Which of the 6 ideas above are worth pursuing?
7. **Timeline**: Build this now or after existing thesis backlog is done?

---

## Next Steps (after review)

- [ ] Nitish reviews this doc and answers decision points
- [ ] Build `historical_data.py` as MVP (fetch any stock's financials at any date)
- [ ] Encode quality scorecard as Python function (quantitative version)
- [ ] Backtest on 6 core holdings first (GROWW, KAYNES, EPACK, KERNEX, SHILCTECH, NESCO)
- [ ] Generate calibration report
- [ ] Decide whether to expand to full 35 or NSE 500
