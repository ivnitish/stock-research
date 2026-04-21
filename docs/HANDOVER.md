# Stock Research System — New Chat Handover

*Read this at the start of every new Claude Code session in `/Users/nitish/stocks automation/`.*

---

## What this system is

A personal equity research pipeline built for Munger-style fundamental analysis. Research notes are written in Markdown, rendered to HTML (live on GitHub Pages), and exported as PDFs with portfolio data hidden (safe to share). The goal is finding multi-baggers — businesses that can compound intrinsic value at 20%+ CAGR for 7-15 years.

**GitHub Pages (live site):** ivnitish.github.io/stocks  
**Working directory:** `/Users/nitish/stocks automation/`  
**Model preference:** Claude Opus (claude-opus-4-6) — always use this for deep analysis  
**User background:** Munger/Buffett philosophy, CFA Level 1. Explain unfamiliar concepts with examples. Never dumb down but always clarify jargon.

---

## The Investment Framework

Every research note evaluates 5 dimensions (5 points each, 25 max):
1. **MOAT** — switching costs, network effects, pricing power, scale advantages
2. **MANAGEMENT** — promoter skin in game, capital allocation, communication quality
3. **FINANCIALS** — ROCE, ROE, OCF vs PAT, D/E, FCF, working capital trends
4. **GROWTH RUNWAY** — TAM headroom, reinvestment rate, runway duration
5. **VALUATION** — fair P/E vs current P/E, margin of safety, multi-bagger math

**Grade:** A=20-25 (multi-bagger candidate), B=15-19 (quality compounder), C=10-14 (watchlist/speculative), D=<10 (avoid/exit)

**Core insight:** A stock's return = EPS growth + P/E re-rating. EPS growth = ROIC × reinvestment rate, sustained over a long runway. Everything in the analysis connects back to this.

---

## Workflow: When user says "do research on [STOCK]"

### Step 1 — Fetch data (do both)
```bash
python3 src/fetch_bse_filings.py SYMBOL        # downloads BSE filings to data/filings/SYMBOL/
```
WebFetch: `https://www.screener.in/company/SYMBOL/consolidated/`

For BSE SME stocks: use BSE code directly — `screener.in/company/544023/`

### Step 2 — Deep research before writing
Before writing a single line of the thesis, extract:
- 10-year P&L trend (revenue CAGR, OPM trajectory, PAT CAGR)
- ROCE, ROE (3yr and 5yr averages)
- Cash flow quality: OCF vs PAT ratio (should be >0.8x consistently)
- Balance sheet: D/E trend, fixed assets, working capital days
- Shareholding: promoter % and direction, FII/DII trend
- Segment/geography revenue breakdown (what drives the business?)
- Management: concall commentary, guidance accuracy, capex plans
- Competitors: market share trend, who is gaining/losing
- Key risks: regulatory, cyclical, competitive, governance
- **Capex and diversification plans** — critical for SMEs; new business lines change the thesis entirely

### Step 3 — Go deeper before concluding
For any non-obvious finding, dig further:
- If OCF is volatile → why? Working capital build or revenue lumpiness?
- If promoter declining → check if secondary sale, ESOP, or restructuring
- If margins compressing → product mix, input costs, or pricing pressure?
- If revenue tripled in 3 years → organic? Acquisitions? New segment?
- **If company mentions new capex** → what's the segment, capacity target, timeline, revenue potential?
- Fetch concall transcripts: `python3 src/fetch_bse_filings.py SYMBOL` then read PDFs in `data/filings/SYMBOL/`
- Check BSE announcements for any recent material disclosures

### Step 4 — Write the research file
Use `research/_TEMPLATE.md` as structure. Key rules:
- Write narratively — not template slot-filling. Bull/bear should read like analyst notes
- Show math: ROIC = numerator/denominator spelled out
- Label opinions vs facts explicitly
- Be skeptical by default — the base rate for multi-baggers is low
- **Never ignore announced capex or diversification plans** — these often change the entire thesis

Output to: `research/SYMBOL.md`

### Step 5 — Render, PDF, index, push
```bash
python3 src/render_all.py SYMBOL   # renders HTML + generates PDF
open output/html/SYMBOL.html       # review in Chrome
```
Then update `output/html/index.html` (add row — see rules in `.claude/rules/index-always.md`)
```bash
git push origin main
```

---

## Key commands

| Task | Command |
|------|---------|
| Research a stock (render + PDF) | `python3 src/render_all.py SYMBOL` |
| Rebuild all HTML + all PDFs | `python3 src/render_all.py` |
| Rebuild HTML only (no PDF, faster) | `python3 src/render_all.py --no-pdf` |
| Generate PDFs only | `python3 src/generate_pdfs.py` or `...SYMBOL` |
| Fetch BSE filings | `python3 src/fetch_bse_filings.py SYMBOL` |
| Push to GitHub | `git push origin main` |
| Open index in browser | `open output/html/index.html` |
| Open PDF folder | `open output/pdf/` |

---

## Key files

| File | Purpose |
|------|---------|
| `research/_TEMPLATE.md` | Master research template — always use this |
| `research/SYMBOL.md` | Individual stock research (source of truth) |
| `research/archive/SYMBOL_v1.md` | Old versions before rewrites |
| `research/us/SYMBOL.md` | US stock research |
| `output/html/SYMBOL.html` | Rendered HTML (auto-generated, never edit) |
| `output/pdf/SYMBOL_DATE.pdf` | Shareable PDFs (portfolio data hidden) |
| `output/html/index.html` | Live homepage — update after every new stock |
| `docs/TODO.md` | Active tasks and backlog |
| `docs/DECISION_LOG.md` | All buy/sell decisions with reasoning |
| `docs/HANDOVER.md` | This file |
| `portfolio.csv` | Holdings: symbol, qty, avg_buy_price |
| `data/filings/SYMBOL/` | Downloaded BSE PDFs (concalls, results, AR) |
| `data/transcripts/` | Concall summaries and channel video notes |
| `data/transcripts/SYNTHESIS.md` | Cross-stock synthesis from all concall research |
| `CLAUDE.md` | Full research framework — the multi-bagger methodology |
| `src/render_plan.py` | Markdown → HTML renderer (handles PRIVATE blocks) |
| `src/render_all.py` | Batch render all + generate PDFs |
| `src/generate_pdfs.py` | Chrome headless PDF generator |

---

## Private data in PDFs

Portfolio data is visible in browser, hidden in PDFs — safe to share with anyone.

**How it works:**
- Wrap private content in `<!-- PRIVATE -->...<!-- /PRIVATE -->` in markdown
- Lines with `**Entry:**` or `**P&L:**` are auto-wrapped as private
- "Decision History" section is auto-wrapped as private
- HTML renders these with yellow tint (visible to you in browser)
- PDFs hide them completely via `@media print { display: none }`

---

## Active portfolio (as of Apr 2026)

| Symbol | Status | Qty | Avg | Key trigger |
|--------|--------|-----|-----|-------------|
| NEWGEN | HOLD | 200 | ₹447.8 | Q4 FY26 results May 5, 2026 |
| PATELSAIR | SMALL STARTER | 1 | ₹265 | Nuclear order flow watch |
| EPACKPEB | HOLD | 451 | ₹227.9 | Capacity ramp FY27 |
| KAYNES | HOLD | 31 | ₹3,923 | — |
| KERNEX | HOLD | 90 | ₹1,125 | — |
| STLNETWORK | HOLD | 1,500 | ₹31.2 | — |
| BANCOINDIA | HOLD | 100 | ₹589.5 | Deep research pending |
| Others | See `portfolio.csv` | — | — | — |

**Pending exits to decide:** SWIGGY, STL, ARTEMIS, ETERNAL, GRSE, RAYMOND (see TODO.md)

**Watchlist (do not enter yet):**
- IEX: Grade B, below ₹120, watch Apr 24 concall (market coupling risk)
- KALYANICASTTECH: Grade C+, below ₹400, wagon manufacturing capex changes thesis
- REDINGTON: Grade C, below ₹180 (yield play only)

---

## Data sources

| Source | What it provides | How to use |
|--------|-----------------|------------|
| Screener.in | 10yr P&L, balance sheet, ratios, cash flows | WebFetch `screener.in/company/SYMBOL/consolidated` |
| BSE filings | Concall PDFs, quarterly results, annual reports | `python3 src/fetch_bse_filings.py SYMBOL` |
| Groww MCP | Live prices, market movers | `mcp__growwmcp__get_ltp` |
| Kite MCP | Live portfolio holdings, P&L | `mcp__kite__get_holdings` |
| Alpha Vantage MCP | Indian: price only (BSE format `RELIANCE.BSE`); US: full data | Via MCP tool |

**Fallback rule:** If Kite MCP fails/is rejected, fetch from Screener.in instead. Never fabricate data.

---

## Research quality standards

- **Narratives over templates:** Bull/bear/compounding sections must read like analyst notes, not slot-filled templates
- **Never ignore capex or diversification:** A company entering a new segment (e.g., castings → wagon manufacturing) can completely change the thesis — always research and include it
- **Skeptical by default:** Your job is to find reasons to REJECT a thesis; if it survives skepticism, that's a meaningful signal
- **No fabrication:** Never invent stock prices, financial metrics, or portfolio data — even in examples. If data is unavailable, say so
- **Research log format:** 15-20 lines max per entry. Merge key findings into main sections with source references
- **New content at top:** When updating existing research files, add new sections/data ABOVE existing content (newest first)
- **Archive before rewriting:** Save old version to `research/archive/SYMBOL_v1.md` before major rewrites

---

## Common research pitfalls to avoid

1. **Using TTM revenue as "FY25 revenue"** — always check if audited annual or trailing 12-month
2. **Ignoring OPM compression** — if margins are falling as revenue grows, operating leverage is not working
3. **Taking stated PAT at face value** — check for other income, one-time items, deferred tax
4. **Missing concall capex announcements** — BSE SMEs often announce major expansions only in concalls/AGMs
5. **Over-relying on P/E** — for capital-light businesses (exchanges, software), P/E understates quality; check ROCE and FCF yield
6. **Ignoring working capital deterioration** — expanding debtor days on a growing business can signal collection problems or channel stuffing
7. **Promoter stake decline** — always check if secondary sale (bad), ESOP (neutral), or family restructuring (clarify)

---

## Session-end checklist (mandatory)

Before closing every session:
1. Update `docs/TODO.md` — mark completed, add new discoveries
2. `git push origin main`
3. GitHub Actions auto-deploys HTML to GitHub Pages (~2-3 min)

---

## Research files quick reference

| Symbol | Grade | Status | Key thesis |
|--------|-------|--------|-----------|
| NEWGEN | B+ | OWNED | SaaS ERP compounder, subscription revenue growing 29% YoY |
| EPACKPEB | B | OWNED | PEB sector leader, capacity doubling, infrastructure tailwind |
| PATELSAIR | B- | SMALL STARTER | Nuclear HVAC with ASME stamps, SHANTI Act optionality |
| KAYNES | B | OWNED | Electronics manufacturing, IoT/ESDM play |
| KERNEX | C+ | OWNED | Railway signalling, order book dependent |
| BANCOINDIA | — | OWNED | Deep research pending |
| IEX | B | WATCHLIST | Power exchange, 85% OPM, market coupling risk |
| KALYANICASTTECH | C+ | WATCHLIST | Castings + containers + wagon mfg capex (BSE SME) |
| TRANSWORLD | D | AVOID | Shipping restructuring, losses deepening |
| REDINGTON | C | AVOID | IT distribution, 2% OPM, no moat |
| PATELSAIR | B | WATCHLIST | Nuclear HVAC certifications, SHANTI Act |

For full framework and scoring methodology: read `CLAUDE.md` in the repo root.
