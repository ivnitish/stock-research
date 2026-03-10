# Anthropic Financial Plugins — Evaluation (2026-03-11)

## Plugins Tested
- `financial-analysis@financial-services-plugins` (core)
- `equity-research@financial-services-plugins` (add-on)

## 18 Slash Commands Available
`/dcf`, `/comps`, `/initiate`, `/earnings`, `/thesis`, `/screen`, `/sector`, and more.

## Verdict: US-only. Skip for India, keep for US stocks.

### Why they don't work for Indian stocks (from source code analysis):
- **Data sources**: MCP priority is S&P Kensho, FactSet, Daloopa, Morningstar — none cover Indian mid/small-caps. Fallback is SEC EDGAR (US only).
- **WACC**: Uses US 10-year Treasury as risk-free rate. No India govt bond yield or country risk premium.
- **Peers**: All examples use US tickers (MSFT, GOOGL, AMZN). No Indian peer logic.
- **Currency**: Defaults to USD millions. No INR/crore support.
- **Tax rate**: Assumes US corporate tax. India's ~25.17% not referenced.

Running `/dcf GROWW.NS` would produce a professional-looking model with **wrong assumptions**.

## What to borrow (structure is excellent):
- DCF 3-scenario structure with sensitivity tables
- Comps methodology (peer selection, multiple ranges)
- Excel formatting patterns (formulas over hardcodes, cell comments)
- Quality checklists and anti-hallucination rules

## What to build custom for India:
- Data layer: Screener.in + yfinance + BSE filings
- India WACC: ~7% risk-free (govt bond), 6-7% equity risk premium
- Indian peer database
- INR-denominated output in crores

## Keep installed for:
- US stock positions (~₹1L portfolio)
- `/dcf AAPL`, `/comps MSFT`, `/earnings GOOGL` etc. should work well
