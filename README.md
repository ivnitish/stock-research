# Indian Stock Analysis & Portfolio Review

Simple setup for **Indian stock analysis** (NSE/BSE) and **portfolio review** using Python and Yahoo Finance. The repo and workflow are **reusable**: every script and module accepts either a **stock ticker** (e.g. `RELIANCE`, `TCS.NS`) or **stock details** (e.g. `{"symbol": "INFY", "series": "EQ", "exchange": "BO"}`).

## What’s included

- **Portfolio review** – Load your holdings from a CSV, fetch live prices, see P&L and allocation.
- **Stock analysis** – Fetch historical data for any Indian stocks and view return summary + normalized chart.
- **Indian-Stock-Market-API client** – Optional free REST API (no API key) for NSE/BSE prices and company info; can be used as the price source for portfolio review.
- **NSE bhav copy (EOD)** – Reusable EOD prices/volume by stock ticker or stock details; uses local files in `data/bhav/` or optional download from NSE.
- **Fundamental valuation** – Price analysis + fundamentals (P/E, ROE, revenue, etc.) and optional fair-value view; reusable for any symbol (e.g. **Groww**: `GROWW.NS`).

## Quick run

From the project folder (use `python3` if `python` is not available):

```bash
# One-time: create venv and install dependencies
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run Groww valuation (price + fundamentals)
python run_stock.py GROWW valuation

# Other runs
python run_stock.py RELIANCE company-name
python run_stock.py GROWW stock-info
python portfolio_review.py
python stock_analysis.py
```

If `pip install` fails with an SSL error, run the same commands in your own terminal (network/certificates may work there).

## Repo and workflow: one input contract

Across the repo, **stock identity** is always one of:

- **Ticker (str):** `RELIANCE`, `RELIANCE.NS`, `TCS.BO`
- **Stock details (dict):** `{"symbol": "TCS", "series": "EQ"}`, `{"symbol": "INFY", "exchange": "BO"}`

Normalization lives in **`stock_input.py`**. Use it at entry points; downstream code gets a single shape.

| Script / module        | Accepts ticker or details | What it does |
|------------------------|---------------------------|--------------|
| `run_stock.py`         | Yes (first arg)           | Single CLI: company-name, eod, stock-info, valuation, analysis |
| `get_company_name.py`  | Yes (arg or JSON string)  | Print company name |
| `portfolio_review.py`  | CSV column = ticker       | P&L and allocation |
| `stock_analysis.py`    | Yes (`symbols` list)       | History and return summary |
| `indian_stock_api.py`  | Yes (all functions)       | Prices and company info |
| `nse_bhavcopy.py`      | Yes (`get_eod`, batch)    | EOD from bhav copy |

**Single-entry workflow (ticker or details):**

```bash
python run_stock.py RELIANCE company-name
python run_stock.py '{"symbol":"TCS","exchange":"BO"}' company-name
python run_stock.py RELIANCE.NS eod 2025-02-07
python run_stock.py RELIANCE stock-info
python run_stock.py RELIANCE analysis --period 6mo
python run_stock.py GROWW valuation          # Price + fundamentals for Groww
```

**In code:** pass the same shape everywhere:

```python
from stock_input import normalize_stock_input, to_ticker, StockInput
from nse_bhavcopy import get_eod
from get_company_name import get_company_name

stock: StockInput = "RELIANCE"  # or {"symbol": "TCS", "series": "EQ"}
get_company_name(stock)
get_eod(stock, date(2025, 2, 7))
```

## Setup

1. **Create a virtual environment (recommended)**

   ```bash
   cd "/Users/nitish/stocks automation"
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Portfolio review

1. **Edit your holdings** in `data/portfolio.csv`:

   | Column         | Description                    |
   |----------------|--------------------------------|
   | symbol         | NSE: `RELIANCE.NS`, BSE: `RELIANCE.BO` (or just `RELIANCE` for default NSE) |
   | quantity       | Number of shares              |
   | avg_buy_price  | Average buy price per share   |
   | exchange       | Optional (NSE/BSE)            |

2. **Run the review**

   ```bash
   python portfolio_review.py
   ```

   By default, prices are from **yfinance**. To use the **Indian-Stock-Market-API** (free, no key) instead:

   ```bash
   USE_INDIAN_STOCK_API=1 python portfolio_review.py
   ```

   Or in code: `run_review(price_source="indian_api")`. If the API is unavailable, the script falls back to yfinance.

   Output: table in the terminal and `output/portfolio_review.csv` with current value, P&L, P&L %, and allocation %.

## Stock analysis

1. **Run with default symbols** (Reliance, TCS, HDFC Bank, Infy)

   ```bash
   python stock_analysis.py
   ```

2. **Use your own symbols** – Edit the `symbols` list at the bottom of `stock_analysis.py`, or call from another script:

   ```python
   from stock_analysis import run_analysis
   run_analysis(symbols=["RELIANCE.NS", "TATASTEEL.NS"], period="6mo")
   ```

   Output: return summary in the terminal and `output/stock_analysis.png` (normalized price chart).

## Ticker format (Yahoo Finance)

- **NSE:** symbol + `.NS` (e.g. `RELIANCE.NS`, `HDFCBANK.NS`)
- **BSE:** symbol + `.BO` (e.g. `RELIANCE.BO`)

You can use NSE symbol without suffix; the code will add `.NS` by default (see `config.py` to switch to BSE).

## Indian-Stock-Market-API (optional)

[Indian-Stock-Market-API](https://github.com/0xramm/Indian-Stock-Market-API) is a free, open-source REST API for NSE/BSE (wraps Yahoo Finance). No API key. A public instance is used by default; you can self-host and set `INDIAN_STOCK_API_BASE_URL` in the environment.

- **Use for portfolio prices**: `USE_INDIAN_STOCK_API=1 python portfolio_review.py` or `run_review(price_source="indian_api")`.
- **Use the client directly** (`indian_stock_api.py`):

  ```python
  from indian_stock_api import search, get_stock, get_stock_list, fetch_prices

  search("reliance")           # Find symbols by company name
  get_stock("RELIANCE.NS")     # Single stock: price, PE, sector, etc.
  get_stock_list(["ITC", "TCS.NS"], res="num")  # Multiple stocks
  fetch_prices(["RELIANCE.NS", "TCS.NS"])       # Dict of symbol -> last_price
  ```

  Test the client: `python indian_stock_api.py`

## NSE bhav copy (EOD, reusable by ticker or details)

Official NSE end-of-day prices/volume. **Reusable** for any stock ticker or stock-details dict.

1. **Local files (recommended)**  
   Put bhav copy CSV in `data/bhav/` as either:
   - `YYYY-MM-DD.csv`, or  
   - NSE-style `cm{dd}{Mon}{yyyy}bhav.csv` (e.g. `cm07FEB2025bhav.csv`).  
   You can download from [NSE historical reports](https://www.nseindia.com/resources/historical-reports-capital-market-daily-monthly-archives) or tools like Getbhavcopy / BhavCopyData.com.

2. **Use in code** – same interface whether you pass a **ticker** or **stock details**:

   ```python
   from datetime import date
   from nse_bhavcopy import get_eod, get_eod_batch, get_bhav_for_date, load_bhav_for_date

   # By ticker (RELIANCE, RELIANCE.NS both work)
   eod = get_eod("RELIANCE", date(2025, 2, 7))
   # -> {"symbol": "RELIANCE", "open": ..., "high": ..., "low": ..., "close": ..., "volume": ...}

   # By stock details (dict)
   eod = get_eod({"symbol": "TCS", "series": "EQ"}, date(2025, 2, 7))

   # Multiple stocks
   rows = get_eod_batch(["RELIANCE", "TCS.NS", {"symbol": "INFY"}], date(2025, 2, 7))

   # Load/fetch full bhav for a date (tries NSE if local file missing)
   df = get_bhav_for_date(date(2025, 2, 7), try_nse=True)
   # Or from a specific path
   df = load_bhav_for_date(date(2025, 2, 7), path="/path/to/cm07FEB2025bhav.csv")
   ```

   If no local file exists, the module can try to download from NSE (may be blocked without cookies; then use local only with `try_nse=False`).

## Project layout

```
stocks automation/
├── README.md
├── requirements.txt
├── config.py
├── stock_input.py       # Single source: ticker or stock details → canonical form (use everywhere)
├── run_stock.py         # CLI: run_stock.py <ticker_or_details> <command> [args]
├── get_company_name.py  # Company name from ticker or details
├── indian_stock_api.py  # Client for Indian-Stock-Market-API (free, no key)
├── nse_bhavcopy.py      # NSE bhav copy EOD by ticker or stock details
├── fundamental_valuation.py  # Price analysis + fundamentals + simple valuation (e.g. GROWW)
├── portfolio_review.py  # Portfolio P&L and allocation
├── stock_analysis.py    # Historical returns and chart
├── docs/
│   └── VALUATION_WHAT_WE_NEED.md  # What we need for valuation (Groww / any stock)
├── data/
│   ├── portfolio.csv   # Your holdings
│   └── bhav/           # Optional: NSE bhav copy CSV (YYYY-MM-DD.csv or cm*.*.csv)
└── output/              # Generated CSV and charts
```

## Notes

- Default price data is from Yahoo Finance (yfinance). Optional Indian-Stock-Market-API uses the same underlying source; market hours and delays apply.
- For official NSE/BSE data, consider NSE India APIs or bhav copy files; this setup is for quick personal analysis.
