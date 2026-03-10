# Groww (Billionbrains Garage Ventures)

**NSE:** GROWW.NS · **BSE:** GROWW.BO  
**Sector:** Financial Services · **Industry:** Capital Markets

---

## Valuation snapshot

*From `run_stock.py GROWW valuation` (yfinance + Indian-Stock-Market-API).*

### Price (1y)

| Metric | Value |
|--------|--------|
| Start price | ₹131.33 |
| End price | ₹169.22 |
| High | ₹188.77 |
| Low | ₹131.33 |
| Total return | **+28.85%** |
| Volatility (proxy) | 4.37% |

### Fundamentals

| Metric | Value |
|--------|--------|
| Market cap | ~₹1.04T |
| P/E (TTM) | 61.3 |
| Forward P/E | 35.9 |
| P/B | 13.7 |
| EPS | ₹2.76 |
| Revenue | ~₹40.5B |
| Net income | ~₹17.1B |
| Dividend yield | 0% |

---

## Recent quarterly results

*Source: yfinance quarterly income statement. Run `python run_stock.py GROWW valuation` to refresh.*

| Quarter end   | Revenue | Net income |
|---------------|---------|------------|
| 2025-12-31    | ₹12.16B | ₹5.47B     |
| 2025-03-31    | ₹4.81B  | ₹3.09B     |
| 2024-12-31    | ₹9.75B  | ₹7.57B     |

*Note: 2025-06-30 quarter may show partial data in the source. Use `output/quarterly_GROWW.csv` for full line items.*

Using the latest quarter (Dec 2025) and annualising (×4): revenue run-rate ~₹48.6B, net income run-rate ~₹21.9B. These can be used to cross-check TTM figures or to base a forward P/E / fair value on trailing quarterly trends.

---

## Fair value estimation

*Method: P/E-based. Fair value = Target P/E × EPS. Assumptions are not a recommendation.*

### Inputs (from snapshot)

- **EPS (TTM):** ₹2.76  
- **Current price:** ₹169.22  
- **Current P/E (TTM):** 61.3  

### Target P/E assumption

Target P/E is chosen by comparison to peers/sector (e.g. Indian fintech / capital markets). Here we use a **range** to show sensitivity.

| Scenario   | Target P/E | Fair value (₹) | vs current |
|------------|------------|-----------------|------------|
| Conservative | 35       | 96.60           | −43%       |
| Base case    | 40       | 110.40          | −35%       |
| Aggressive   | 45       | 124.20          | −27%       |

*Formula: Fair value = Target P/E × EPS = Target P/E × 2.76*

### Interpretation

- At **₹169.22**, the stock trades at **P/E 61**. If you believe a fair P/E is **35–45**, the implied **fair value range is ~₹97–₹124**.
- Current price is **above** that range → valuation appears **stretched** unless you assume higher long‑term P/E or much higher EPS growth.
- To use your own target P/E, run:  
  `python -c "from fundamental_valuation import run_valuation, ValuationInput; run_valuation('GROWW.NS', assumptions=ValuationInput(peer_pe=40))"`  
  and change `peer_pe=40` as needed.

---

*CSV: `output/valuation_GROWW.csv`*
