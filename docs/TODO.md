# Research System — TODO
*Last updated: 2026-04-10*

---

## ✅ COMPLETED — 2026-04-09/10 session

- [x] **Portfolio updated** — Apr 7 holdings file (Excel) used as source of truth. GROWW corrected to 500 shares avg ₹159.91, EPACKPEB to 751 shares avg ₹195.06, GRSE 26 shares, PARADEEP marked sold.
- [x] **Decision Log created** — `docs/DECISION_LOG.md` + rendered HTML + nav tab in index. Entry for Apr 9: exit GRSE/RAYMOND/SWIGGY/STL/ARTEMIS/ETERNAL, concentration to 5-8 stocks.
- [x] **Downside framework** — added to `_TEMPLATE.md` (4-method table: asset floor/balance sheet survival/normalized earnings/strategic value). Applied to RAYMOND thesis.
- [x] **Print CSS** — `@media print` added to `render_plan.py`. Back button hidden on print. All 47 research HTMLs re-rendered.
- [x] **Section anchors + floating TOC** — every research page now has anchor IDs on all headings + a floating "Jump to section" panel. All 47 pages re-rendered.
- [x] **NIFTY valuation page** — `research/NIFTY_VALUATION.md` created: PE band framework (below 16x = buy, 20-22x = fair, above 25x = sell), current reading 21x = fair value. Added to index.
- [x] **ANTELOPUS** — added to watchlist index (Grade C 14/25, Watch <₹450).
- [x] **GRSE** updated — exit confirmed, FY26 TTM ₹6,400 Cr, 8 vessels delivered, NGC policy context, mgmt superannuation flag.
- [x] **RAYMOND** updated — exit confirmed, Q3 FY26 PAT ₹7 Cr, net debt ₹740 Cr (was wrong as net cash — corrected), AP plant/LEAP context, re-entry trigger ₹340.
- [x] **KERNEX** updated — CMP ₹1,109, ₹502 Cr new KAVACH orders (₹91 Cr + ₹411 Cr), BHE 51:49 JV for Moving Block System (major new development), Railway safety policy tailwind.
- [x] **EPACKPEB** updated — CMP ₹177, TTM ₹1,385 Cr, PLI/data centre/China+1 tailwinds section added.
- [x] **NESCO** updated — ₹1,000 Cr FY26 revenue milestone (announced Mar 19), Q2 FY26 PAT ₹119 Cr at 50% margin.
- [x] **LIFE (Ethos)** updated — why rising: Banner Life JV (Mar 24), analyst upgrades (GS $33, Barclays $20), Q1 earnings May 6, lock-up July 2026.
- [x] **India tab fix** — Indian watchlist stocks were invisible under India tab. Fixed by splitting `data-section="watch"` into `watch india` / `watch us`. PATELSAIR, NIFTY_VALUATION, NESCO etc. now visible under India.
- [x] **render_plan.py** — accepts optional output dir arg: `python3 src/render_plan.py foo.md output/html/`

---

## 🔴 NEXT SESSION — TASK BRIEFS FOR NEW AGENT

### Task 1: NEWGEN full research rewrite (HIGHEST PRIORITY)
**Context:** NEWGEN is our core holding (200 shares, ~6% of portfolio). Current file (`research/NEWGEN.md`) is a Quick Summary only — no full template sections. Old version archived at `research/archive/NEWGEN_v1.md`.

**Data already fetched (use this, do NOT re-fetch Screener):**
- CMP ₹457, Market Cap ₹6,496 Cr, P/E 19.9x, P/B 4.1x, ROCE 28%, ROE 22.5%
- 52W Range: ₹401–₹1,379 (-67% from peak, -48% 1Y return)
- D/E ~0, Cash ₹1,000+ Cr, TTM Revenue ~₹1,396 Cr, TTM PAT ₹283 Cr, EPS ₹20
- 5Y Revenue CAGR 19%, 5Y Profit CAGR 34%
- 9M FY26: Revenue ₹1,122 Cr (+6% YoY), PAT adjusted ₹222 Cr (+7% YoY)
- Q3 FY26: Revenue ₹400 Cr, PAT ₹63 Cr (one-time ₹35 Cr labor code hit → adjusted ₹90 Cr)
- Q2 FY26: Revenue ₹401 Cr, PAT ₹82 Cr. Q1 FY26: ₹321 Cr / ₹50 Cr
- Subscription revenue 9M: ₹134 Cr (+29% YoY). Annuity 9M: ₹250 Cr (+20% YoY)
- Revenue split: BFSI 68-71%, Insurance 14%, Govt 7%, EMEA 32%, India 31%, US 21% (+21% YoY), APAC 16%
- Promoter 53.52%, FII 17.34%, FII increasing stake
- Recent wins: Kuwait bank $2.22M, UK pension GBP 3M, Ghana $5.6M, European retail EUR 4.2M
- AI uncertainty causing deal elongation (key risk, management confirmed in Q3 concall Jan 2026)
- Competitors: ServiceNow, Pegasystems, Appian, Oracle BPM
- Q4 FY26 results: May 5, 2026 (critical catalyst — watch for guidance)

**What to write:** Full template rewrite using `research/_TEMPLATE.md`. All 11 sections. Quality Score ~18-19/25. Multi-bagger math: bear 1.9x (15% CAGR/20x exit), base 3.2x (22% CAGR/25x exit), bull 5.2x (30% CAGR/30x exit). Key thesis: rare Indian software product at 20x PE on 34% profit CAGR — market pricing "AI destroys the business" when reality is "AI slows deal cycles temporarily." Subscription revenue 29% growth = SaaS transition underway.

**After writing:** `python3 src/render_plan.py research/NEWGEN.md output/html/` then update `output/html/index.html` entry (currently in grade-b india section), then commit + push.

---

### Task 2: PRESSTONIC research
**Context:** User asked about `https://www.screener.in/company/PRESSTONIC/`. No prior research exists.

**What to do:** Fetch Screener page, run through Phase 0 kill filter checks, quick thesis assessment, write `research/PRESSTONIC.md`, render to HTML, add to index. If Grade C or below with no clear thesis, mark as watchlist/avoid with rationale.

---

### Task 3: Page reorganization
**Context:** User said "I feel like we need to organize our pages — current structure is too confusing." Index has ~50+ entries across mixed sections. Need a proposal first, then implement.

**What to propose:**
- Current sections: Grade A India, Grade B India (3 sub-sections), Owned (tracking), Watchlist (mixed Indian + US), Reference docs
- Problem: watchlist mixes Indian stocks, US stocks, macro docs, journals all in one blob
- Proposed structure: Portfolio (owned) | India Research | US Research | Macro & Reference
- Separate nav tabs for India / US / Macro instead of filter buttons
- Cards view for watchlist (already exists but underused)

**Read `output/html/index.html` current structure before proposing.** Show user the proposal before implementing.

---

### Task 4: Exits to execute
**Context:** Decision Log (Apr 9) flagged these for exit. Need to track execution.

| Stock | Decision | Trigger |
|-------|----------|---------|
| SWIGGY | Exit now | CMP ~₹278, -51% position |
| STLNETWORK | Exit now | CMP ~₹19, -38% position |
| ARTEMISMED | Exit | Grade C, single hospital |
| ETERNAL | Exit on rally | Exit above ₹260 |
| GRSE | Exit | Already above base case |
| RAYMOND | Exit | R/R 1.3:1, too thin |

**What to do:** Check current CMPs, update DECISION_LOG.md with execution status when user confirms exits, update portfolio index with reduced positions. No action needed from agent — this is a reminder for user.

---

### Task 5: BANCOINDIA deep research
**Context:** Grade A 19/25 business (#1 Indian radiator, 32% ROCE, China+1 auto theme). CMP ₹566 is 36% off 52W high ₹880. Already in target portfolio (position 4 in concentration plan). Has research file but may need update. Check `research/BANCOINDIA.md` — if full template exists, just update; if shallow, do full rewrite.

---

### Task 6: RSYSTEMS research (shallow — needs upgrade)
**Context:** `research/RSYSTEMS.md` is a Quick Summary only. Q2 FY26 profit spike was uninvestigated. R Systems is a mid-size IT services company. Check if worth doing full research or marking as exit/avoid.

---

## ACTIVE MONITORING TRIGGERS

| Stock | Trigger | When | Action |
|-------|---------|------|--------|
| ICICIAMC | Price ≤ ₹2,400 | Watch daily | Build to 15-20% of portfolio |
| EPACKPEB | Q4 FY26 revenue ≥ ₹400 Cr | May 2026 results | Add 100 shares |
| EPACKPEB | Price ≤ ₹155 | Watch daily | Add regardless of Q4 |
| NEWGEN | Price ≤ ₹430 | Watch daily | Add meaningfully |
| GRSE | Price ≤ ₹2,000 | After exit | Re-enter |
| RAYMOND | Price ≤ ₹340 | After exit | Re-enter if AP plant on track |
| LIFE (US) | Lock-up expiry July 2026 | July 2026 | Buy dip to $8-10 |
| LIFE (US) | Q1 2026 earnings | May 6, 2026 | Watch for guidance |
| NEWGEN | Q4 FY26 results | May 5, 2026 | Critical catalyst |
| PATELSAIR | Q4 FY26 revenue trend | May 2026 | Confirm timing vs structural |

---

## ⚠️ DECIDE THESE NOW (Top 5)

- [x] **ITC Limited full investment thesis** — Complete analysis with SOTP valuation, post-hotel-demerger assessment, Budget 2026 excise hike impact analysis. Quality Score 19/25 (Grade B), Classification: Quality Compounder. SOTP fair value ₹280-329/share vs CMP ₹293. Recommendation: WATCHLIST, accumulate below ₹270. Key insight: 36.8% ROCE + 3% 10-year stock CAGR = classic value trap, but post-demerger structural improvement may narrow conglomerate discount.
- [x] **NILE Limited full research upgrade** — Upgraded initial screening to complete investment thesis. Key findings: 80-90% customer concentration in Amara Raja (existential risk), Amara Raja backward-integrating with own 150,000 MTPA recycling plant, Grade C quality (10/25), probability-weighted fair value ₹977 vs CMP ₹1,525 — overvalued. Recommendation: AVOID new position, watchlist only.

---

## URGENT — API Key Rotation

- [ ] **Rotate Grok API key** — deprioritized, do later. Delete at https://console.x.ai/account/api-keys and generate new one.

---

## ⚠️ DECIDE THESE NOW

| # | What | Why it matters | Status |
|---|------|---------------|--------|
| 1 | ~~**Exit PARADEEP**~~ | ✅ Already sold — not in Apr 7 holdings | DONE |
| 2 | **Execute exits: SWIGGY, STL, ARTEMIS, ETERNAL** | All decided Apr 9. Capital needed for NEWGEN/ICICIAMC deployment. Don't wait. | ACTION NEEDED |
| 3 | **Execute exits: GRSE, RAYMOND** | Base case already below CMP (GRSE). R/R 1.3:1 (RAYMOND). Both decided Apr 9. | ACTION NEEDED |
| 4 | **Q4 FY26 results watch** — EPACKPEB, KERNEX, NEWGEN | Go/no-go decision in May 2026. Triggers in monitoring table above. | Set reminder |
| 5 | **GROWW trim plan** — still 500 shares, ~7% of portfolio | If above ₹190, trim and redeploy to NEWGEN (add at ₹430) or hold cash for ICICIAMC ₹2,400. | Watch ₹190 |

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
- [x] ~~HDFCBANK full thesis~~ — DONE (2026-03-25). Banking-specific framework (NIM, CASA, P/B-ROE). Post-merger integration + governance crisis analysis.
- [ ] NVDA Q&A deep dive — Q&A-style research (scale limits, AMD shift, hyperscaler spend motives, bear case ₹42 scenario)
- [ ] Real US positions thesis — RGTI, OKLO, ACHR etc. (all in loss, speculative)
- [ ] STLTECH watch trigger — only revisit if DGTR anti-dumping duty granted
- [ ] **KCP Limited** — AGM transcript analysed (2026-03-25). Cement + heavy engg + Vietnam sugar. Rs 978 Cr cash, 75 acres Chennai land, subsidiary for monetization. Interesting value play — needs Screener data for full thesis.
- [x] ~~**GRAB (US: GRAB)**~~ — DONE (2026-04-04). v3 rewrite. 18/25 Grade B+, Multi-Bagger Candidate. Two-gear thesis: core platform leverage + GrabFin re-rating. Base $6.50-7.00 (+75%), buy below $4.50. GRAB vs LIFE comparison added.
- [x] ~~**Ethos Technologies (US: LIFE)**~~ — DONE (2026-04-04). 17/25 Grade B, Multi-Bagger Candidate. InsurTech marketplace, 98% gross margins, only profitable insurtech at scale. IPO'd Jan 2026, down 37% to $11.87. Base $37 (3.1x). Wait for lock-up expiry July 2026 to enter at $8-10.
- [x] ~~**Microsoft (US: MSFT)**~~ — DONE (2026-04-01). Quality Compounder, 20/25 Grade A, $370 CMP at 23x PE (decade low). Base case 2.1x in 5 years. Watchlist — waiting for Q3 FY26 confirmation.
- [ ] **DCIL (Dredging Corp of India)** — 50-year company, ₹1,146 Cr revenue (highest ever), ₹1,400 Cr order book, targeting ₹3,000 Cr. GRSE is shipyard partner. PSU dredging monopoly (80% of India's maintenance dredging).

## SECTOR THESIS — NUCLEAR POWER INDIA

- [ ] **Sector thesis created:** `research/SECTOR_NUCLEAR_INDIA.md` — 100 GW by 2047, ₹14-23 lakh Cr total capex, SHANTI Bill 2025 opens private sector
- [ ] **PATELSAIR** — update thesis with nuclear angle (N-NPT certified, 1 of 3 in India)
- [ ] **Walchandnagar Industries** — Screener data + thesis (legacy DAE partner, 30-40% nuclear revenue)
- [ ] **MTAR Technologies** — Screener data + valuation check (precision nuclear components, typically 50-80x PE)
- [ ] **KSB Ltd** — quick check (only approved supplier for primary coolant pumps)
- [ ] **HCC** — balance sheet check (built 60% of India's nuclear plants, historically debt-heavy)
- [ ] **BHEL** — monitor nuclear turbine order book (₹10,800 Cr order for 6 turbine islands)

## NEW — AUTORESEARCH BACKTESTING ENGINE

- [ ] **Approach doc:** `docs/AUTORESEARCH_APPROACH.md` — review and answer 7 decision points before implementation
- [ ] Inspired by [karpathy/autoresearch](https://github.com/karpathy/autoresearch) — thesis backtesting + scorecard calibration
- [ ] MVP: backtest 6 core holdings (GROWW, KAYNES, EPACK, KERNEX, SHILCTECH, NESCO) with 1-year lookback

## CONCALL DEEP DIVE — TOP 5 STOCKS (PRIORITY)

Gap identified: our research relies too heavily on Screener numbers. Concalls reveal qualitative insights (repeat customer rates, real WC guidance, competitive dynamics, management candor) that numbers miss. EPACK transcript analysis proved this — 6 thesis challenges found that pure number-crunching missed.

**Process:** `fetch_bse_filings.py SYMBOL` → read concall PDFs → extract against standard question set → update research file

Standard questions for every concall:
1. Repeat customer rate / customer stickiness
2. Real working capital guidance (not balance sheet snapshot)
3. Customer concentration (top 5 clients as % of revenue)
4. Segment-wise revenue breakup and growth
5. What did management say about competition?
6. Growth guidance — did they revise it? Up or down?
7. Capex planned and expected return/timeline
8. Any related-party transaction disclosures
9. What risks did analysts ask about?
10. What did management NOT answer or dodge?

| Stock | Filings fetched? | Concall available? | Status |
|---|---|---|---|
| EPACKPEB | YES (7 filings) | YES — Q3 FY26 concall | YouTube done + concall pending |
| RAYMOND | YES (11 filings) | YES — Q3 FY26 transcript | **DONE** — all monitorables met, value unlock timeline pushed out |
| GRSE | YES (10 filings) | YES — Q3 FY26 earnings call | **DONE** — NGC ₹33K Cr step-change, FY28 gap risk flagged |
| NESCO | YES (2 filings) | No concall — Q3 results only | **DONE** — segment data extracted, WSA ₹260 Cr yellow flag |
| KERNEX | YES (7 filings) | No concall — investor pres only | **DONE** — March 2025 pres cross-referenced, TAM 2x (85,000 km) |

## YOUTUBE TRANSCRIPT PIPELINE

**Current workflow (manual):** User provides video links → `yt-dlp --write-auto-sub --skip-download --sub-lang hi,en "URL"` → Claude analyses transcript → findings added to research file

**Already done:** EPACKPEB (4 transcripts analysed, 6 thesis challenges found), SHILCTECH (Girish Gupta)

- [ ] **Install yt-dlp** if not already: `pip install yt-dlp`
- [ ] Build simple script: `src/yt_transcript.py URL` → downloads subs → saves to `data/transcripts/SYMBOL_videoID.txt`
- [ ] Search YouTube API (free tier, needs Google API key) for quality analysis videos per ticker
- [ ] Curate list of trusted Hindi/English stock analysis channels (filter out promotional noise)

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

## ✅ COMPLETED (2026-03-28 session)

**Concall Deep Dives (BSE filing analysis):**
- **KERNEX** — March 2025 investor presentation cross-referenced with thesis. TAM doubled: 85,000 km full network (was 44,000 km). Production capacity quantified: 450 units/month. Bid pipeline ₹4,033 Cr incremental. TCAS 4.0 production-ready (99% software complete). New products (NMS, Pulse Generators, Radio Modems, Drones). Research file updated with 50+ line research log entry.
- **NESCO** — Q3 FY26 standalone results with full segment breakdown. IT Park ₹100 Cr at 83% margin (cash cow confirmed). Foods ₹70 Cr at 13% margin (+106% YoY, OPM diluter). **Yellow flag: Way-Side Amenities segment has ₹260 Cr assets deployed but is loss-making** — capital discipline concern. Research file updated.
- **GRSE** — Q3 FY26 earnings call deep dive (12 Feb 2026). Revenue ₹1,896 Cr (+49% YoY), 9M ₹4,883 Cr (approaching full FY25). NGC ₹33K Cr step-change: order book target ₹50K Cr by FY26-end. New: govt ₹69,725 Cr shipbuilding incentive, 30mm naval guns (no domestic competition), 207 commercial platforms pipeline. FY28 revenue gap risk flagged. Thesis strengthened.
- **RAYMOND** — Q3 FY26 concall deep dive (27 Jan 2026). Aerospace ₹105 Cr (+49%, first >₹100 Cr quarter). Auto EBITDA 13.7% (+330bps, structural). Net cash ₹214 Cr. New: Sinnar plant built Jan 2026, kit value $35K/aircraft, LEAP-1C for COMAC C919. Value unlock timeline pushed out (needs AP plant + tariff stability). All key monitorables met.

**Earlier this session:**
- **EPACKPEB** — cash quality analysis vs Interarch (CFO/PAT comparison, P/B added to peer table, upside/margin-of-safety comparison). EPACK justified P/B 2.67x vs trading at 2.02x (24% undervalued). Interarch at 3.62x vs justified 2.00x (81% overvalued).
- **DREDGECORP** — updated with DCIL Golden Jubilee press release (₹3,000 Cr revenue target, 11 new dredgers, ₹1,400 Cr order book, ₹1,000 Cr rights issue dilution risk). Stock remains overvalued.
- **INTEGRATEDIND / Nurture Well** — deep related-party analysis. Promoter Sanidhya Garg mapped across 7 companies. M.G Metalloy (metals company) received ₹56.5 Cr in warrants as promoter group. 8/10 fraud indicators present — not proof but high concentration. Action: verify FY25 annual report before adding.
- **Nuclear sector thesis** (SECTOR_NUCLEAR_INDIA.md) — created last session, rendered to HTML
- **GRSE** — research log updated with DCIL press release mentioning GRSE as shipyard partner

**Index page audit:**
- 4 missing HTML files added to index.html: SECTOR_NUCLEAR_INDIA, KCP, LOSERS_ANALYSIS, GROWW_vs_ICICIAMC

---

## ✅ COMPLETED (2026-03-25 session)

**Research:**
- KAYNES promoter selling investigation — 12-quarter shareholding trend extracted from Screener. Two discrete block sales (not drip-selling), stopped for 2 quarters, promoter 53.46%. Concern downgraded. Research file updated.
- HDFCBANK full thesis — banking-specific framework (NIM, CASA, P/B-ROE, governance crisis). Post-merger integration analysis with peer comparison.
- KCP Limited AGM transcript (Aug 2025) analysed — cement/heavy engg/Vietnam sugar. Key: Rs 978 Cr cash, 75-acre Chennai land, subsidiary for monetization.

**Code:**
- `red_flag_monitor.py` — added 9 missing positions (ANANTRAJ, ICICIAMC, INTEGRATEDIND, NEWGEN, RSYSTEMS, SAKSOFT, RAYMOND, NESCO, SHAKTIPUMP). Fixed STLNETWORK ticker (was STLTECH.NS showing +477%, now STLNETWORK.NS showing -42% correctly). Fixed INTEGRATEDIND ticker (.NS→.BO). Updated stale scores (BANCOINDIA 0→19, SHILCTECH 0→18, KERNEX 18→17). Now monitors 24 holdings.
- PORTFOLIO_OVERVIEW.md — fixed RAYMOND (C·11→B·17), STL ticker, PARADEEP action (→EXIT NOW), scores for BANCOINDIA/SHILCTECH/KERNEX.

**Pending:**
- [ ] KCP full thesis if user interested
- [ ] Bull/bear narrative improvements on RAYMOND/NESCO/EPACKPEB/KERNEX (marginal — current versions already strong)

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
