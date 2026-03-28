# Gotchas — Known Failure Points

## Data Sourcing
- **Screener.in CMP is stale**: Shows cached prices days old (e.g., "13 Feb close" on Feb 27). ONLY use for historical financials. Get CMP from Tickertape or Google Finance search card.
- **Yahoo Finance off by 10-15%**: Shows US-session delayed quotes for Indian stocks. HDFCBANK showed ₹1,001 on Yahoo vs ₹869 actual NSE close. NEVER use for Indian CMP.
- **Alpha Vantage has no Indian fundamentals**: Only BSE price data (format: `RELIANCE.BSE`). For Indian fundamentals, always use Screener.in.
- **Screener.in free tier**: May hit rate limits. Space out fetches. Use consolidated view for holding companies.

## Research Quality
- **Narrative over formula**: Bull/bear/compounding sections must read like analyst notes, not template slot-filling. Bad: "ROIC 34% × 80% reinvestment = 27% CAGR." Good: "EPACK's compounding engine runs at 27% incremental ROIC on capital deployed into a market where India's PEB penetration is 15% versus 70%+ globally..."
- **Never fabricate data**: If you can't find a number after 2 attempts, write "data unavailable". Never estimate or infer financial figures.
- **Research log entries**: Keep full content, date every entry, merge findings into main sections with source refs. Don't condense without asking.

## Path & Environment
- **Project path has a space**: Always quote paths — `"/Users/nitish/stocks automation/"`. Scripts and git commands will break without quotes.
- **BSE filings script**: `python3 src/fetch_bse_filings.py SYMBOL` — saves to `data/filings/SYMBOL/`. Run this early for concall PDFs.

## Quality Scorecard Detailed Criteria

### MOAT (1-5)
- 5: Wide, durable (monopoly, patent-backed, network + switching cost together)
- 4: Clear competitive advantage persisting 5+ years
- 3: Advantage present but narrow or replicable in 3-5 years
- 2: Weak advantage, mainly scale or geography
- 1: No moat — pure commodity

### Management (1-5)
- 5: Founder-led, 50%+ promoter, no pledging, excellent capital allocation, honest concalls
- 4: Strong management, 40-50% promoter, minor concerns
- 3: Average — some concerns (low holding, pledging, capital allocation misses)
- 2: Weak — promoter selling, high pledging, governance red flags
- 1: Red flags — SEBI actions, fraud signals, major governance issues

### Financials (1-5)
- 5: ROCE > 25%, ROE > 20%, margin > 15%, CFO > PAT, D/E < 0.5, 3Y FCF positive
- 4: ROCE > 18%, ROE > 15%, decent margins, manageable debt
- 3: ROCE 12-18%, average margins, D/E 0.5-1.5
- 2: ROCE < 12%, thin margins, high debt or negative FCF
- 1: Loss-making or balance sheet at risk

### Growth Runway (1-5)
- 5: TAM 10x+ current revenue, penetration < 10%, 25%+ revenue CAGR runway for 7+ years
- 4: TAM 5-10x, clear expansion path, 20%+ CAGR for 5+ years
- 3: TAM 3-5x, moderate growth visibility
- 2: TAM < 3x or growth decelerating
- 1: Stagnant or shrinking market

### Valuation (1-5)
- 5: Trading below intrinsic value on all methods, PEG < 0.8
- 4: Fairly valued with upside on re-rating, PEG 0.8-1.2
- 3: Fairly valued, limited margin of safety
- 2: Expensive on most metrics, priced for perfection
- 1: Significantly overvalued, priced for impossibility
