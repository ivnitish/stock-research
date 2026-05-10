# Research System — TODO
*Last updated: 2026-05-09*

---

## ✅ Completed — 2026-05-09

- **NCDEX pre-IPO watch note** — `research/NCDEX.md`. Grade D 8/25, status UNLISTED / PRE-IPO WATCH. FY25 op revenue ₹88 Cr (4-yr decline), unlisted ₹378-384, mcap ₹3,444 Cr, P/B 4.6x. Daily turnover collapsed from ₹2,310 Cr to ₹300-400 Cr after Dec 2021 SEBI ban on 7 agri contracts. ₹770 Cr fresh capital raised; equity & MF approvals received but not built. Recommendation: Avoid IPO, watch ban-lift.
- **MSEI pre-IPO watch note** — `research/MSEI.md`. Grade D 9/25, status UNLISTED / PRE-IPO WATCH. FY25 revenue ₹17.4 Cr / op revenue ₹5.4 Cr, net loss ₹34.2 Cr, ₹1,240 Cr recapitalization (Peak XV / Rainmatter / Billionbrains / Share India / Jainam / Monarch / Trust). Unlisted ₹6, mcap ₹6,688 Cr, P/B 22.7x. LES launched Jan 27, 2026 covering 130 stocks (₹40 lakh/month/MM, runs through Jun 30, 2026). Recommendation: Watch until daily turnover sustains >₹100 Cr equity cash for 2 months.
- **ADOR research note** — `research/ADOR.md`. Grade B 16/25, Tracking position. CMP ₹1,078, mcap ₹1,877 Cr, P/E 22.3x, P/B 3.37x. FY26 PAT ₹82 Cr (+37%) on revenue ₹1,140 Cr (flat). Margin recovery story — Q1 -2% OPM → Q4 14.79% OPM (PAT +89% YoY). Capex visible (FA ₹117 Cr → ₹204 Cr) but topline decoupled — needs FY27-28 absorption. Promoter -3.14% in FY25 = Pattern 10 yellow flag. Add criteria: 2 of 3 (promoter stable, OPM ≥13% × 2Q, revenue YoY ≥10% × 2Q).
- **Framework appendices added** — Voice-compliant additions to `learnings/multibagger_patterns.md` (Pattern 9 margins-through-trough, Pattern 10 no-insider-distribution-at-bottom, kill signals), `CLAUDE.md` (Phase 0.5 Pre-existing capability, Phase 4.5.3 Margin behaviour through stress, Phase 4.5.4 Market label vs reality), `SKILL.md` (Step 2.5 Segment & insider depth pull, Step 6 checklist additions), `_TEMPLATE.md` (Universal market-label-vs-reality table). Appended as APPENDIX sections to preserve current flow; promote to main phases after they've earned their place.
- **Task #8 — Holdings table wired to portfolio.csv** — `src/sync_holdings_from_csv.py`. Reads `data/portfolio.csv` as source of truth, updates qty/avg/invested + derived (Δ/share, current, P&L abs/%) on existing index.html stock rows by onclick handler. Right-to-left position-based replacement so identical "—" cells don't collide. Idempotent. Reports CSV symbols missing HTML rows (6: ATHERENERG, BHEL, NWIL, PATELSAI, SOUTHWEST, ZENTEC). Notable corrections applied: EPACKPEB 751 → 1,451; ARTEMISMED 181 → 362; RAYMOND "0 (exited)" → 300 (re-entered); NESCO 1 → 20.

## Open (next session)

- Triage rows for ATHERENERG, BHEL, NWIL, PATELSAI, SOUTHWEST, ZENTEC — rows already exist in index.html and now sync from CSV; each still needs a research note + grade + onclick handler. Currently linked: NWIL→INTEGRATEDIND.html (parent company).
- Review whether to promote framework appendices into main phases (Phase 0.5, 4.5.3, 4.5.4 in CLAUDE.md; Step 2.5 in SKILL.md; market-label table in _TEMPLATE.md). Currently sitting as APPENDIX sections.
- Review NESCO classification (tagged "Monitor · Exhibition+IT" in tracking section but holdings now show 20 shares — real position).
- Review RAYMOND classification (still "Watch · Re-buy <₹380" in watch section; CSV shows 300 held).
- Wire CMP refresh from Groww MCP into sync script (currently leaves CMP cell untouched, derives Δ/PL from existing CMP).

### New research candidates (queued)

- **MEIL** — Mangal Electrical Industries Ltd (BSE: 544492, NSE: MEIL). Transformer components / electrical capital goods. CMP ₹342, mcap ₹944 Cr, P/E 21.3, P/B 1.68, ROE 34.1%, ROCE 30.4%, 5y profit CAGR 74%. Source: https://www.screener.in/company/MEIL/. Initial read: high-quality returns at fair P/B; 5y profit CAGR 74% needs a sustainability check (base effect or genuine compounding?). Queued 2026-05-10.

---

## ✅ Completed — 2026-05-04

- **Multi-bagger pattern study series complete (4 new studies):**
  - `research/learnings/multibagger_BAF.md` — Bajaj Finance (2010-11 bottom, ~100x). Consumer NBFC pivot thesis: Rajeev Jain from GE/AmEx + Nanoo Pamnani advisory, 12% NPA root cause fixed (600-borrower-profile underwriting), zero-cost EMI generating 20-25% internal yield hidden below headline P&L, India credit-to-GDP secular tailwind. PAT CAGR 35% sustained over 12 years.
  - `research/learnings/multibagger_TITAN.md` — Titan Company (2002-03 bottom, ~150x). Tanishq segment growing 29% to ₹345 Cr with positive PBIT, buried under consolidated -55% PAT. 18-carat failure already replaced by 22-carat + Karatmeter model by 2000; market still pricing the old failure in 2002-03. Jhunjhunwala entry at ₹3-6. Organized jewelry at 6% of ₹45,000 Cr TAM.
  - `research/learnings/multibagger_PAGE.md` — Page Industries (2008-09 bottom, ~80x). Stock -50% while EPS +80% in same year. Exclusive 50-year Jockey license renewed in 2008. Genomal family 50-year Philippines track record. 65% unbranded innerwear market. ROE 35-40% through the crisis, OPM stable at 20-21%.
  - `research/learnings/multibagger_APLAPOLLO.md` — APL Apollo Tubes (2014-15 bottom, ~30x). #1 organized player (55% structural hollow sections) in 50%-unorganized market. ₹250 Cr capex cycle causing flat PAT despite 42% revenue growth — market read as no earnings power; FY2017 showed 184% PAT jump. GST (2017) eliminated unorganized tax-evasion cost advantage.
- **Pattern synthesis complete:** `research/learnings/multibagger_patterns.md` — 8 patterns, all with 4+/5 occurrence rate. Top 5 (universal, 5/5): underpenetrated TAM, first-mover position, price-business disconnect, bear case right about symptom wrong about root cause, structural regulatory tailwind. Plus 3 at 4/5: segment masking, domain-specific management prior, adequate balance sheet.
- **Framework distillation (Block C):**
  - `CLAUDE.md` Phase 0.4: Added "Consolidation Trigger" (organized share <40% + pending regulatory equalizer) and "Price-Business Disconnect" as named triggers
  - `CLAUDE.md` Phase 1.1: Added segment-level ROIC rule — always compute organized-only market share + segment revenue CAGR separately from consolidated
  - `CLAUDE.md` Phase 4.3→4.4: Added Phase 4.4 "Domain-Specific Prior Track Record" — prior domain expertise in same business/geography is stronger predictor than current company results
  - `SKILL.md` Step 6: Added Multi-Bagger Pattern checklist (6 new items: organized share sub-segment, regulatory equalizer, segment CAGR, bear case root cause test, capex cycle ROIC verification, operator domain experience)
  - `_TEMPLATE.md` Stress Test section: Added "What was true at the bottom" table for turnaround/inflection theses — forces separation of what market is pricing vs what segment data shows vs whether root cause is still present
- **Index.html:** Added 6 rows (MULTIBAGGER patterns doc + 5 study rows: BSE, BAF, TITAN, PAGE, APL)

## Open (next session)

- NCDEX research note (Block F)
- Metropolitan Stock Exchange (MSE) research note (Block F)
- Ador Welding research note — screener.in/company/ADOR (Block F)
- Wire index.html holdings table to data/portfolio.csv (Task #8 — Block D)

---

## ✅ Completed — 2026-05-03

- **Holdings refresh** — `data/portfolio.csv` updated from Groww broker export (03-May-2026). STLNETWORK: 1500 shares → 1 share (sold down to tracking stub)
- **index.html STLNETWORK row** updated to "Exited 02-May-26 (1-share stub)"
- **BSE multi-bagger study** — `research/learnings/multibagger_BSE.md`. ~119x return. Pattern: fortress balance sheet + dormant SME platform + latent derivatives optionality priced at zero.

---

## ✅ Completed — 2026-05-02

- **PROTEAN research note** — `research/PROTEAN.md`. Mid-depth analyst note on Protean eGov Technologies. CMP ₹530, down ~63% from 52w high after PAN 2.0 contract loss (May 2025). Debt-free utility at P/B 2.11, but 5y sales CAGR 3% and DII holding collapsed from 41% → 21% in two years. Verdict: watchlist, not buy. Look for two clean quarters of 15%+ growth from non-PAN lines, ₹50 Cr+ quarterly from ONDC/AA, DIIs stabilising. Index.html updated with watchlist entry (Grade C, watch <₹450, target ₹700).
- **MANUGRAPH research note** — `research/MANUGRAPH.md`. Mid-depth note on Manugraph India (₹42 Cr mcap micro-cap). Trades at 0.43x book, debt-free, promoter at 57.67% stable, Q3 FY26 first profitable quarter in years. But newspaper press industry in 20-year structural decline, FY17 ₹35 Cr loss = Manugraph Americas / DGM Chapter 11 bankruptcy, Carraro packaging diversification 7yrs old still small. Includes decade P&L, balance sheet evolution, working capital chaos (inventory days peaked at 1,033 in FY21). Verdict: speculative deep-value ticket, half-percent position max. Index.html updated.
- **Framework: Voice Guide added to template + writing-quality rule** — `_TEMPLATE.md` and `.claude/rules/writing-quality.md` updated with explicit anti-patterns (no LLM-template scaffolding like "the bull case is", no editorial one-liners like "cheap and stagnant is a trap, not an opportunity", no list-as-sentence comma strings, no preambles). Concrete reference paragraph from Protean verdict embedded as the voice anchor. Voice pass step required before finalising any research file.
- **Framework: Phase 4.5 Second-Order Stress Test added across template + SKILL + CLAUDE** — All three files now require a 5-Whys drill on the ROIC engine (descriptive answer at level 1 → systemic cause at level 5; structural answer = durable moat, company-controlled = fragile) and a base-case world-state at 2 and 5 years (revenue/margin profile, management agenda, what new risks success itself triggers — competition entering, regulatory attention, capital allocation pressure once cash flows). New section in `_TEMPLATE.md` Summary Verdict between "What does the market think" and "Multi-Bagger Math". New Step 3D in `SKILL.md` with checklist item. New `## PHASE 4.5` in `CLAUDE.md` between Phase 4 and Phase 5.

## ✅ Completed — 2026-04-27

- **RAYMOND research refresh + structural cleanup** — `research/RAYMOND.md` v2.2.
  Stock rallied to ₹461 (+25.6% from ₹367 at Apr 9 exit decision). Refreshed CMP/
  market cap/EV/asymmetry math. At ₹461, base case ₹530 = +15% upside vs bear ₹240
  = −48% downside → asymmetry 0.31x, fails Grade B threshold. EXIT call vindicated;
  capital redeployed to NEWGEN earned the gap as alpha. Re-entry framework: buy
  back <₹380 OR <₹420 if Q4 FY26 prints aerospace ≥₹110 Cr at ≥20% margin.
  **Structural fixes:** renamed duplicate `## 4b. Outlook` → `### 4h.` (was conflict
  with `### 4b. Engineering Segment Actuals`); renumbered duplicate `### 5.2 Margin
  of Safety` → `### 5.3` (was conflict with `### 5.2 DCF Calculation`); shifted
  Position Sizing → 5.4, SoTP → 5.5. Reconciled header EXIT vs body HOLD/ADD
  contradiction. Updated Decision History with exit row, Version History to v2.2,
  Review Schedule with Q4 board meeting note (Apr 22 newspaper publication filed).
  Index.html updated: Raymond moved Grade B holdings → watchlist with "Re-buy <₹380"
  action tag and "Fairly Valued" classification.
- **MCP status check** — Kite MCP session expired (need `mcp__kite__login`); Groww
  MCP configured in `~/.claude.json` as `growwmcp` but no `mcp__growwmcp__*` tools
  exposed in this session — server failing to register. Needs `claude mcp list`
  diagnostics from repo dir.

- **ADISOFT IPO analysis** — DRHP-based research note `research/ADISOFT.md`. Adisoft
  Technologies Ltd (SME IPO, NSE EMERGE), industrial automation integrator,
  Pune-based, FY25 revenue ₹131.7 Cr, PAT ₹16.1 Cr, reported RoCE 29% / RoE 39%.
  **Decision: AVOID at any plausible band — Grade D (8/25).**
  Phase 0 fails: top customer 48.48% of revenue, 78.61% auto-sector concentration,
  negative OCF for FY24 + FY25 despite rising PAT, trade receivables ~4x in 2 years,
  pre-IPO 1,200:1 bonus issue (Sep 5, 2025), partnership-to-public-limited
  conversion only Sep 11, 2025, restated financials by non-statutory auditor,
  no ISO/IATF certification, all premises rented, unregistered trademarks,
  no listed-co experience among directors. Sole listed peer Patil Automation
  at 27.28x P/E provides soft cap; even at SME-discount band, asymmetry <1x.
  Rendered to HTML; index.html updated with Adisoft in watchlist (Grade D · Avoid).

---

## ✅ Completed — 2026-04-26

- **ABB India full research** — written `research/ABB.md` from CY25 concall + investor presentation
  + Q4 CY25 concall + Q3 CY25 concall PDFs. Grade B (18/25), WATCHLIST at CMP ₹7,328.
  Multi-bagger math: Bear ₹4,060 / Base ₹9,000 / Bull ₹14,300 (5-year horizon).
  Buy zone ₹4,500-5,500 where asymmetry rises to 6-10x. Active triggers: Capacity
  Expansion + Regulatory Tailwind (India-EU FTA, Budget 26-27).

- **63MOONS full research** — written `research/63MOONS.md` driven by 63SATS Cybertech
  FY26 Investor Update PDF. Grade C (10/25), SPECULATIVE WATCHLIST at CMP ₹683.
  Trades at 0.9x book with embedded optionality on 63SATS subsidiary
  (FY26 ₹87 Cr → FY27 target ₹350 Cr revenue). Governance overhang: NSEL legacy,
  Feb 2026 NSE/BSE warning. Asymmetry 0.5x at CMP — only buy on price <₹500
  AND clean Q1 FY27 print. Position size: 1% MAX.

- Both files rendered to HTML + PDF (via `src/render_all.py`); index.html updated
  with both entries in watchlist section.

---

## 🔴 NEXT — ACTIVE TASK BRIEFS

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

### Task 6: GitHub Pages — Shareable Research (viewer mode)
**Context:** User wants to share stock research pages with friends without exposing portfolio data.

**What we know:**
- Current site: all pages gated behind auth (nitish/stocks2026)
- Problem: sharing password gives friends access to everything including portfolio positions, buy prices, private notes
- User wants: share index (stock list) + individual research pages, but hide portfolio-specific data
- Back button should still work (friends navigate index → research → back to index)

**Constraints:**
- Must be built and tested on a **git branch** before merging to main
- Branch name: `feature/viewer-mode`

**Likely implementation:**
- Two-role auth in `auth.js`: owner (full access) + viewer (research only)
- `<!-- PRIVATE -->` convention in markdown → rendered as hidden blocks for viewers
- Index: hide portfolio columns (position size, cost basis, P&L) for viewers; show stock list + grades + links
- Research pages: hide status/position/buy price blocks for viewers; back button works for all

**Do NOT start until user finishes explaining the full requirement.**

---

### Task 7: RSYSTEMS research (shallow — needs upgrade)
**Context:** `research/RSYSTEMS.md` is a Quick Summary only. Q2 FY26 profit spike was uninvestigated. R Systems is a mid-size IT services company. Check if worth doing full research or marking as exit/avoid.

---

### Task 8: MF Sector Allocation Tracker
**Context:** Mutual fund monthly portfolio disclosures (AMFI) reveal which sectors smart money is increasing/decreasing.

**What to build:**
- Fetch AMFI monthly disclosures or use Trendlyne/Tijori data
- Track sector allocation % changes over 3-6 quarters for top 10-15 AMFs
- Flag sectors with >2% aggregate increase as "MF accumulation" — cross-reference with our watchlist
- Monthly cron job → `data/mf_sector_flows.csv`

---

### Task 9: Historical Multibagger Analysis
**Background agent task.** `research/MULTIBAGGER_PATTERNS.md` — what % of return came from earnings growth vs P/E re-rating? Stock list: Kaynes, KERNEX, Cochin Shipyard, Dixon, CAMS, APL Apollo, Polycab, DMart, PI Industries, Astral, Bajaj Finance.

---

## ACTIVE MONITORING TRIGGERS

| Stock | Trigger | When | Action |
|-------|---------|------|--------|
| ICICIAMC | Price ≤ ₹2,400 | Watch daily | Build to 15-20% of portfolio |
| EPACKPEB | Q4 FY26 revenue ≥ ₹400 Cr | May 2026 results | Add 100 shares |
| EPACKPEB | Price ≤ ₹155 | Watch daily | Add regardless of Q4 |
| NEWGEN | Price ≤ ₹430 | Watch daily | Add meaningfully |
| NEWGEN | Q4 FY26 results | May 5, 2026 | Critical catalyst |
| GRSE | Price ≤ ₹2,000 | After exit | Re-enter |
| RAYMOND | Price ≤ ₹340 | After exit | Re-enter if AP plant on track |
| LIFE (US) | Lock-up expiry July 2026 | July 2026 | Buy dip to $8-10 |
| LIFE (US) | Q1 2026 earnings | May 6, 2026 | Watch for guidance |
| PATELSAIR | Q4 FY26 revenue trend | May 2026 | Confirm timing vs structural |

---

## ⚠️ PENDING DECISIONS

| # | What | Why it matters | Status |
|---|------|---------------|--------|
| 1 | **Execute exits: SWIGGY, STL, ARTEMIS, ETERNAL** | All decided Apr 9. Capital needed for NEWGEN/ICICIAMC. Don't wait. | ACTION NEEDED |
| 2 | **Execute exits: GRSE, RAYMOND** | Base case already below CMP (GRSE). R/R 1.3:1 (RAYMOND). | ACTION NEEDED |
| 3 | **Q4 FY26 results watch** — EPACKPEB, KERNEX, NEWGEN | Go/no-go decision in May 2026. | Set reminder |
| 4 | **GROWW trim plan** — 500 shares, ~7% of portfolio | If above ₹190, trim → redeploy to NEWGEN (₹430) or hold cash for ICICIAMC (₹2,400). | Watch ₹190 |

---

## SECTOR THESIS — NUCLEAR POWER INDIA

- [ ] **Sector thesis:** `research/SECTOR_NUCLEAR_INDIA.md` — 100 GW by 2047, ₹14-23 lakh Cr total capex, SHANTI Bill 2025 opens private sector
- [x] **PATELSAIR** — nuclear angle confirmed. NPCIL = ₹23-24 Cr current revenue. N-NPT stamp = 1 of 3 in India.
- [ ] **Walchandnagar Industries** — Screener data + thesis (legacy DAE partner, 30-40% nuclear revenue)
- [ ] **MTAR Technologies** — Screener data + valuation check (precision nuclear components, typically 50-80x PE)
- [ ] **KSB Ltd** — quick check (only approved supplier for primary coolant pumps)
- [ ] **HCC** — balance sheet check (built 60% of India's nuclear plants, historically debt-heavy)
- [ ] **BHEL** — monitor nuclear turbine order book (₹10,800 Cr order for 6 turbine islands)

---

## RESEARCH BACKLOG

- [ ] NVDA Q&A deep dive — scale limits, AMD shift, hyperscaler spend motives, bear case ₹42 scenario
- [ ] Real US positions thesis — RGTI, OKLO, ACHR etc. (all in loss, speculative)
- [ ] STLTECH watch trigger — only revisit if DGTR anti-dumping duty granted
- [ ] **KCP Limited** — AGM transcript analysed (2026-03-25). Cement + heavy engg + Vietnam sugar. ₹978 Cr cash, 75 acres Chennai land. Interesting value play — needs Screener data for full thesis.
- [ ] **DCIL (Dredging Corp of India)** — 50-year company, ₹1,146 Cr revenue (highest ever), ₹1,400 Cr order book, targeting ₹3,000 Cr. PSU dredging monopoly.
- [ ] **SHAKTIPUMP** — apply TAM-anchored DCF (PM-KUSUM scheme 35L pump target, only 5L done)
- [ ] **Weekend Investing / Market Pulse** — subscribe beehiiv, add to reference sources. Read as macro pulse only, not stock picks.
- [ ] **Rotate Grok API key** — low priority. Delete at console.x.ai and generate new one.
- [ ] **AUTORESEARCH backtesting engine** — review `docs/AUTORESEARCH_APPROACH.md`, answer 7 decision points before building

---

---

## ARCHIVE — COMPLETED & REFERENCE

### ✅ Completed — 2026-04-15 session

- [x] **DCMSIL SOTP Model 3** — Century Enka as tyre cord peer (8.3x EV/EBITDA). Bear ₹50, Base ₹69, Bull ₹90. Conclusion: at ₹69 CMP, market paying ~₹100 Cr for pre-revenue defence.
- [x] **fetch_yt_channel.py** — YouTube channel transcript tool. Lists videos, fetches English transcripts (youtube-transcript-api v1.2.4 + yt-dlp fallback). Saves to `data/transcripts/CHANNEL/DATE_TITLE.md`.
- [x] **Transcript three-layer pipeline** — Synthesis → Summary → Raw transcript. SYNTHESIS.md rolling doc. skill: `analyze-transcript`.
- [x] **Ravi Dharamshi transcript analyzed** — iKmTGMthTDY. FII outflow = GFC-equivalent, bond yields 4.5% = Trump leash, IT structural headwind 1-1.5M jobs.
- [x] **PATELSAIR AGM analyzed** — EPMtzXum5o0. NPCIL = ₹23-24 Cr current revenue. FY25 revenue corrected to ₹287.82 Cr. P/E corrected to 10.5x. Cyclical slowdown confirmed by management.
- [x] **PATELSAIR updated** — CMP ₹315, status revised to SMALL STARTER DEFENSIBLE.
- [x] **TODO.md Task 6 added** — GitHub Pages viewer mode, branch-first constraint.

### ✅ Completed — 2026-04-09/10 session

- [x] Portfolio updated — Apr 7 holdings file used as source of truth
- [x] Decision Log created — `docs/DECISION_LOG.md` + rendered HTML + nav tab in index
- [x] Downside framework — added to `_TEMPLATE.md`
- [x] Print CSS — `@media print` added to `render_plan.py`
- [x] Section anchors + floating TOC — all research pages updated
- [x] NIFTY valuation page created
- [x] GRSE, RAYMOND, KERNEX, EPACKPEB, NESCO, LIFE (Ethos) updated
- [x] India tab fix — Indian watchlist stocks now visible under India tab
- [x] render_plan.py — accepts optional output dir arg

### ✅ Framework — DCF Growth Rate Methodology Fix (DONE)

All action items completed (2026-03-19): `docs/VALUATION_FRAMEWORK.md` updated with Growth Rate Anchoring section. SHILCTECH DCF re-run (base ₹2,613→₹4,670). Applied to KAYNES, EPACKPEB, KERNEX.

### ✅ Concall Deep Dive — Top 5 (ALL DONE)

| Stock | Status |
|---|---|
| EPACKPEB | DONE — Q3 FY26 concall + YouTube (6 thesis challenges found) |
| RAYMOND | DONE — all monitorables met, value unlock timeline pushed out |
| GRSE | DONE — NGC ₹33K Cr step-change, FY28 gap risk flagged |
| NESCO | DONE — segment data extracted, WSA ₹260 Cr yellow flag |
| KERNEX | DONE — March 2025 pres cross-referenced, TAM 2x (85,000 km) |

### ✅ Earlier Backlog (DONE)

- [x] ITC full thesis — SOTP ₹280-329, watchlist accumulate below ₹270
- [x] NILE — Grade C (10/25), 80-90% customer concentration, AVOID
- [x] NWIL/IIL — OWNED (165 shares, +52%)
- [x] NESCO full thesis — Grade B+, Tower 2 catalyst
- [x] HDFCBANK full thesis — Banking framework, post-merger integration
- [x] GRAB (US) — v3 rewrite, Grade B+, base $6.50-7.00
- [x] LIFE (US: Ethos) — Grade B, base $37, wait for lock-up July 2026
- [x] MSFT — Grade A, 20/25, base 2.1x in 5 years
