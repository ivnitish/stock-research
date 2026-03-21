# Stock Research System

Personal fundamental research system for identifying multi-bagger opportunities in Indian equities (NSE/BSE) with selective US positions.

**Philosophy:** Charles Munger — read a lot, analyze deeply, hold long. Target: 25% IRR.

---

## What's Here

### Research Files (`research/`)
Per-company investment theses using a structured multi-bagger framework:
- Kill Filter → Compounding Engine → Management Quality → Competitive Landscape → Valuation
- Quality Score: 5 dimensions × 5 points = 25 max (A/B/C/D grade)
- DCF: Bear / Base / Bull with capacity-anchored growth rates

### Portfolio Dashboard (`output/html/index.html`)
Live portfolio view with holdings, fair values, buy zones, expected CAGR, and per-stock thesis links.
Hosted at: [ivnitish.github.io/stock-research](https://ivnitish.github.io/stock-research)

### Automation (`src/`)
- Daily portfolio price update (7pm)
- Weekly red flag monitor (promoter pledging, ROCE decline)

### BSE Filing Fetcher (`scripts/fetch_bse_filings.py`)
On-demand downloader for quarterly results, concall transcripts, annual reports, investor presentations from BSE.
```bash
python3 scripts/fetch_bse_filings.py KERNEX           # last 365 days
python3 scripts/fetch_bse_filings.py RAYMOND --days 180
python3 scripts/fetch_bse_filings.py ALL              # all portfolio stocks
```
Downloads to: `data/financial statemnt and concals/{SYMBOL}/`

---

## Portfolio Companies

20 Indian stocks across defence, EMS, aerospace, fintech, BFSI, capital goods, and pharma.

---

## Key Docs

| Doc | Purpose |
|-----|---------|
| `research/_TEMPLATE.md` | Master research template |
| `docs/RESEARCH_APPROACH.md` | Data sources + research workflow |
| `docs/VALUATION_FRAMEWORK.md` | DCF + P/B-ROE methodology |
| `docs/TODO.md` | Active decisions + research backlog |
| `docs/SUPPLIER_CUSTOMER_DATA.md` | Customer/supplier analysis for all portfolio stocks |
