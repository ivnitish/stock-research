# Research System — TODO
*Last updated: 2026-03-22*

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

## FRAMEWORK — DCF Growth Rate Methodology Fix (IMPORTANT)

**Problem:** Current DCF models use mechanically declining growth rates (e.g. 20%→10%→5% terminal) without grounding them in business reality. This systematically undervalues companies with strong tailwinds, capacity expansions, or historical hypergrowth that is structurally supported.

**SHILCTECH is the clearest example:** DCF bull case = ₹3,596, but CMP already ₹3,727. The DCF said "overvalued" but the business has ROE 53%, capacity doubling 7,500→14,000 MVA by Apr 2027, and India's T&D capex cycle is multi-decade. The model was wrong because the growth rate assumption was wrong.

**The fix — for each stock, growth rates must be anchored to:**

1. **Capacity-constrained revenue ceiling** — if capacity doubles by FY27, revenue physically cannot grow at 10%. Model: (new capacity × utilization rate × ASP) = revenue ceiling. Growth rate is implied, not assumed.
2. **Industry tailwind TAM** — India T&D capex ₹9L Cr by 2032, PM-KUSUM target 35L pumps, aerospace order backlog 13-year supply, etc. If the industry is growing 20%/year, a market-share-gaining company can grow faster. Use this as a floor.
3. **Historical CAGR as a reference point** — if a company grew revenue at 50% CAGR for 3 years, the bear case should be "deceleration to 20-25%", not "collapse to 10%". Deceleration is realistic; reversal to slow growth needs to be justified by specific risks.
4. **Management investments as a signal** — ₹510 Cr capex commitment (RAYMOND AP plant), ₹750 Cr order book (SHILCTECH) → these are forward-looking indicators that management is confident in demand. Factor in.

**Action items:**
- [x] ~~Revise `docs/VALUATION_FRAMEWORK.md`~~ — DONE (2026-03-19). Growth Rate Anchoring section added.
- [x] ~~Re-run SHILCTECH DCF~~ — DONE (2026-03-19). Base ₹2,613→₹4,670, verdict "overvalued"→"25% undervalued".
- [x] ~~Review all DCF models for growth rate anchoring failures~~ — DONE (2026-03-19). Applied to KAYNES, EPACKPEB, KERNEX.
- [ ] **SHAKTIPUMP** — apply TAM-anchored DCF (PM-KUSUM scheme 35L pump target, only 5L done)

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

## ✅ COMPLETED (2026-03-22 session — template v2 rewrites + versioning)

**Research rewrites to new template (5 stocks):**
- RAYMOND.md — v2 rewrite: Summary Verdict, Kill Filter, Compounding Engine Q&A, DCF math. Base ₹530 (+42%)
- NESCO.md — v2 rewrite: Base ₹1,430 (+36%), land value floor, Tower 2 catalyst
- EPACKPEB.md — v2 rewrite: Base ₹260 (+59%), full competitive landscape vs Interarch
- KERNEX.md — v2 rewrite: Major corrections — normalised PAT ₹24 Cr (not ₹50 Cr), DCF base ₹874 (was ₹1,689). Score 18→17
- GRSE.md — v2 rewrite: Full template restructure, incremental ROIC 34%, narrative bull/bear cases

**BANCOINDIA.md** was rewritten earlier this session as the reference implementation.

**Template improvements:**
- Bull/bear case guidance rewritten — emphasizes narrative with numbers woven in, good/bad examples
- Compounding Engine Q&A guidance updated — "explain WHY first, then show the math"
- Version History section added to template

**Research versioning system implemented:**
- `research/archive/` created — stores old versions as `SYMBOL_v1.md`
- All 6 rewritten stocks have v1 archived: BANCOINDIA, RAYMOND, NESCO, EPACKPEB, KERNEX, GRSE
- Each research file has Version History table at bottom linking to older versions
- Future rewrites will follow this pattern automatically

**Feedback captured:**
- Research writing quality: narrative over formula, EPACK bull case as model example
- Saved to memory: `feedback_research_writing_quality.md`

**Pending:**
- [ ] Improve bull/bear narrative quality in RAYMOND, NESCO, EPACKPEB, KERNEX (GRSE done as reference)
- [ ] PARADEEP competitive landscape (Section 6) — carried over
- [ ] HDFCBANK full thesis — carried over

---

## ✅ COMPLETED (2026-03-20 session — GRSE thesis)

**GRSE.md — Full Investment Thesis Created:**
- Data sourced from Screener.in (FY21-FY25 P&L, balance sheet, cash flows, 6 quarters through Dec 2025)
- FY25: Revenue ₹5,076 Cr, PAT ₹527 Cr, OPM 8%, ROCE 37%; TTM PAT ₹689 Cr (Dec 2025)
- 3yr Revenue CAGR 42%, 3yr PAT CAGR 41% — near-zero debt (D/E 0.005x), negative working capital model
- Quality Score: 17/25 Grade B (MOAT 4, Management 3, Financials 4, Growth Runway 4, Valuation 2)
- Full Section 4b (Bear/Base/Bull) capacity-anchored: order book ~₹22,000-25,000 Cr (4.5-5x revenue), capacity ceiling ~₹8,000 Cr at current berths
- DCF: Bear ₹1,420, Base ₹2,650, Bull ₹4,200 vs CMP ₹2,296 — FAIRLY VALUED at base case (7% discount to base)
- P/B-ROE: not appropriate for order-book-driven business; DCF weighted 90%
- Section 6: full peer comparison vs Mazagon Dock (41x PE, 49% ROCE), Cochin Shipyard (50x PE, 20% ROCE), L&T defence, Fincantieri
- Key insight: OPM 8% understates economics — ₹300-350 Cr other income from Navy advance pool adds ~6-7% equivalent OPM; true economics ~14% operating return
- Status: WATCHLIST — fairly priced at CMP; target entry ₹1,800-2,000 or export order catalyst for re-rating
- Rendered to GRSE.html and opened in Chrome

---

## ✅ COMPLETED (2026-03-20 session — PATELSAIR thesis)

**PATELSAIR.md — Full Investment Thesis Created:**
- Data sourced from Screener.in (FY21-FY25 P&L, balance sheet, cash flows, quarterly data through Dec 2025)
- FY25: Revenue ₹388 Cr, PAT ₹17 Cr, OPM 9%, ROCE 14%; FCF ₹39 Cr (exceptional working capital release)
- FY26 slowdown flagged: 9M revenue ~₹163 Cr vs 9M FY25 ₹286 Cr — timing vs structural open question; Q4 FY26 is the key test
- Quality Score: 13/25 Grade C+ (MOAT 2, Management 2, Financials 3, Growth Runway 3, Valuation 3)
- Full Section 4b (Bear/Base/Bull) with capacity-anchor: fixed assets stable at ₹44 Cr, no capex, working capital-driven model
- DCF: Bear ₹250, Base ₹444, Bull ₹868 — CMP ₹219 priced near bear case; base implies 103% upside
- P/B-ROE: bear ₹104, base ₹314, bull ₹628 — stock below book at 0.75x; only makes sense if ROE sustainably <12%
- Section 6: full peer comparison vs ISGEC (20x PE), Thermax (65x PE), HLE Glascoat, GMM Pfaudler + re-rating thesis
- Status: WATCHLIST — wait for Q4 FY26 results (May 2026) to confirm timing vs structural thesis
- Rendered to PATELSAIR.html and opened in Chrome

---

## ✅ COMPLETED (2026-03-19 session — PGEL thesis)

**PGEL.md — Full Investment Thesis Created:**
- Research gathered: Screener data (FY22-FY25 financials + 4 quarterly results), competitor financials (Dixon, Amber, Kaynes, Syrma), industry AC penetration data, capacity expansion plans
- FY25: Revenue ₹4,870 Cr, PAT ₹288 Cr, OPM 10%, ROCE 19.4% — 64% 3Y revenue CAGR
- Q2 FY26 shock documented (PAT –96%, OPM 4.6%) and Q3 FY26 recovery (Rev +46% YoY) analyzed
- Full Section 4b (Bear/Base/Bull FY26-28 with capacity-anchored rationale) completed
- DCF analysis: CMP ₹505 priced in bull case already (bear ₹151, base ₹260, bull ₹449) — stock expensive on DCF
- Section 6 competitive landscape: depth analysis vs Amber, Dixon, Kaynes, Syrma + re-rating thesis
- Status: WATCHLIST — buy below ₹460; strong buy below ₹380 if OPM recovery confirmed
- Quality Score: 16/25 Grade B– (Growth 5/5, MOAT 2/5, Financials 3/5, Management 3/5, Valuation 3/5)
- Rendered to PGEL.html and opened in Chrome

---

## ✅ COMPLETED (2026-03-19 session — continued)

**DCF methodology rollout to 3 stocks:**
- KAYNES: Base ₹1,299→₹1,669 (+28%). Verdict unchanged: genuinely expensive at ₹3,726. OPM recovery (12%→15-16%) is the primary thesis driver. Buy zone updated ₹2,000-2,400. Promoter selling remains key risk.
- EPACKPEB: Base ₹133→₹234 (+76%). Major verdict reversal: "slightly overvalued" → "46% upside at ₹160". India PEB penetration 15% vs 70%+ global + PLI + data centers. Buy below ₹200.
- KERNEX: Base ₹852→₹1,689 (+98%). Largest reversal. 17x order book makes sub-30% growth arithmetically impossible — demand pre-sold 17 years. Bear DCF ₹950 = only -7% from CMP. Risk/reward highly asymmetric.

**Valuation framework commit + push (prior session work):**
- VALUATION_FRAMEWORK.md + SHILCTECH.md committed to main repo

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
- YouTube transcripts added to `data/transcripts/`

---

## ✅ COMPLETED (2026-03-21 session)

**Market Notes:**
- `MARKET_NOTE_MAR2026.html` created — Nifty 25,500 support analysis + HDFC Bank 52-week low setup
- Two Hindi YouTube transcripts (Vivek Singhal / Trading Vivek): Nifty support levels + HDFC Bank panic sell
- HDFC Bank section: 30yr 52W-low pattern, P/B 2.2x vs 10yr median 3.6x, P/E 16.6x vs median 23.6x, RBI governance clearance, record earnings
- index.html: MKT NOTE + HDFCBANK rows added to watchlist table; MKT NOTE card added to cards view
- HDFCBANK added to watchlist as "Watch · Thesis needed"

**Prior session (continuing):**
- SWANDEF.md — full thesis (D·9/25), Compounding Engine Q&A, FV ₹95–665 vs CMP ₹2,057. Verdict: watch only, entry at ₹600–800
- KERNEX.md — Compounding Engine Q&A written (incremental ROIC ~50%, 12-15yr runway, kill condition)
- Google Sheets backend (docs/SHEETS_SETUP.md) — Apps Script + notes widget for all thesis pages
- notes.js + submit.html — created; full thesis submission + per-stock notes widget
- Alpha Vantage MCP added (YUS2XHH8BEO3Y539), Indian stocks: price only (TICKER.BSE)
- Quality Score → Valuation parameter mapping added to VALUATION_FRAMEWORK.md
- _TEMPLATE.md Section 3: "Why Multi-Bagger" → "Compounding Engine Q&A"
- index.html: sticky header fix (overflow-x: clip), column rationalization (Target ₹ / Buy Zone / Upside / CMP/Ref), removed GROWW vs ICICIAMC card

**Continued this session:**
- [x] BSE filing fetcher script (`scripts/fetch_bse_filings.py`) — built and tested end-to-end
  - 20 stocks in PORTFOLIO dict with BSE codes
  - Filters: Results, Annual Report, Investor Presentation, Analyst Meet, concall transcripts
  - Downloads to `data/filings/{SYMBOL}/{YYYYMMDD}_{CATEGORY}_{HEADLINE}.pdf`
  - Usage: `python3 scripts/fetch_bse_filings.py SYMBOL [--days 180] [--list]` or `ALL`
  - KERNEX: 3 PDFs downloaded (Q3 results 4.3MB, JV, order win)
  - RAYMOND: 10 PDFs downloaded (Q3 results 4.1MB, earnings call transcript 636KB, investor pres 3.2MB)
  - 404s expected for older archived files (BSE CDN limitation, not a bug)
- [x] render_plan.py table separator bug fixed — old pattern matched `| |` (empty cell), skipping header rows. All 36 research HTMLs re-rendered.
- [x] _TEMPLATE.md — 4 years + TTM P&L, 6 quarters, Summary Verdict moved to top, Compounding Engine Q&A, correct valuation formula
- [x] RAYMOND.md — full rewrite with Q3 FY26 call data, 17→16/25 corrected, management claims cross-referenced, full Compounding Engine Q&A, Owner Earnings DCF

**Pending:**
- [ ] PARADEEP competitive landscape (Section 6) — Chambal/Coromandel/RCF/Deepak data needed
- [ ] HDFCBANK full thesis — post-merger ROIC, NIM trajectory, loan book quality
- [ ] Google Sheets 5-min setup (user action required — see docs/SHEETS_SETUP.md)

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
