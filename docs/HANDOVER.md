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

**Full framework in:** `CLAUDE.md` — read it before any research session.

---

## Major Framework Updates (Apr 2026)

These were added to `CLAUDE.md` and `research/_TEMPLATE.md` this session — every new research note uses them automatically:

1. **Phase 0.4 — Growth Trigger Scan (Kamayaka Framework):** 6 triggers to identify before entering — Capacity Expansion, Operating Leverage, Margin Expansion, Promoter Buying, Regulatory Tailwind, Turnaround. Entry without a trigger = speculation.

2. **Margin of Safety — explicit required calculation:** MOS = (Base Case − CMP) / Base Case. Asymmetry ratio = upside% / downside%. Ratio >2x = good bet. Required in every Summary Verdict.

3. **Recommendation Decision Matrix — fixes "no buy" bias:**
   - BUY (5-8%): Grade A/B + asymmetry >3x + MOS >20%
   - BUY REDUCED (3-5%): Grade A/B + asymmetry 2-3x
   - TRACKING POSITION (1-2%): Grade A/B + strong thesis + asymmetry 1.5-2x
   - WATCHLIST: price too high, asymmetry <1.5x
   - AVOID: Grade C/D
   - "Interesting, worth watching" is NOT a recommendation — must give specific action + size

4. **Technical Entry Snapshot:** RSI, MFI, price vs SMA 50/200, delivery volume %, key support levels. Fetch from Trendlyne. MFI >80 = near-term pullback risk, phase entry. Use for timing only — not investment decision.

5. **Plain-English explanations (Instruction 10):** Every concept explained as if reader hasn't encountered it. Jargon comes AFTER plain explanation, never instead of it. Test: can you explain the mechanism without the finance term?

6. **First principles grounding (Instruction 9):** Complete this before every BUY: "This company will earn more money in FY[X] because [specific factory/product/contract] causes [revenue/margin] to grow — evidence already in motion: [CWIP/order book/utilization]."

7. **Glossary section in every research file:** Plain-English definitions of all industry-specific terms used in that note.

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
- Be skeptical by default — but be equally willing to say BUY clearly when thesis holds
- **Never ignore announced capex or diversification plans** — these often change the entire thesis
- Add Glossary section at bottom — define all industry-specific terms in plain English

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
| Render single markdown to HTML | `python3 src/render_plan.py FILE.md output/html/` |
| Generate single PDF | Chrome headless — see generate_pdfs.py |

---

## Key files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Full research framework — the multi-bagger methodology (read first) |
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
| `data/transcripts/channel/` | YouTube video syntheses (Kamayaka, etc.) |
| `data/transcripts/SYNTHESIS.md` | Cross-stock synthesis from all concall research |
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

---

## Watchlist — entry conditions

| Stock | Grade | CMP (Apr 26) | Entry Zone | Key condition |
|-------|-------|-------------|-----------|---------------|
| IEX | B (18/25) | ~₹126 | <₹120 (full), <₹130 tracking | Q4 FY26 concall Apr 24 — market coupling risk key; TRACKING POSITION now, add at ₹120 |
| KALYANICASTTECH | B- (15/25) | ~₹665 | <₹450 (full), <₹550 tracking | Wagon revenue H2 FY27; container capacity 16,000 units by FY26 end; 85% utilization confirmed |
| REDINGTON | C (10/25) | ~₹229 | <₹180 | Yield play only; not portfolio mandate |
| MVGJL | C (11/25) | ~₹178 | <₹150 + OCF positive 2Q | OCF negative — wait for cash generation proof |

---

## Recent research completed (Apr 2026)

| Stock | Date | What changed |
|-------|------|-------------|
| KALYANICASTTECH | Apr 21-23 | Major rewrite — Q2 FY26 concall (wagon mfg, RDSO MOU, ₹4,000 Cr vision); competitive data sheet (85% utilization, 16,000 unit expansion); plain-English rewrites; Glossary added; bear case floor revised from -45% to -25% |
| IEX | Apr 21 | New research — Grade B 18/25, market coupling explained, PXIL/HPX context |
| REDINGTON | Apr 21 | New research — Grade C 10/25, Avoid |
| MVGJL | Apr 23 | New research — Grade C 11/25, Avoid; vs Thangamayil comparison |
| TRANSWORLD | Apr 20 | Updated — restructuring not winddown; fleet details; Avana=DP World |

## Learning resources added (Apr 2026)

| File | What it is |
|------|-----------|
| `data/transcripts/channel/Kamayaka_Research_Value_Investing_summary.md` | Structured synthesis — 6 growth triggers, 6 moat types, P/S table, 20+ stock examples, 10 implementation items |
| `data/transcripts/channel/Kamayaka_Research_Value_Investing_clean.md` | Full readable transcript (8,300 words, filler removed, sections added) |
| PDFs for both in `output/pdf/` | Kamayaka_Research_Value_Investing_summary + _clean |

---

## Data sources

| Source | What it provides | How to use |
|--------|-----------------|------------|
| Screener.in | 10yr P&L, balance sheet, ratios, cash flows | WebFetch `screener.in/company/SYMBOL/consolidated` |
| BSE filings | Concall PDFs, quarterly results, annual reports | `python3 src/fetch_bse_filings.py SYMBOL` |
| Trendlyne | Technical analysis — RSI, MFI, SMA, support levels | WebFetch `trendlyne.com/equity/technical-analysis/[BSE_CODE]/[ID]/[SLUG]/` |
| Groww MCP | Live prices, market movers | `mcp__growwmcp__get_ltp` |
| Kite MCP | Live portfolio holdings, P&L | `mcp__kite__get_holdings` |
| Alpha Vantage MCP | Indian: price only (BSE format `RELIANCE.BSE`); US: full data | Via MCP tool |

**Fallback rule:** If Kite MCP fails/is rejected, fetch from Screener.in instead. Never fabricate data.

---

## Research quality standards

- **Narratives over templates:** Bull/bear/compounding sections must read like analyst notes, not slot-filled templates
- **Never ignore capex or diversification:** A company entering a new segment can completely change the thesis — always research and include it
- **Skeptical but decisive:** Find reasons to reject — but if the business survives scrutiny, say BUY clearly with a position size. "Interesting" is not a recommendation
- **Margin of safety required:** Every note must show MOS% and asymmetry ratio (upside/downside). Asymmetry >2x = good bet
- **Plain-English explanations:** Every industry term explained in plain English in the Glossary. Every mechanism explained without jargon first, then the term as shorthand
- **No fabrication:** Never invent stock prices, financial metrics, or portfolio data — even in examples
- **Research log format:** Keep all content. Merge findings into main sections with source references. Most recent first
- **New content at top:** When updating existing research files, add new sections/data ABOVE existing content
- **Archive before rewriting:** Save old version to `research/archive/SYMBOL_v1.md` before major rewrites

---

## Common research pitfalls to avoid

1. **Using TTM revenue as "FY25 revenue"** — always check if audited annual or trailing 12-month
2. **Ignoring OPM compression** — if margins are falling as revenue grows, operating leverage is not working
3. **Taking stated PAT at face value** — check for other income, one-time items, deferred tax
4. **Missing concall capex announcements** — BSE SMEs often announce major expansions only in concalls/AGMs
5. **Over-relying on P/E** — for capital-light businesses (exchanges, software), P/E understates quality; check ROCE and FCF yield
6. **Ignoring working capital deterioration** — expanding debtor days on a growing business can signal collection problems
7. **Promoter stake decline** — always check if secondary sale (bad), ESOP (neutral), or family restructuring (clarify)
8. **Defaulting to WATCHLIST** — if a business is Grade B and asymmetry is 2x+, give it a TRACKING POSITION at minimum

---

## Session-end checklist (mandatory)

Before closing every session:
1. Update `docs/TODO.md` — mark completed, add new discoveries
2. `git push origin main`
3. GitHub Actions auto-deploys HTML to GitHub Pages (~2-3 min)

---

## Research files quick reference

| Symbol | Grade | Status | CMP | Entry | Key thesis |
|--------|-------|--------|-----|-------|-----------|
| NEWGEN | B+ | OWNED | — | ₹447.8 | SaaS ERP compounder, subscription revenue growing 29% YoY |
| EPACKPEB | B | OWNED | — | ₹227.9 | PEB sector leader, capacity doubling, infrastructure tailwind |
| PATELSAIR | B- | SMALL STARTER | — | ₹265 | Nuclear HVAC with ASME stamps, SHANTI Act optionality |
| KAYNES | B | OWNED | — | ₹3,923 | Electronics manufacturing, IoT/ESDM play |
| KERNEX | C+ | OWNED | — | ₹1,125 | Railway signalling, order book dependent |
| BANCOINDIA | — | OWNED | — | ₹589.5 | Deep research pending |
| IEX | B (18/25) | WATCHLIST | ~₹126 | <₹120 | Power exchange, 85% OPM, 85% market share, market coupling risk |
| KALYANICASTTECH | B- (15/25) | WATCHLIST | ~₹665 | <₹450 | Containers (85% util, 16K cap) + wagons (RDSO MOU) + rail terminal |
| MVGJL | C (11/25) | AVOID | ~₹178 | <₹150+OCF | Regional jeweller, negative OCF, FII exit 8%→0.6% |
| TRANSWORLD | D (8/25) | AVOID | ~₹159 | — | Shipping restructuring, vessel arrests, CRISIL watch |
| REDINGTON | C (10/25) | AVOID | ~₹229 | <₹180 | IT distribution, 2% OPM, no moat |

For full framework and scoring methodology: read `CLAUDE.md` in the repo root.
