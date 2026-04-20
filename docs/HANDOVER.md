# Stock Research System — New Chat Handover

*Read this at the start of every new Claude Code session in `/Users/nitish/stocks automation/`.*

---

## What this system is

A personal equity research pipeline. You write research notes in Markdown, they render to HTML (GitHub Pages), and can be exported as private-data-free PDFs. The framework is Munger-style fundamental analysis focused on identifying multi-baggers (20%+ CAGR compounders).

**GitHub Pages (live site):** ivnitish.github.io/stocks  
**Working directory:** `/Users/nitish/stocks automation/`  
**Model preference:** Claude Opus (claude-opus-4-6)

---

## When user says "stock research" on a new company

1. **Fetch financials:** `python3 src/fetch_bse_filings.py SYMBOL` for filings; WebFetch `screener.in/company/SYMBOL/consolidated` for ratios
2. **Use the template:** `research/_TEMPLATE.md` — follow the 11-section structure
3. **Output file:** `research/SYMBOL.md`
4. **Render to HTML:** `python3 src/render_all.py SYMBOL` — renders HTML + generates PDF automatically
5. **Update index:** Add row to `output/html/index.html` (see rules in `.claude/rules/index-always.md`)
6. **Open in Chrome to review:** `open output/html/SYMBOL.html`
7. **Push:** `git push origin main`

**Quality scoring:** 5 dimensions × 5 points = 25 max. A=20-25, B=15-19, C<15, D=structural problem.

**Never fabricate data.** If Screener.in doesn't have it, say so.

---

## Key commands

| Task | Command |
|------|---------|
| Research a stock (render + PDF) | `python3 src/render_all.py SYMBOL` |
| Rebuild all HTML + all PDFs | `python3 src/render_all.py` |
| Rebuild all HTML only (fast) | `python3 src/render_all.py --no-pdf` |
| Generate PDFs only | `python3 src/generate_pdfs.py` or `python3 src/generate_pdfs.py SYMBOL` |
| Fetch BSE filings | `python3 src/fetch_bse_filings.py SYMBOL` |
| Push to GitHub | `git push origin main` |
| Open index in browser | `open output/html/index.html` |
| Open PDF folder | `open output/pdf/` |

---

## Key files

| File | Purpose |
|------|---------|
| `research/_TEMPLATE.md` | Master template for every research note |
| `research/SYMBOL.md` | Individual stock research (source of truth) |
| `output/html/SYMBOL.html` | Rendered HTML (auto-generated, don't edit) |
| `output/pdf/SYMBOL_DATE.pdf` | PDF exports (portfolio data hidden via print CSS) |
| `output/html/index.html` | Homepage / stock list — update manually after each new stock |
| `docs/TODO.md` | Active tasks and backlog |
| `docs/DECISION_LOG.md` | Buy/sell decision history |
| `portfolio.csv` | Current holdings with entry price, qty, avg cost |
| `data/filings/SYMBOL/` | Downloaded BSE PDFs |
| `data/transcripts/` | Concall summaries and channel notes |
| `src/render_plan.py` | Markdown→HTML renderer (with PRIVATE block support) |
| `src/render_all.py` | Batch render all files + generate PDFs |
| `src/generate_pdfs.py` | Chrome headless PDF generator |

---

## Private data in PDFs

Portfolio data (entry price, P&L, decision history) is **visible in the browser but hidden in PDFs**.

How it works:
- In markdown, wrap private content with `<!-- PRIVATE -->...<!-- /PRIVATE -->`
- Lines with `**Entry:**` or `**P&L:**` are auto-wrapped as private
- The "Decision History" section is auto-wrapped as private
- In HTML, these render with a yellow tint (visible to you)
- In PDFs (via print CSS), they disappear completely — safe to share

---

## Active portfolio (as of Apr 2026)

| Symbol | Status | Key trigger |
|--------|--------|-------------|
| NEWGEN | HOLD, 200 shares | Q4 FY26 results May 5, 2026 |
| PATELSAIR | SMALL STARTER | Nuclear order flow watch |
| EPACKPEB | HOLD | Capacity ramp FY27 |
| Others | See `portfolio.csv` | — |

**Pending exits to review:** SWIGGY, STL, ARTEMIS, ETERNAL, GRSE, RAYMOND (see TODO.md)

---

## Data sources

| Source | What it provides | How |
|--------|-----------------|-----|
| Screener.in | Indian fundamentals (P&L, BS, ratios, 10yr) | WebFetch `screener.in/company/SYMBOL` |
| BSE filings | Quarterly results, concall PDFs, annual reports | `src/fetch_bse_filings.py` |
| Groww MCP | Live prices, market data | `mcp__growwmcp__get_ltp` |
| Kite MCP | Live portfolio, orders | `mcp__kite__get_holdings` |
| Alpha Vantage MCP | Price data only for Indian stocks (BSE format: `RELIANCE.BSE`); full data for US stocks | Via MCP |

---

## Session-end checklist

Before closing every session:
1. Update `docs/TODO.md` (completed items + new backlog)
2. `git push origin main`
3. GitHub Actions auto-deploys HTML to GitHub Pages

---

## Research files reference

All research files are in `research/`. Key ones:
- `research/NEWGEN.md` — Newgen Software (OWNED, Grade B+)
- `research/PATELSAIR.md` — Patels Airtemp (SMALL STARTER, nuclear/HVAC)
- `research/EPACKPEB.md` — EPACK Prefab (OWNED)
- `research/TRANSWORLD.md` — Transworld Shipping (AVOID, Grade D)
- `research/KALYANICASTTECH.md` — Kalyani Cast-Tech (WATCHLIST, Grade C+)
- `research/us/` — US stock research (LIFE/Ethos, etc.)

For the full framework and scoring methodology, read `CLAUDE.md` in the repo root.
