# Stock Research System — Session Status (2026-03-11)

## What We Built Today

### Phase 0: Folder Reorganization + Git Init — DONE
- Git initialized with `.gitignore` (excludes venv, xlsx, output, pycache)
- Python modules moved to `src/` (fundamental_valuation, portfolio_review, stock_analysis, indian_stock_api, nse_bhavcopy, get_company_name)
- Excel files moved to `data/groww/` with cleaner names
- Created: `research/`, `journal/weekly/`, `skills/`, `data/screener/`
- GROWW.md moved from docs/ to research/
- Imports updated, `run_stock.py GROWW valuation` verified working
- Initial commit on `main` branch

### Phase 1a: Anthropic Financial Plugins Evaluation — DONE
- Installed `financial-analysis` and `equity-research` plugins
- **Verdict: US-only.** Hardwired for SEC, FactSet, S&P. Wrong WACC, wrong currency, wrong peers for Indian stocks.
- **Keep for US stocks** — `/dcf AAPL`, `/comps MSFT` etc. should work well
- **For India**: Build custom skills using Screener.in + BSE filings
- Full evaluation: `docs/plugin_evaluation.md`

### Phase 1b: Groww Excel Importer — DONE
- Built `src/groww_importer.py` — parses Holdings + Orders Excel
- Output: `data/portfolio.csv` (37 stocks, ₹10,19,938 invested — matches Groww exactly)
- Output: `journal/decisions.csv` (468 historical orders with date, stock, action, quantity, price)
- ISIN → NSE symbol mapping from order history (163 symbols)
- Run: `python src/groww_importer.py`

### RULES.md Updated
- Scope expanded: India (primary) + US stocks
- Separate workflows for each market

---

## Current Folder Structure

```
stocks automation/
├── config.py, stock_input.py, run_stock.py   # Root (entry points + config)
├── src/                                       # All Python modules
│   ├── fundamental_valuation.py
│   ├── portfolio_review.py
│   ├── stock_analysis.py
│   ├── indian_stock_api.py
│   ├── nse_bhavcopy.py
│   ├── get_company_name.py
│   └── groww_importer.py                      # NEW
├── research/GROWW.md                          # Per-stock thesis
├── journal/decisions.csv                      # 468 historical orders
├── data/
│   ├── portfolio.csv                          # 37 real stocks
│   ├── groww/                                 # Broker Excel exports
│   └── screener/                              # Future: Screener.in exports
├── skills/                                    # Future: Claude skill definitions
├── docs/
│   ├── RESEARCH_SYSTEM_PLAN.md
│   ├── plugin_evaluation.md                   # NEW
│   └── SESSION_STATUS.md                      # This file
└── output/
```

---

## What's Next (Token-Efficient Priority)

### Do NOW (cheap — mostly Python code, no web fetching)

| Task | What | Tokens |
|------|------|--------|
| **Quality Scorecard** | `src/quality_scorecard.py` — Munger 5-dimension scoring (1-5 each, /25 total) | Low |
| **Thesis Template** | `research/_TEMPLATE.md` — standard format for all stocks | Low |
| **Cron: Weekly Portfolio Update** | Python script + cron that fetches prices via yfinance, updates portfolio value | Zero (runs without Claude) |
| **Cron: Red Flag Monitor** | Python script checking ROCE decline, promoter holding changes | Zero |

### Defer to Rate Limit Reset (expensive — needs web search + analysis)

| Task | What | Tokens |
|------|------|--------|
| **GROWW Thesis** | Full thesis using Screener.in data, DCF, quality score | High |
| **India Research Skill** | `skills/india-research.md` — Claude prompt adapted from vishalmdi | Medium |
| **DCF Model** | `src/dcf_model.py` with 3 scenarios + reverse DCF | Medium |
| **Top 6 Holdings Thesis** | KAYNES, EPACK, KERNEX, ARTEMIS, NAVA, PARADEEP | High |
| **Historical Decision Review** | Claude-assisted review of 468 past orders | High |

### Cron Jobs (save tokens permanently)

| Job | Schedule | What it does |
|-----|----------|--------------|
| `portfolio_update.py` | Daily 7pm IST | Fetch prices via yfinance, update portfolio value + P&L |
| `red_flag_monitor.py` | Weekly Sunday 9am | Check ROCE, promoter holding, debt for all 37 stocks |
| `weekly_digest.py` | Weekly Sunday 10am | Generate markdown summary of portfolio changes |

---

## Architecture Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| India data source | Screener.in + BSE + yfinance | Free, comprehensive for Indian stocks |
| US data source | Anthropic financial plugins | Official, designed for US markets |
| Valuation models | Custom Python (DCF, multiples) | India-specific WACC (7% RFR), INR/crores |
| Thesis storage | Markdown in `research/` | Human-readable, version-controlled |
| Decision log | CSV in `journal/` | Structured, queryable, backfilled from Groww |
| Claude skills | Markdown in `skills/` | Editable prompts, no plugin management |

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `config.py` | All paths, API URLs, sys.path setup |
| `stock_input.py` | Ticker normalization (single input contract) |
| `src/groww_importer.py` | Parse Groww Excel → portfolio.csv + decisions.csv |
| `src/fundamental_valuation.py` | Price analysis + yfinance fundamentals |
| `data/portfolio.csv` | Real portfolio (37 stocks) |
| `journal/decisions.csv` | 468 historical orders |
| `docs/plugin_evaluation.md` | Why Anthropic plugins don't work for India |
| `RULES.md` | Project scope and data source rules |

---

## Full Plan
See: `/Users/nitish/.claude/plans/toasty-frolicking-music.md`
