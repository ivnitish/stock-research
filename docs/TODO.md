# Research System — TODO
*Last updated: 2026-03-19*

---

## URGENT — API Key Rotation

- [ ] **Rotate Grok API key** — deprioritized, do later. Delete at https://console.x.ai/account/api-keys and generate new one.

---

## DECIDE THESE NOW (Top 5)

| # | What | Why it matters | Effort |
|---|------|---------------|--------|
| 1 | **Exit PARADEEP immediately** at market price | No recovery scope — competitors (Chambal, Coromandel, RCF) have better Q results + better valuations. Do not wait for bounce. | Low |
| 2 | **Q4 FY26 results watch** — EPACKPEB, KERNEX, ETERNAL | These three are "hold pending result". Need a go/no-go decision in May 2026. | Low (set reminder) |
| 3 | **KAYNES promoter selling** — check BSE filings | 4.3% stake sold in 9 months. Thesis is conditional on this resolving. | Medium |
| 4 | **GROWW trim plan** — 26% of portfolio in a B·19 stock | Expected CAGR only 11%. Trimming above ₹190 and redeploying to ICICIAMC improves portfolio CAGR ~1.5%. | Low (set price alert) |
| 5 | **Kite MCP → XIRR** — connect to get dated order history | Need actual transaction dates to compute real XIRR vs the thesis-estimated 13.5% CAGR. | Medium |

---

## RESEARCH BACKLOG (do when you have time)

- [x] ~~NWIL / IIL~~ = Integrated Industries Ltd — already had thesis, updated status to OWNED (165 shares, +52%)
- [x] ~~Nesco full thesis~~ — DONE. 19/25 Grade B+, Tower 2 catalyst, asset-value undervaluation
- [ ] NVDA Q&A deep dive — Q&A-style research (scale limits, AMD shift, hyperscaler spend motives, bear case ₹42 scenario)
- [ ] Real US positions thesis — RGTI, OKLO, ACHR etc. (all in loss, speculative)
- [ ] STLTECH watch trigger — only revisit if DGTR anti-dumping duty granted

## NEW — AUTORESEARCH BACKTESTING ENGINE

- [ ] **Approach doc:** `docs/AUTORESEARCH_APPROACH.md` — review and answer 7 decision points before implementation
- [ ] Inspired by [karpathy/autoresearch](https://github.com/karpathy/autoresearch) — thesis backtesting + scorecard calibration
- [ ] MVP: backtest 6 core holdings (GROWW, KAYNES, EPACK, KERNEX, SHILCTECH, NESCO) with 1-year lookback

## YOUTUBE TRANSCRIPT PIPELINE (idea)

- [ ] **Auto-pull YouTube transcripts** for stock analysis videos using `youtube-transcript-api` or `yt-dlp --write-auto-sub`
- [ ] Search YouTube API for quality analysis videos per ticker (keywords: "analysis", "deep dive", "thesis", "investor presentation")
- [ ] Extract key insights and add to relevant research files automatically
- [ ] Already used manually for SHILCTECH (Girish Gupta) and EPACKPEB (Aakash Gupta)

## RESEARCH SKILL IDEAS

- [ ] **Q&A research format** — for complex thesis questions (e.g. NVDA: "why do hyperscalers keep spending?", "when does the bear case happen?") — build a `skills/qa-research.md` skill that structures research as Qs with sourced answers
- [ ] Template: Question → Evidence → Counterargument → Our view → Confidence level
- [ ] **Grok API integration** — x.ai's Grok has cheap real-time web access. Evaluate if it can replace some Claude web-search heavy lifting in Q&A research. Pricing vs Claude API cost. Setup: get keys from console.x.ai (needs X account).

## CODE BACKLOG

- [ ] **Grok API integration** — Rotate key first (console.x.ai), then run `python3 src/grok_test.py`. Deprioritized — do when bandwidth available.
- [ ] `red_flag_monitor.py` — add 20+ newer positions (NEWGEN, SAKSOFT, ICICIAMC, tracking stocks)
- [ ] Friend access / Claude API chat widget in index.html
- [ ] Cards view — tracking stocks section missing
- [ ] Weekly digest auto-generator (`src/weekly_digest.py`)

---

## ✅ COMPLETED (2026-03-19 session)

**index.html — major UI update:**
- Added Multibagger potential column (BullTarget/CMP): EPACKPEB 5x+, SWIGGY 4.5x, KERNEX 2.7x, GROWW 2.5x
- Added Margin column (upside % to Fair Value)
- Added valuation tags (Deep Value / Undervalued / Fair / Rich) next to company names
- Renamed "3Y Target" → "Fair Value"
- RAYMOND moved from Grade C → Grade B 16/25, company name fixed from "stub" to "Engineering"
- PARADEEP action → "EXIT NOW — market price"

**RAYMOND Section 4b — Order Book Deep Dive (new):**
- Order book Rs 6,500+ Cr (2.5-3x revenue coverage)
- Customer breakdown: Safran 35-40%, P&W new LTA, GE+RR existing; all 3 OEMs = 88% global market
- 1,200 SKUs across 15 engine programs; qualification→serial transition is key margin lever
- AP plant May 2027; per-unit cost -7-9% post-commissioning

**CONCENTRATION_STRATEGY.md (new):**
- 41 → 10 positions: exit tracking (Move 1), exit Grade C (Move 2), build ICICIAMC 1%→15-20% (Move 3)
- Timeline: PARADEEP this week, SWIGGY limit ₹300, STLNETWORK hard deadline June 30 2026

**GitHub Pages fix:**
- Main repo remote renamed from `origin` → `main-backup` to prevent overwriting HTML repo
- HTML repo force-pushed to restore ivnitish.github.io/stock-research

**YouTube transcript pipeline idea** added to TODO backlog.

---

## ✅ COMPLETED (2026-03-17 session)

**Research updates:**
- PARADEEP: EXIT IMMEDIATELY (no bounce-waiting). Competitors have better quarterly results + valuations.
- SHILCTECH: Full YouTube transcript data (ROE 53%, capacity doubling 7,500→14,000 MVA, strategy insights). Full competitive landscape vs Voltamp/EMCO/ABB/Hitachi Energy.
- NESCO: Full thesis created (19/25 Grade B+). Tower 2 catalyst, asset-value ₹17,000-24,000 Cr vs ₹7,200 Cr market cap.
- INTEGRATEDIND: Status corrected WATCHLIST → OWNED (165 shares, +52%).

**Framework improvements:**
- Peer comparison section added to `_TEMPLATE.md` (5-layer competitive landscape)
- Autoresearch approach doc created (`docs/AUTORESEARCH_APPROACH.md`)

**Housekeeping:**
- Grok API deprioritized to later
- YouTube transcripts added to `data/yt transcripts/`

---

## ✅ COMPLETED (2026-03-14 session — continuing)

**GROWW vs ICICIAMC:** Extracted 900+ line comparison section from index.html → created `research/GROWW_vs_ICICIAMC.md` (allocation analysis, ROE sustainability, valuation, rebalancing rec). Rendered to HTML. Added cross-links in GROWW.md and ICICIAMC.md thesis files. Index now has simple link card instead of embedded content.

**Previous (earlier today):**

**Research:** Valuation framework doc (`docs/VALUATION_FRAMEWORK.md` → `output/html/VALUATION_FRAMEWORK.html`) — DCF + P/B-ROE theory, India assumptions, worked examples (GROWW, JUSTDIAL), when models disagree · Linked in index.html as Reference row · JUSTDIAL deep thesis v2 (investments > market cap SOTP, Q3 FY26 OPM 31%)

**All research docs:** Quick Summary + one-line thesis + Buy/Hold/Sell price table added to all ~20 research files

---

## ✅ COMPLETED (2026-03-13 session)

**Index.html:** Mobile wrapping fix · Section totals (JS) · Expected CAGR section (~13.5% weighted) · ICICIAMC vs GROWW ROE deep dive · P/B formula corrected (g=6%) · STLNETWORK/STLTECH confusion fixed · Nifty 20K scenario page · Full column table (Qty/Avg/CMP/Invested/Current/P&L) · Auth localStorage fix · 23 tracking stocks · Averaging recommendations · Filter buttons

**Research files:** STLNETWORK.md (C·10, owned) · STLTECH.md (C·11, watchlist) · NIFTY20K_WATCHLIST.md · PORTFOLIO_OVERVIEW.md · GROWW.md v2 · ICICIAMC.md · JUSTDIAL.md · SWIGGY.md · ETERNAL.md

**Automation:** Portfolio price update (daily 7pm) · Red flag monitor (weekly Mon 8am) · DCF model · P/B-ROE model · Decision log review (468 trades, -₹64.8K, 6 patterns) · Weekly journal W11
