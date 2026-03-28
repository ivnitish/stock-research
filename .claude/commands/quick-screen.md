# Quick Screen — Fast Stock Screening

Screen `$ARGUMENTS` to decide if it deserves full research. This is a 5-minute filter, not a deep analysis.

## Steps

1. **Resolve the ticker:**
   - If Indian (no suffix or .NS/.BO/.BSE): use Screener.in
   - If US: use Alpha Vantage MCP or WebSearch

2. **Fetch key metrics** (Indian stocks via `web_fetch: https://www.screener.in/company/$ARGUMENTS/consolidated/`):
   - ROCE (3-year average)
   - ROE (3-year average)
   - Debt/Equity ratio
   - Promoter holding %
   - Revenue CAGR (5-year)
   - Profit CAGR (5-year)
   - Cash conversion (OCF vs PAT)
   - Current P/E and P/B

3. **Score against quality dimensions** (1-5 each, /25 total):
   - **Capital Efficiency:** ROCE > 20% = 5, 15-20% = 4, 10-15% = 3, 5-10% = 2, <5% = 1
   - **Growth:** Revenue CAGR > 25% = 5, 20-25% = 4, 15-20% = 3, 10-15% = 2, <10% = 1
   - **Balance Sheet:** D/E < 0.1 = 5, 0.1-0.3 = 4, 0.3-0.7 = 3, 0.7-1.5 = 2, >1.5 = 1
   - **Governance:** Promoter > 60% = 5, 50-60% = 4, 40-50% = 3, 30-40% = 2, <30% = 1
   - **Cash Quality:** OCF/PAT > 1.2 = 5, 1.0-1.2 = 4, 0.7-1.0 = 3, 0.5-0.7 = 2, <0.5 = 1

4. **Output verdict** (DO NOT create a research file):

```
## Quick Screen: [SYMBOL]
Score: [X]/25 | Grade: [A/B/C/D]
CMP: [price] | P/E: [X] | P/B: [X] | Mkt Cap: [X]

| Dimension        | Value     | Score |
|-----------------|-----------|-------|
| Capital Efficiency | ROCE X% | X/5   |
| Growth           | Rev CAGR X% | X/5 |
| Balance Sheet    | D/E X    | X/5   |
| Governance       | Promoter X% | X/5 |
| Cash Quality     | OCF/PAT X | X/5  |

**Verdict:** [Worth full research / Watchlist only / Pass]
**Key concern:** [1 line — the biggest question mark]
**Key strength:** [1 line — the most compelling aspect]
```

Grading: A = 20-25, B = 15-19, C = 10-14, D = below 10.
- A/B: Worth full `/research` analysis
- C: Watchlist — monitor for improvement
- D: Pass unless there's a specific catalyst thesis
