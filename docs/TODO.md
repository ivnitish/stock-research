# Research System — TODO
*Last updated: 2026-04-27*

---

## ✅ Completed — 2026-04-27

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
