# Stock price analysis & fundamental valuation – what we need

## Groww share (GROWW)

**Valuation snapshot in markdown:** [GROWW.md](GROWW.md)

- **NSE:** `GROWW.NS` (Billionbrains Garage Ventures Limited)  
- **BSE:** `GROWW.BO`  
- Listed Nov 2025; we use **free data only** (yfinance + Indian-Stock-Market-API).

You can run **price analysis** and **fundamental valuation** with no extra input from you. If you want a **custom valuation** (e.g. DCF or peer P/E), we need the optional inputs below.

---

## What we need from you

### 1. Nothing (default)

We can run with **no input** from you:

- **Price analysis:** history, return, high/low, volatility (from yfinance).
- **Fundamentals:** P/E, P/B, ROE, EPS, revenue, net income, etc. (yfinance + API where needed).
- **Output:** console summary + `output/valuation_GROWW.csv`.

```bash
python run_stock.py GROWW valuation
# or
python fundamental_valuation.py GROWW.NS
```

### 2. Optional: assumptions for valuation

If you want a **fair value** or **target price** from multiples or DCF, you can pass:

| What | Meaning | Example |
|------|--------|--------|
| **Peer / target P/E** | P/E multiple to value the stock (e.g. vs sector) | `peer_pe=45` |
| **Revenue growth %** | Assumed revenue growth for projections | `revenue_growth_pct=25` |
| **Terminal growth %** | Long-term growth in DCF | `terminal_growth_pct=5` |
| **Discount rate %** | WACC / required return for DCF | `discount_rate_pct=12` |

Right now the script uses **reported data only** by default. To use these, call from code:

```python
from fundamental_valuation import run_valuation, ValuationInput

# Relative valuation: fair value = peer_pe * EPS
run_valuation("GROWW.NS", assumptions=ValuationInput(peer_pe=40))

# (DCF can be added later using revenue_growth_pct, terminal_growth_pct, discount_rate_pct)
```

### 3. Optional: your own data

If you have:

- **Financial statements** (Excel/CSV): we can add a loader and use them in valuation.
- **Peer list** (e.g. Zerodha, Upstox, other brokers): we can add peer P/E or EV/EBITDA comparison.
- **Bhav copy** for GROWW: place in `data/bhav/` for EOD prices in addition to yfinance.

---

## Data limits (free tier)

- **yfinance:** Good for price history and many fundamentals; coverage can be patchy for very new listings.
- **Indian-Stock-Market-API:** Good for current price and P/E when yfinance is missing.
- **Groww** listed in Nov 2025, so history is short; fundamentals may be incomplete on free sources.

For deeper valuation (full DCF, peer comparison, quarterly financials), consider Fincrux or EODHD (see RULES.md).
