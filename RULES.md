# Project rules (for review)

These are the rules and preferences for this repo. They are also applied in Cursor via `.cursor/rules/stocks-project.mdc`.

---

## 1. Scope

- **Fundamental investing only**: This repo is for long-term fundamental analysis and portfolio review, **not** for options, futures, or derivatives.
- **Dual market: India + US**. Primary focus on NSE/BSE. US stocks also in scope (SEC filings, US tickers). Separate workflows for each market since APIs and data sources differ.
  - **India**: Screener.in, BSE filings, Trendlyne, yfinance (`.NS`/`.BO` tickers)
  - **US**: SEC EDGAR, yfinance (plain tickers like `AAPL`), Anthropic financial plugins if they work well
- Portfolio allocation between markets is flexible — research-driven, not fixed.

---

## 2. Data and APIs

- **Prefer low-cost or free APIs**: When suggesting or implementing data sources, prefer free tiers or affordable APIs suitable for personal/fundamental use. Avoid recommending expensive real-time or institutional feeds unless explicitly asked.
- **Document limitations**: If using free or delayed data (e.g. Yahoo Finance), note it in code comments or README where relevant.

---

## 3. Reusable repo: ticker or stock details

- **One input contract**: Every script and module that takes a “stock” must accept either a **stock ticker** (str, e.g. `RELIANCE`, `TCS.NS`) or **stock details** (dict, e.g. `{"symbol": "INFY", "series": "EQ", "exchange": "BO"}`).
- **Single source of truth**: Use `stock_input.py` to normalize at entry points (`normalize_stock_input`, `to_ticker`, `to_symbol_series`). Downstream code should not re-parse ticker vs details.
- **Workflow**: Prefer the same shape for CLI and code (e.g. `run_stock.py <ticker_or_details> <command>`).

## 4. Code and outputs

- Keep analysis scripts reproducible (e.g. config-driven paths, clear CSV/Excel inputs).
- Portfolio and analysis outputs should be human-readable (CSV, simple charts) unless you ask for something else.

---

## 5. APIs for fundamental investing (low-cost / free)

Use these as preferred options when adding or recommending data sources. Not for options/futures—oriented use.

| Source | Type | What you get | Cost |
|--------|------|--------------|------|
| **Yahoo Finance (yfinance)** | Library | Prices, some fundamentals (income statement, balance sheet, cash flow) for many Indian tickers (`.NS` / `.BO`). Coverage can be patchy for smaller NSE/BSE names. | Free |
| **Indian Stock Exchange API** (indianapi.in) | REST API | Company info, financial statements, key ratios, BSE/NSE prices, analyst views, shareholding, news. | Free tier / check site |
| **Indian-Stock-Market-API** (GitHub) | Open-source API | Wraps Yahoo; real-time NSE/BSE prices and company info. No API key. | Free |
| **EODHD** | REST API | Historical prices + fundamental data for NSE. Free plan available. | Free tier; paid from ~$19.99/mo |
| **Fincrux** | API | Indian fundamentals: quarterly results, P&L, cash flow, shareholding, ratios (P/E, ROE, ROCE) for 3000+ companies. | Check site for pricing |
| **Tradient** | API | Indian market data, currency, GDP, news, technical indicators. | Claimed free (500K+ companies) |
| **NSE bhav copy / reports** | Official | EOD prices/volume via NSE archives or tools like Getbhavcopy / BhavCopyData.com. Financial statements via NSE corporate filings, not bhav copy. | Free (download/scripts) |

**Practical note**: For a simple, zero-cost setup, **yfinance** is already in this project and works for prices and basic fundamentals for many Indian stocks. For deeper fundamental coverage (ratios, quarterly financials, shareholding), consider **Fincrux** or **EODHD** free tier and document the source in the code.

---

*Edit this file or `.cursor/rules/stocks-project.mdc` to change rules; keep both in sync if you want the doc to match Cursor behavior.*
