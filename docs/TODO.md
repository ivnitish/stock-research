# Research System — TODO
*Last updated: 2026-07-05*

---

## ✅ Completed — 2026-07-05 (5-stock research batch: SETL, VISL, SELECTRIC, PPAP + TRIVENI update)

Batch run via parallel subagents. All five are WATCHLIST/AVOID — no new positions. Common thread: quality-ish businesses (or freshly-listed special situations) at prices that already discount perfect execution.

- **SETL (Standard Glass Lining) — WATCHLIST, Grade B · 15/25.** `research/SETL.md` created. India's largest glass-lined reactor maker for pharma/specialty-chem (Dr Reddy's since 2014, Aurobindo, Cadila, Laurus). CMP ₹277.75 → ~72x trailing, the most expensive glass-lined stock in India (GMM Pfaudler 46x, Anup 41x, HLE 50x). FCF negative 5 straight years; ROCE collapsed 43%→15% post-IPO as capital came in. ~₹1,000 Cr order book (1.3x book-to-bill). GScale Energy data-centre acquisition (₹487 Cr planned) flagged as venture-grade diversification outside core competence. Buy alert ₹180-200. **Note: file title reads "Standard Engineering Technology" — likely a naming slip; business is unambiguously Standard Glass Lining Technology. Needs header correction.**
- **VISL (Vedanta Iron & Steel) — AVOID, Grade C · 11/25.** `research/VISL.md` created + updated same day from demerger deck. Newly-listed (Jun 2026) iron-ore + ESL steel + Liberia demerger entity. CMP ₹42.6, up ~110% since listing on thin-float momentum while 1H FY26 segment EBITDA collapsed ~55% YoY. Trades ~12x FY25 / ~26x 1H-FY26-annualised EV/EBITDA vs NMDC 5x, Tata 8x, JSW 10x. Governance overhang (Vedanta Resources UK ~$5bn debt, history of upstreaming listco dividends; Viceroy flagged ESL's ₹2,000 Cr NCD may route to parent). Management demerger deck targets 4x EBITDA ($133M→$526M by FY29) — haircut 60-70% for execution/cycle risk it's worth ~₹22-31/share, inside the existing base range, so no rating change. Watch below ₹28.
- **SELECTRIC (Schneider Electric President Systems, BSE 544786) — WATCHLIST, Grade B- · 14/25.** `research/SELECTRIC.md` created. Schneider (~74%) subsidiary making 19-inch server-rack/telecom enclosures, direct-listed 12 Jun 2026. CMP ₹1,518 → 48x on FY26 PAT that FELL 19% (revenue −16%) — FY25 may have been a data-centre pull-forward. Trade-for-trade, ~288-share daily volume, thin-float melt-up. India DC rack market ~19% CAGR is the structural tailwind. Buy zone below ₹950.
- **PPAP Automotive — WATCHLIST, Grade C · 11/25.** `research/PPAP.md` created. Auto-ancillary (sealing systems + injection-moulded parts) for Maruti/Honda/Toyota. CMP ₹256 vs book ₹242 — trades slightly ABOVE conservative fair value, no MOS today. FY26 headline PAT ₹43 Cr is a mirage: ~₹49.8 Cr one-time gain from selling the Tokai rubber JV stake; core operating profit ~₹0.2 Cr. Margin collapse 21%→10% OPM is structural (top-2 customers 68%, no pricing power). Products EV-agnostic (protects volume not margin). ₹4,171 Cr order book secures volume not margin. Buy alert ₹200-210 (near book).
- **TRIVENI — updated (corporate-action SOTP per-share estimates).** Merged user-provided demerger value split: TPTL ₹275-350/PT share, sugar stub ₹200-250/TRIVENI share. On the 1:3 ratio, combined package ≈ ₹292-367 vs CMP ₹446.90 → market paying ~20-35% premium to sum-of-parts pre-listing. Sharpens read toward mild overvaluation; no rating change (still WATCHLIST/TRACKING 1-2%). Best entry is buying the ex-demerger sugar stub at ₹250-300 post-listing.

All five rendered to HTML + PDF; index.html updated with all rows in the watchlist section.

### Open follow-ups from this batch

- **SETL:** correct the file header company name (Standard Engineering Technology → Standard Glass Lining Technology); verify exact registered name and NSE symbol. Watch FY27 FCF turn and whether GScale acquisition dilutes returns.
- **VISL:** first standalone quarterly print is the load-bearing validation. Watch ESL 5 MTPA commissioning timeline and whether $1.3Bn capex funding breaks the <2x Net Debt/EBITDA promise (only ~$266M debt capacity on FY26 EBITDA — chicken-and-egg).
- **SELECTRIC:** watch whether FY27 H1 revenue re-accelerates (real growth) or FY25 was a one-off pull-forward. CFO exit flagged in unlisted commentary — verify governance.
- **PPAP:** needs FY26 segment-level P&L and capacity utilisation (not in Screener public view). Whole thesis = does core OPM recover to 12%+ over FY27-28.

---

## ✅ Completed — 2026-07-02 (TRIVENI initial research — demerger arbitrage)

- **TRIVENI new initiation — WATCHLIST / TRACKING 1-2% at ₹446.90.** `research/TRIVENI.md` created. Grade B · 15/25. Fair-value special situation, not a compounder. Consolidated PAT ₹269 Cr FY26, ROCE 9%, P/E 36x. The bet is the NCLT-approved demerger of the Power Transmission Business into TPTL (record date 3 Jun 2026, listing ~Aug 2026). PT segment does 34% PBIT margin on ₹370 Cr FY25 revenue (~5% of revenue, ~31% of pre-tax profit). Combined SOTP ₹320-428 vs CMP ₹446.90 → 0-10% base case upside, no margin of safety. Bull ₹625 (+40%) on TPTL at 30x + sugar MSP revision; Bear ₹280 (-37%) on soft TPTL listing + frozen MSP. Asymmetry ~1.2x — below the 2x BUY REDUCED threshold. Correct call is TRACKING (1-2%) into pre-listing window with option to build on stub if it overshoots below ₹380 post-listing.
- **Framework flag noted:** the "hidden gem" framing was tested against numbers — consolidated ROCE 21%→9% in 3Y, PAT CAGR 3Y −19%, FCF negative 4 of 5 years — pushed back against the marketing narrative. Advisor call before drafting caught this. PT segment moat is real but it's a small slice of the consolidated business.
- **HTML rendered** via `venv/bin/python3 src/render_all.py TRIVENI --no-pdf`. Index updated with TRIVENI row in watchlist section: Grade B · 15/25, Tracking 1-2%, SOTP ₹410 vs CMP ₹446.90.

### Open follow-ups for TRIVENI

- **Watch TPTL listing (August 2026 expected)** — first-10-day close and mcap. Below ₹1,900 Cr = re-rating trade fails, exit tracker. Above ₹2,400 Cr = build to 2%.
- **Watch sugar stub print post-listing** — if TRIVENI stub trades below ₹300 without proportional TPTL uplift, buy sugar+ethanol at 10-12x forward PAT.
- **Data gap:** FY25/FY26 segment-level PBIT for Sugar, Alcohol, Water is estimated from management commentary. Update when FY26 annual report drops (Aug-Sep 2026). H1 FY26 PDF could not be parsed; direct AR download needed for segment capital employed.

---

## ✅ Completed — 2026-06-07 (STLTECH rally decode + VINDHYATEL new initiation)

- **STLTECH rally decode + verdict update.** `research/STLTECH.md` rewritten with June 2026 update at top, original March note preserved below divider. Stock moved from ₹187 (Mar 13) → ₹619 (Jun 6) = +231% in 3 months; from Jan 27 low of ₹84.65 = +631% / 7.4x. Four catalysts mapped: (1) $1.11 bn US hyperscaler order through Mar 2029 — single largest driver; (2) DGTR anti-dumping duty on Chinese/Korean/Indonesian OFC effective Aug 2025, 5-year duration; (3) AI-data-center thematic re-rating (10-36x more fiber per MW vs cloud DC); (4) India DC capacity 1.4 GW → 8 GW by 2030. Grade upgraded C·11 → B·14 (business genuinely inflecting), but verdict held at WATCHLIST because asymmetry from ₹619 is 1.27x — below 2x threshold. Multi-Bagger Math: Bull ₹1,150 (+86%) / Base ₹620 (0%) / Bear ₹195 (-68%). Buy zone ₹420-450 or proof of second hyperscaler order. Framework lesson logged: a stock with specific catalysts identified in a watchlist note should default to 1-2% tracking position, not 0% — the March note's serial-conditions approach cost the 7x.

- **VINDHYATEL new initiation — BUY REDUCED 3-4% at ₹1,993.** `research/VINDHYATEL.md` created. Grade B · 16/25. Deep-value mirror trade to STLTECH: same anti-dumping tailwind (group's Birla Furukawa was the petitioner), same India DC + 5G + government infra tailwind, but at P/B 0.56x (vs STLTECH 13.3x) and on positive earnings (₹220 Cr TTM PAT vs STLTECH ₹56 Cr). Three structural value drivers: (a) trades at half book value; (b) 8.29% stake in listed Birla Corporation worth ~₹800-1,200 Cr — 35-50% of own mcap, marked at cost on BS; (c) Birla Cable merger (10:115 swap, NCLT pending) consolidates group OFC under one listed entity. Q4 FY26 PAT ₹103 Cr (47% of full-year) confirms anti-dumping flow-through has begun. Order book ₹5,812 Cr = 1.6 years revenue visibility. Multi-Bagger Math: Bull ₹4,200 (+110%) / Base ₹3,000 (+50%) / Bear ₹1,400 (-30%). Asymmetry 1.7x base / 3.7x bull. MOS 33.6%. Funding source flagged: STLNETWORK (currently -40%) is the natural recycle candidate. Five Kamayaka triggers firing (regulatory + margin expansion + turnaround + capacity expansion + consolidation).

- **Anti-dumping concept explained** to user (CFA Level 1 background) using the OFC case as the concrete example — DGTR process, dumping margin calculation, 5-year duration, petitioner-benefits-most principle, EU boomerang risk.

- **`output/html/index.html` updated:** STLTECH row upgraded to Grade B · 14/25 with "Watch · Buy <₹450" action and ₹619 CMP / ₹420-450 buy zone shown. VINDHYATEL added as new row in watchlist section: Grade B · 16/25, "Buy Reduced · 3-4%" action, ₹1,993 CMP / ₹3,000 base target.

- **HTML rendered** via venv python (`/Users/nitish/stocks automation/venv/bin/python3 /tmp/render_md.py`) for both files; opened in Chrome for review.

- **Feedback saved to memory:** `feedback_groww_mcp_on_demand.md` — Groww MCP is on-demand only, not auto. MEMORY.md updated accordingly.

### Open follow-ups for next session

- **Watch STLTECH Q1 FY27 print** (Aug 2026) — PAT >₹150 Cr would confirm run-rate ₹600 Cr+ and pull forward earnings; below ₹100 Cr = order delivery slipping
- **Watch VINDHYATEL Q1 FY27 print** (Aug 2026) — OPM must stay ≥6% to confirm Q4 FY26 margin step-up was anti-dumping flow-through and not project-mix one-off
- **Track Birla Cable merger NCLT progress** (Q2-Q3 FY27 expected closure)
- **Consider STLNETWORK exit** to fund VINDHYATEL initiation — separate decision but flagged as natural recycle
- **Adjacent candidates to evaluate:** HFCL (Grade B inflection at P/B 5.86x), KRN Heat Exchanger (DC cooling, wait <₹950)

---

## ✅ Completed — 2026-06-02 (NESCO / ICICIAMC / SHILCTECH Q4 FY26 review)

- **Three small-position Q4 FY26 reviews logged.** All three files received a 2026-06-02 entry at the top of their Research Log section. Source: Screener.in consolidated (NESCO, SHILCTECH) and standalone (ICICIAMC) — May 2026 concall transcripts referenced but not yet read; flagged for follow-up.
- **NESCO Q4 FY26:** Revenue ₹252 Cr (+31% YoY), OPM 47% (down from 56% YoY — Foods mix dilution continues), PAT ₹93 Cr (+5%). FY26 full year ₹932 Cr revenue (+27%), PAT ₹413 Cr (+10%). CMP ₹1,164 / P/E 19.9x. **Verdict: HOLD** — thesis intact, position 1.9% appropriate, adds belong at ₹900-1,100. Segment-level IT Park vs BEC vs Foods split not in consolidated Screener data — needs BSE standalone Q4 filing.
- **ICICIAMC Q4 FY26:** Revenue ₹1,517 Cr (+20% YoY, flat QoQ), EBITDA margin 76% (operating leverage continues), PAT ₹763 Cr (+10% YoY but **-17% QoQ** — likely treasury MTM, needs concall confirmation). FY26 ₹5,765 Cr revenue (+16%), PAT ₹3,298 Cr (+24%). CMP ₹3,354 / P/E 50.3x. **Verdict: HOLD** — toll-booth working, +52% P&L doing its job, no trim. Add zone ₹2,200-2,400 only.
- **SHILCTECH Q4 FY26 — MAJOR MISS, thesis-level event.** Revenue ₹152 Cr (-34% YoY vs ₹232 Cr Q4 FY25), OPM compressed to **21%** from 31%, PAT ₹28 Cr (-49% YoY). FY26 full year ₹652 Cr revenue (+4.7%) and PAT ₹158 Cr (+7.5%) — **missed even the March DCF bear case** (which projected ₹811 Cr / ₹195 Cr). CMP ₹4,030. Recalibrated bear case fair value ~₹2,275 — implies CMP is 77% above recalibrated downside. **Verdict: TRIM half on rally above ₹4,200, monitor Q1 FY27 + read May 2026 concall** before deciding on remaining position. Hard exit trigger: another YoY revenue decline AND OPM <25%. Quality score should drop to ~16/25 pending concall context (is the miss US-tariff-driven and transient, or demand-driven and structural?). The portfolio model's -11.3% 3y CAGR target for SHILCTECH now looks RIGHT — the capacity-anchored DCF upgrade from March 2026 is broken.
- **Open follow-ups for next session:** (1) Read SHILCTECH May 2026 concall transcript for revenue miss cause + order book FY27 visibility — decide trim vs exit; (2) Read ICICIAMC May 2026 concall for the QoQ PAT dip cause (treasury vs operating); (3) Pull NESCO Q4 BSE standalone for segment-level IT Park / BEC / Foods split.
- HTML re-rendered via `python3 src/render_all.py`.

---

## ✅ Completed — 2026-06-02 (Q4 FY26 refresh for ARTEMISMED / GRSE / ANANTRAJ)

- **ARTEMISMED** — Added 2026-06-02 log entry to `research/ARTEMISMED.md`. Screener refresh (CMP ₹269, mcap ₹4,258 Cr, P/E 40.2). Material new datapoint: board has called June 4 postal ballot to **raise up to ₹700 Cr** (~16% potential dilution at CMP). Reverses the 2026-06-01 "pause the trim" stance — **proceed with TRIM to 2-3% of portfolio** ahead of the dilution overhang. Quality score 15/25 Grade C reconciliation confirmed; no dimension upgrade. ROE still 12% (below 13% used in P/B-ROE model).

- **GRSE** — Added 2026-06-02 log entry to `research/GRSE.md`. Q4 FY26 numbers already captured in 2026-05-10 update; this entry focuses on **governance flags**: BSE ₹9.55L fine 29-May-2026 for missing independent directors / committees Q4 FY26; FY26 secretarial report flagged "multiple NSE/BSE fines"; two new senior technical appointments late May. Added governance compliance risk row to Section 7 risks table. No score change yet — but two consecutive quarters of fines would downgrade Management 3/5 → 2/5 and overall 17/25 → 16/25. HOLD-with-trim-above-₹3,000 unchanged; NGC binary catalyst still primary swing factor.

- **ANANTRAJ** — Added 2026-06-02 log entry to `research/ANANTRAJ.md`. Q4 FY26 is genuinely new and clean: **Revenue ₹647 Cr, PAT ₹149 Cr (+25% YoY per Screener), OPM 26%**. FY26 full year ₹2,512 Cr / ₹557 Cr (revenue +22%, PAT +31%, OPM +200 bps — operating leverage in the literal sense). Updated header (CMP ₹549, mcap ₹19,752 Cr, P&L +19.1%), FY26 row in financials table, Q4 FY26 row in quarterly trend (with note on Q4 FY25 discrepancy between Screener fetch and original file figure). **Material catalyst:** 01-Jun-2026 MoU with Haryana government for ₹25,000 Cr data centre & cloud services investment — data centre pivot has moved from optionality to in-motion. HOLD-and-let-it-run; raised informal buy zone to ₹450-500 (no chasing above CMP). 17/25 Grade B retained.

- HTML re-render kicked off via `python3 src/render_all.py` (background).

---

## ✅ Completed — 2026-06-02 (VENUSREM Q4 FY26 review)

- **VENUSREM Q4 FY26 + FY26 results review.** `research/VENUSREM.md` updated with 2026-06-02 Research Log entry (top of section 11), Q4 row added to Quarterly Trend table, 2026-05-26 result bullet added to Recent Developments, Update History row added, header refreshed (CMP ₹1,414, market cap ₹1,890 Cr). Numbers from Screener consolidated 2026-06-02 fetch: Q4 revenue ₹259 Cr (+33% YoY, largest quarter ever), OPM 24%, PAT ₹48 Cr (+129%); FY26 revenue ₹770 Cr, OPM 19%, PAT ₹103 Cr (+129%), EPS ₹76.90; **₹10/share dividend declared — first in 12+ years**; borrowings ₹12 Cr; reserves ₹650 Cr; AGM 2026-08-20. **OPM-sustain test passed comfortably** (Q3 21% + Q4 24%; FY26 19% vs the 18% upgrade-condition bar). VRP-034 status not disclosed in the result release — flagged as open follow-up. **Recommendation held, not changed:** existing 3-4% holders HOLD (do not trim on price alone — upgrade condition met but stock ran ahead of confirmation); new money WAIT for ₹950-₹1,100 pullback OR Phase 2 catalyst; aggressive add zone moves to <₹950 from <₹780. TRIM trigger at ₹1,400 not fired because failure condition (no FY27 OPM ≥17%) not observable yet and trajectory supportive. Multi-bagger math + Action Table formal refresh queued for v1.2 (FY26 PAT ₹103 Cr already above v1.1 FY27E base case of ₹100 Cr — pulled forward ~1 year). HTML re-rendered via `python3 src/render_all.py`.

---

## ✅ Completed — 2026-06-02 (Telegram bridge + morning-news skill)

- **Telegram bridge built** — `scripts/telegram_bridge.py` forwards messages from @niti_agent_bot to `claude -p` running in this repo. Whitelists chat ID 1679797853 only. Uses `--dangerously-skip-permissions` (unattended), `--continue` after the first message of each chat session, `/new` command resets, `/whoami` debugs auth. Replies "thinking..." immediately so user sees the message landed. Logs to `scripts/telegram_bridge.log` (gitignored) with 10s spawn timeout and 600s run timeout. Long replies chunked at 4000 chars. Bot token + chat ID live in `.env` (gitignored); `.env.example` shipped. Run: `caffeinate -dims python3 -u scripts/telegram_bridge.py` from venv.

- **morning-news skill** — `.claude/skills/morning-news/SKILL.md` is the single source of truth for the daily brief. Reads `data/portfolio.csv` (no Groww/Kite calls), ranks holdings by cost basis (qty × avg_buy_price), web-searches last-24h material news for each (results / regulatory / management / orders / ratings — skip price moves and noise), plus top-5 India + top-3 US macro. Writes `docs/MORNING_BRIEF.md`. Behaviour switch: `MORNING_NEWS_DRY_RUN=1` stops after writing the file; otherwise opens a GitHub issue (GitHub emails the user) and POSTs the issue URL to Telegram via `TELEGRAM_BOT_TOKEN`. Local runner `scripts/morning_news.py` invokes the skill with the dry-run flag by default; `--full` flips to production mode.

- **Open loops** — (1) cloud `/schedule` routine still to be created at claude.ai/code/routines pointing at the morning-news skill (8:45 IST daily); (2) bridge dies whenever the laptop sleeps — Oracle Cloud ARM free tier is the durable fix.

---

## ✅ Completed — 2026-06-01

- **KELTECH (Keltech Energies) research file created** — `research/KELTECH.md` written + rendered to `output/html/KELTECH.html` + indexed under Grade C section. Grade **C (12/25), AVOID at ₹5,010**. Defence-energetics market label does not appear in company disclosure: customer page lists Coal India, NMDC, SAIL, cement majors and zero MoD/OFB/DRDO entries; segment report shows only Explosives (88%) + Perlite (12%); OPM 8% vs Solar Industries' 28% and Premier Explosives' 10%-on-defence-book. Multi-bagger math: bear ₹3,185 (-36%) / base ₹6,400 (+28%) / bull ₹16,800 (+236% IF defence revenue actually shows up in FY26 AR). Asymmetry 0.78x at CMP — does not clear Phase 5.3 thresholds. Revisit triggers: ₹3,500 entry zone, FY26 annual report defence disclosure (July-Aug 2026), or quarterly OPM through 10% for 2 consecutive quarters. Peer comp table the most load-bearing analysis. ₹38 Cr CWIP build in FY26 with no investor presentation explaining purpose is the residual reason not to short. Open questions: capex purpose, capacity utilisation, Chowgule group RPT in FY26 AR.

- **NIBE Ltd research file created** — `research/NIBE.md` written + rendered to `output/html/NIBE.html` + indexed under Grade C watch section in `output/html/index.html`. Grade C+ (13/25), **TRACKING POSITION 1.5% at ₹1,521**. Multi-bagger math: bear ₹720 (-53%) / base ₹2,000 (+31%) / bull ₹3,200 (+110%) over 3 years; asymmetry unfavourable at CMP, becomes 2x at ₹1,150 entry. Thesis: real capability story (Pinaka ToT May 2025, Elbit PULS partnership, ₹3,000 Cr Shirdi complex inaugurated 23 May 2026 by Defence Minister, Suryastra MLRS production flagged off) but ugly FY26 numbers (PAT collapsed from ₹27 Cr to ~₹0, two consecutive quarters of operating losses, debtor days 109→178, FCF negative two years). Phase 5.6 forward PEG primary applied (capex absorbing margins). Walk-away triggers: any quarter with negative PAT AND debtor days >200; QIP >10% of equity; promoter <50%. Phase 0.4 active triggers: Capacity Expansion + Regulatory Tailwind + Turnaround (partial). Phase 0.5 capability passes (Shirdi built/operating), Phase 4.5.3 borderline (capex absorbing without prior-cycle ROIC proof). Open questions: Is Q4 FY26 snap-back delivery catch-up or genuine ramp? Total order book across subs? Why did NAL cease as step-down subsidiary April 2026?

---

## ✅ Completed — 2026-05-25 (afternoon — portfolio single-source-of-truth fix)

- **Portfolio page collapsed to single source of truth.** Three pages were drifting and confusing agents (portfolio.html, PORTFOLIO_OVERVIEW.html stale at 2026-03-13 showing wrong totals like ₹15.21L invested / 45 positions, and the inline table inside index.html). Cleanup: `output/html/PORTFOLIO_OVERVIEW.html` now a meta-refresh redirect to `portfolio.html`; `research/PORTFOLIO_OVERVIEW.md` moved to `research/archive/PORTFOLIO_OVERVIEW_v1_2026-03-13.md`; the OVERVIEW card on index.html (line ~1464) now points at portfolio.html with accurate copy; the three orphaned scripts `src/portfolio_overview.py`, `portfolio_update.py`, `portfolio_review.py` moved to `src/archive/`. Updated `.claude/commands/portfolio-check.md` and `.claude/agents/portfolio-reviewer.md` so future agents read portfolio.html first (Kite/Groww MCP becomes the fallback, not the entry point). README.md gained a "Source-of-truth chain" diagram so the rule is documented.

- **Expected 3yr CAGR column removed; Upside % + Action shown instead.** The old "Exp 3y CAGR" applied a single 3-year horizon to per-row targets that came from research files written with different horizons (EPACKPEB ₹800 multi-year base case sat next to RAYMOND ₹530 1-yr fair value next to ETERNAL ₹218 exit trigger), producing a meaningless weighted +18.3% portfolio CAGR. The fix replaces the CAGR column with two cleaner columns: **Upside % = (target / CMP − 1) × 100** (raw distance, no horizon assumed) and **Action** (BUY / ADD / HOLD / WATCH / EXIT, taken from each row's action-tag class in index.html). The snapshot now shows "Avg Upside · Active Holds" current-weighted across BUY/ADD/HOLD positions only (excludes EXIT/WATCH/no-target), with explicit caveat in the footer that target horizons differ.

- **`src/refresh_portfolio.py` rewritten** to match the current 7-cell stock-row layout in index.html (the legacy version expected an 11-cell layout that index.html stopped using around mid-May, so portfolio.html was silently stuck on May 12 stale data). New flow: read qty/avg from portfolio.csv, CMP from latest broker xlsx, target+action from index.html stock-rows, then generate (a) standalone portfolio.html + (b) snapshot block in index.html. The old per-row patch logic on index.html stock-rows was dropped — index.html stock-rows are now read-only for the script's purposes (they belong to the research-index view, not the portfolio view).

- **FOCUS.md + INVESTING_PLAYBOOK.md updated** to drop the misleading "18.3% expected 3yr CAGR" header line and point at portfolio.html for live state instead. Both re-rendered to HTML.

---

## ✅ Completed — 2026-05-25

- **Portfolio model targets refresh** — `src/valuation_dashboard.py` TARGETS dict updated for three stale entries flagged in this session: **RAYMOND ₹493 → ₹1,100** (post-realty-demerger SOTP base; aerospace + auto components only — old target was set before clean post-demerger numbers); **EPACKPEB ₹800 → ₹500** (de-rate is done, from here PAT-growth play not multiple-expansion play; ₹800 needed margin breakout to 13-14% AND multiple staying at 25-30x while sector de-rates — aggressive); **KERNEX ₹1,444 → ₹1,800** (base case at P/E 30x FY29E; explicit caution: don't add above ₹1,050, trailing 43x already rich). Method strings document the reasoning.

- **EPACKPEB research file refresh** — `research/EPACKPEB.md` log entry for 2026-05-25: corrected position-size header (was 451 sh / ₹195 avg from older snapshot, actual is **1,451 sh at ₹183.99 avg, 23.0% of portfolio**, +8.8% in profit). Folded in Q4 FY26 + FY26 print (revenue ₹1,525 Cr +34%, PAT ₹93 Cr +56%, OPM stuck at 10% all four quarters — margin breakout failed empirically). Peer comp table vs INTERARCH and PENIND (corrects earlier overstatement that "peers at 13-15% OPM" — actual PEB sector is 9-11% structural). PEB sector de-rate diagnosis (P/E 57x → 22x is multiple compression, not earnings collapse; largely done from here). Revised multi-bagger math from ₹184 entry: base 2.5x (₹460-500), bull 3.5-3.8x (₹650-700). Position-size decision: **trim 400 sh @ ₹200-210 to drop to 17%**, redeploy ~₹80K (₹42K → RAYMOND add, ₹35K → NEWGEN dry powder <₹430). Q1 FY27 thesis test rules: OPM ≥12% AND order book cover >0.8x ⇒ upgrade; OPM <11% AND cover <0.7x ⇒ exit residual to ~5%.

- **KERNEX research file refresh** — `research/KERNEX.md` log entry for 2026-05-25: B- borderline-multibagger scrutiny under 80%-in-top-5 concentration mandate. CMP ₹1,351 (mcap ₹2,271 Cr), P/E **43.1x trailing** (already very rich), P/B 13.1x, ROE 38% / ROCE 23.8% / OPM 23% (excellent), order book ₹2,704 Cr (~10x FY25 revenue), April 2026 BLW + PLW Kavach wins ₹158 Cr. Honest multi-bagger math from ₹1,125 entry: base 1.6x (₹1,800), bull 2.5x (₹2,800), bear 0.8x (₹900). Three structural reasons to stay cautious: 43x P/E means most multiple expansion is done, promoter holding 28.8% (declining, below 30% framework threshold), execution at scale unproven (FY25 was first profitable year). **Hold 90 sh, don't add above ₹1,050.** Not a top-5 conviction slot at current price.

- **RAYMOND research file refresh — Q4 FY26 concall deep dive (YouTube)** — `research/RAYMOND.md` log entry for 2026-05-25 from Q4 FY26 earnings call transcript ([Concall.in upload](https://www.youtube.com/watch?v=H33qGBo2q9A), hosted by Anand Rathi). Full transcript saved at `data/transcripts/raymond/raymond_q4_fy26_concall.txt` (55,390 chars). New disclosures absorbed:
  - **Aerospace segment ₹392 Cr revenue (+26% YoY), EBITDA ₹88 Cr (+25%), 22.3% margin**; order book ₹2,350 Cr over 5 years; 75% of products engine-segment across LEAP/GTF/narrow-body/wide-body; 25+ customers (single OEM has 7+ legal entities — derisked); 100+ new SKUs FY26 targeting 250-365/year ("one a day")
  - **Auto components ₹1,667 Cr revenue (+10%), EBITDA ₹223 Cr (+34%), 13.4% margin (+240 bps YoY)** — operating leverage CONFIRMED structural per SAP HANA + integration synergies + cost reduction programs (not one-off)
  - **₹930 Cr 5-year capex disclosed** (₹500 Cr aerospace + ₹430 Cr auto) — fully self-funded from internal accruals, no dilution risk
  - **Andhra Pradesh greenfield timeline clarified**: commercial production starts late calendar year 2027 = Q4 FY28 (was assumed May 2027 in prior research); FY29 is when "real growth" from AP shows up (~₹150-200 Cr incremental)
  - **NEW optionality surfaced**: first build-to-spec / own-design IP order won (customer + product confidential); N1 component qualification (rotating engine parts — turbine blades etc) on roadmap (currently N2; N3→N2 took 5y); industrial gas turbine RFQs in pipeline
  - **Updated SOTP**: base ₹1,100-1,200 (3x from ₹364 entry), bull ₹1,500-1,800 (4x), stretch 5y with aerospace pure-play SOTP unlock ₹2,000-2,500 (5-6x from entry)
  - **Position-size action**: add ~90 sh in ₹460-475 zone (funded from EPACKPEB trim above); takes RAYMOND from 11.1% → ~14% of portfolio. Don't pay above ₹500.

### Pending repo tasks (broker-side stock repositioning is user's own; not tracked here)

- **SAKSOFT thesis verification** — portfolio model shows +31.7% expected CAGR (highest after EPACKPEB); currently only 5% weight. Refresh research file to verify whether thesis supports promoting to a 10% slot in top-5 multi-bagger basket.
- **BANCOINDIA deep refresh** — owned position 4.9% with shallow research file; user previously flagged as priority refresh.
- **NEWGEN Q1 FY27 working-capital normalisation check** — research file has open monitor: working capital days exploded 72d → 244d in Q4 FY26; needs to drop back <200d in Q1 FY27 print for the deep-dive A diagnostic to close cleanly.

---

- **Iran War v3 — Day 85 update (May 19-24 events).** Added a fresh section at the top of `research/IRAN_WAR_V3.md` and re-rendered `output/html/IRAN_WAR_V3.html`. Five-day events:
  - **Russia oil waiver expired May 16 without renewal.** Treasury Sec Bessent publicly said no renewal (May 12-13), Treasury posted a renewed licence (May 14-15), licence lapsed (May 16). India's May 14 formal extension request was acknowledged, not granted. India's May 2.3 mbpd Russian-crude run-rate is now a ceiling, not a floor. Secondary-sanctions risk on Indian banks/shippers active.
  - **14-point MOU now "converging"** per Iran FM spox Baghaei (May 23 — Persian first, then English). Enrichment moratorium negotiated at 12-15 years; snap IAEA inspections; first frozen-asset tranche $6-10B.
  - **60-day ceasefire extension reportedly close to signing.** Business Standard May 22 wrap tied Nifty +0.27% (close 23,719) to traders monitoring US-Iran talks; Hormuz reopening is the signing condition.
  - **Iran-Oman Hormuz toll framework** — Iran offered paid-passage model; Trump rejected the structure (insisting "free, no toll"), not the underlying trade. Oman channel still active at deputy-FM level.
  - **Markets:** Brent ~$105 (May 22), INR 96.96 ATH low (past v3 escalation tell of <97), Brent-Dubai spread widening to Dubai +$1.50 from near-parity on May 18.
  - **Probability shifts vs v3 May 19:** base case 55% → 45-50%; escalation 25% → 25-30%; de-escalation 20% → 25-30%; regime fracture unchanged sub-5%. Distribution widened — both tails fatter, same expected value.
  - **Action list adjustments:** de-escalation trade moves from "deploy on signing" to "1-2% probe pre-signing" (Indian financials + IT) because MOU convergence is now official Iranian language. ONGC trade now closer to active because Brent has held >$95 for four weeks AND Russia exemption lapsed. PSU OMC / Indigo / defence / paints unchanged.

---

## ✅ Completed — 2026-05-19

- **Index page declutter (Proposal B+A) — complete.** Full restructure of `output/html/index.html`:
  - **B (sections):** Built new `output/html/library.html` with 15 meta-doc rows (Macro, Market Notes, Screens, Frameworks, Decisions, Journals, Learning) moved off the homepage. Linked via "📚 Library" in header nav.
  - **A (columns):** Trimmed from 16 columns to 7 — kept Ticker, Grade, Action, CMP, P&L%, Target·Mult (combined), arrow. Dropped Qty, Avg, Δ/share, Invested, Current, P&L₹, CMP-Ref, Buy-Zone. 87 rows transformed. ~21% line reduction (2480 → 1954).
  - **Holdings rebuilt against portfolio.csv as source of truth:** 6 stale held rows (GROWW, KAYNES, SHAKTIPUMP, NAVA, RSYSTEMS, PARADEEP — all exited but cells never cleared) cleared and evicted to Watchlist section. BSE and RAILTEL also evicted (researched but not held). Total 8 rows moved to Watchlist.
  - **Held block sorted by current value desc** (user explicitly said "not by grade"). Single "INDIAN HOLDINGS" banner replaces the previous Grade A / Grade B 19/25 / Grade B 18/25 / Grade B 17/25 / Grade C / Tracking sub-banners. Top 5 holdings by value: EPACKPEB, RAYMOND, KERNEX, NEWGEN, THRIVE.
  - **Totals reconciled to portfolio.csv:** Header pf-strip and footer TOTAL row both show ₹11.62L invested, ₹12.62L current, +₹1.00L (+8.61%), 23 holdings, dated 19-May-2026. Previously off by ₹1.4-3.6L because of the 6 stale held rows + stale hardcoded values.
  - **Nav dedup:** Removed the `👁 Portfolio` toggle button (column-trim made it redundant). Single `📊 Portfolio` link to `portfolio.html` remains.
  - 14 watchlist-no-thesis rows (KPITTECH, BRIGADE, FABTECH, NIPPOBATRY, TTKHLTCARE, SAGILITY, URBANCO, POLICYBZR, IZMO, NDTV, CGCL, VSTIND, NETWEB, SATIN) removed from index entirely — no research, no holding, just cruft.
  - 4 monitor-position stub research files created (ATHERENERG, BHEL, ZENTEC, SOUTHWEST) so all index links resolve. DREDGECORP onclick wired to existing research file. Only QQQM (US ETF info row) intentionally remains without an onclick.
- **Scripts added** to `src/` for repeatability: `declutter_index.py` (row removal + onclick wiring), `fix_index_totals.py` (CSV reconciliation + strip/footer update), `trim_index_columns.py` (16→7 column transform), `rebuild_held_block.py` (rebuilds held block from CSV with sort), `sort_index_by_amount.py` (earlier iteration, kept for reference).

---

## ✅ Completed — 2026-05-18

- **Multibagger Astral study integrated.** `multibagger_ASTRAL.md` validated APPENDIX 2 — Astral compounded ~20-25x 2014-2022 while trading at 30-50x trailing P/E throughout; PEG 1.0-1.6x most of the run. Four refinements applied to `research/learnings/multibagger_patterns.md` APPENDIX 2 as "Refinements from Astral study (2026-05-12)" sub-section: (1) **Mix-shift duration substitutes for rate** — terminal mix percentage is the criterion, not 200bps/yr threshold (100bps × 9yrs ≈ 200bps × 4yrs); (2) **Distribution density uses company's own disclosure** — track whichever count the company reports consistently, not an imposed definition; (3) **Crisp-event re-rating vs cumulative re-label** — Phase 4.5.4 distinguishes step-function re-ratings (BSE/BAF/APL) from attrition re-ratings (Astral/Cera/Fine Organic), with different position-sizing implications; (4) **Kill signals need corroboration** — single trigger = monitoring signal; ≥2 concurrent triggers needed to confirm runway closed and justify exit (Astral 2022-2024 was a false positive under single-trigger rule). Re-rendered to HTML and pushed to `output/html/`.
- **Multibagger study index links fixed.** 6 existing rows (MULTIBAGGER pattern synthesis, BSE STUDY, BAF STUDY, TITAN STUDY, PAGE STUDY, APL STUDY) had no `onclick` handler — visible but unclickable since 2026-05-04. All 6 wired to `multibagger_X.html`. New ASTRAL STUDY row added to the same series. Per-study HTML files (multibagger_BSE.html, _BAF.html, _TITAN.html, _PAGE.html, _APLAPOLLO.html, _ASTRAL.html) rendered via background agent and copied to `output/html/` from `research/learnings/`. Updated synthesis card to reflect "6-stock study + APPENDIX 2".
- **Invisible-links systemic issue identified.** 26 stock-rows in index.html have no onclick (20 in tracking-india section, 6 multibagger rows now fixed). Triage of the remaining 20 (KPITTECH, BRIGADE, FABTECH, NIPPOBATRY, TTKHLTCARE, SAGILITY, URBANCO, POLICYBZR, IZMO, NDTV, CGCL, VSTIND, NETWEB, ZENTEC, SATIN, BHEL, ATHERENERG, DREDGECORP, SOUTHWEST, QQQM) in progress via background agent — output will list per-row recommendation (wire existing / create stub / remove).
- **Index page declutter proposal in flight.** User flagged page is too cluttered (~50 rows × 15 columns, mostly "—" placeholders for non-held rows). Audit agent producing 3 layout options for selection.

---

## ✅ Completed — 2026-05-16

- **VENUSREM v1.1 — material correction for VRP-034 / FDA QIDP miss.** User flagged that v1.0 missed Venus's April 2025 US FDA QIDP designation for VRP-034 (novel polymyxin B with proprietary Renal Guard tech, 70% nephrotoxicity reduction). QIDP under GAIN Act = priority FDA review + Fast Track + 5 years extra US market exclusivity (10 total post-approval). This is the FDA pathway v1.0 incorrectly assumed was absent. Re-graded: MOAT 3→4, MANAGEMENT 2→3, GROWTH RUNWAY 3→4. **Quality Score 15→18/25 (Grade B upper half).** Probability-weighted PV ₹1,117 vs CMP ₹912 → MOS 18%, asymmetry >2x. **Recommendation upgraded from Tracking 1-2% to BUY REDUCED 3-4%** at ₹912; build to 5% on Q4 FY26 OPM ≥18% OR VRP-034 Phase 2 progression. Aggressive buy zone moved up from <₹700 to <₹780. Index entry tag updated to "Buy reduced 3-4% · Build <₹780", val-tag changed to undervalued, asymmetry shown as ~2.3x.
- **VENUSREM v1.0 initial thesis** — `research/VENUSREM.md` written. Grade B (15/25), TRACKING POSITION 1-2% at CMP ₹912. Subsequently upgraded — see v1.1 entry above. Core thesis: post-debt-cleanup injectables exporter (carbapenem/meropenem focus); borrowings ₹335 Cr (FY16) → ₹2 Cr (FY25); Q3 FY26 EBITDA margin >20% (multi-quarter high), 9M FY26 PAT +127% YoY on revenue +12%. Three Kamayaka triggers firing (capex, operating leverage, margin expansion). AMR optionality via Feb 2025 Infex Therapeutics MET-X license (UK partnership). Catalysts: Q4 FY26 results 2026-05-26 (OPM sustain test + possible first dividend in 12 years); VRP-034 Phase 2 progression; MET-X readouts.
- **Memory saved** — `feedback_no_default_tracking.md` — don't default to "Tracking 1-2%" on every stock. Grade A/B + asymmetry >2x + MOS >15% means BUY REDUCED 3-5%, not Tracking. For pharma research, always search FDA designations (QIDP / Fast Track / Orphan / Breakthrough) before grading — VENUSREM v1.0→v1.1 case study.

---

## ✅ Completed — 2026-05-12

- **RAILTEL initial thesis** — `research/RAILTEL.md` written (643 lines, ~9.5K words). Grade B (16/25), **BUY REDUCED 3%** at CMP ₹333. Base FV ₹442 (MOS 24.7%), bear ₹245, bull ₹680. Asymmetry 1.27x. Core thesis: Telecom segment ROIC 37% on already-depreciated 65,000-km OFC + railway right-of-way; segment mix-shift from low-margin Project (4-5%) toward high-margin Telecom (27% and rising via Data Centre + Aadhaar). Sharpest concern: trade receivables +30% YoY vs revenue +23%; cash conversion the load-bearing watch. Index entry added under `grade-b india` 16/25 section.
- **RAILTEL Section 4c added (OFC + DC deep dive)** — answering: can the OFC + DC sub-business reach ₹10,000 Cr standalone valuation? Math: FY30 needs OFC ₹2,100 Cr (12% CAGR), DC ₹950 Cr (47% CAGR; 25-30 MW capacity vs 3 MW today), combined PBIT ₹915 Cr at 30% margin, exit P/E 15x → ₹10,275 Cr standalone. Probability ~40-50% by FY30, ~65-70% by FY32. Trigger to upgrade conviction: FY28 capex guidance during May 2027 call — if ₹500 Cr+ with explicit DC capacity targets >10 MW, size up. Hyperscaler partnership (telegraphed 18 months, not yet announced) is the single biggest accelerant.
- **NSDL framework gap-fill pass** — added (a) "Why this business?" opener, (b) first-principles physical earnings mechanism per Instruction 9 (three observable revenue drivers with evidence already in motion), (c) Growth Trigger Scan across 6 Kamayaka triggers (two yellows, zero greens — speculative-entry by Kamayaka rule, consistent with tracking-not-buy verdict), (d) Technical Entry Snapshot from Trendlyne (CMP ₹855, RSI 42.7, MFI 35.6, price below both 50- and 200-SMAs — neutral with slight oversold tilt; updated MOS 36.8%, asymmetry 1.35x at the new CMP), (e) Glossary defining DP/DPS, demat, custody, NDML, AA, e-KYC, PEG, OPM, promoter conventions, OFS, FII/DII, reverse DCF. Plus Multi-bagger Math + MOS section added 2026-05-11: present-day fair values (bear ₹487, base ₹1,352, bull ₹2,024) discounted at 13% from 3-yr targets; MOS 35.3% clears Grade B threshold but asymmetry 1.23x caps at tracking-not-full-BUY. Full-BUY upgrade triggers: CMP ≤ ₹780, OR two consecutive quarters of revenue ≥22% with OPM ≥32%.
- **GREAVESCOT, RAILTEL, NSDL rendered** to HTML + PDF (`output/html/{...}.html`, `output/pdf/{SYMBOL}_2026-05-12.pdf`). All three opened in Chrome.

---

## ✅ Completed — 2026-05-11

- **GREAVESCOT initial thesis** — `research/GREAVESCOT.md` written. Grade C (12/25), WATCHLIST. Sum-of-parts asymmetry note. Standalone diesel-engine + Excel earns ₹200 Cr PAT but GEML (Ampere EV) burns ₹182 Cr at segment PBIT — consolidated EPS ₹4.60 hides ~₹8.59 standalone. CMP ₹177 vs base FV ₹150 (-15% MOS), bear ₹47 (-73%), bull ₹273 (+54%). Asymmetry 0.74x — fails >2x test at current price; spec buy zone ₹120-135. Catalysts: GEML PBIT loss narrowing (-₹223 → -₹182 in FY26), FAME III notification, GEML IPO (DRHP filed Dec 2024). Added to index.html under watch/grade-c section. Q4 FY26 segment data fetched from financial results PDF; investor presentation downloaded to `data/filings/GREAVESCOT/`.

---

## ✅ Completed — 2026-05-10

- **Q4 FY26 results sweep** — fetched and analysed for RAYMOND, NEWGEN, GRSE, EPACKPEB (not yet filed), LIFE/Ethos.
  - RAYMOND: aerospace ₹119.4 Cr revenue cleared ₹110 Cr trigger; PBIT margin 17.45% (missed 20% bar by 2.55pp). FY26 aero ₹392 Cr (+26%), PBIT ₹49 Cr (+51%). Net debt has reappeared (~₹360 Cr) as AP plant capex begins to bite.
  - NEWGEN: FY26 revenue ₹1,574 Cr (+6%), PAT ₹301 Cr, EPS ₹21.38. Subscription +24% (SaaS +36%); US +20%; India/EMEA license deals delayed.
  - GRSE: FY26 revenue ₹7,002 Cr (+38%), PAT ₹748 Cr (+42%), EBITDA margin 15.3%. ₹520 Cr revenue + ₹63 Cr PBT from P-17A true-up (underlying revenue ~₹6,482 Cr +28%).
  - LIFE/Ethos: Q1 2026 revenue $193M (+104% YoY) blew out; stock at $30 vs $8-10 buy zone — dip thesis dead unless lock-up unloading creates real selling.
  - EPACKPEB: Q4 not filed yet (board meeting pending). Mambattu Phase II commercial production from Apr 29 → Q1 FY27 impact.
- **Portfolio reality fix — research file `Status:` headers refreshed** to match `data/portfolio.csv`:
  - RAYMOND — was "EXITED"; now HOLD 300 sh @ ₹364.37, +42% (CMP ~₹516). Decision: HOLD; add zone ₹400-450; trim zone ₹620+.
  - SWIGGY — was "OWNED IPO entry"; now HOLD 49 sh @ ₹565, −52%. Decision: EXIT and harvest ~₹14.5K capital loss.
  - ETERNAL — was stale entry/CMP; now HOLD 98 sh @ ₹337, −27%. Decision: HOLD until ₹260+ rally then trim/exit.
  - GRSE — was WATCHLIST + EXIT call; now HOLD 26 sh @ ₹2,267, +29%. Decision: HOLD; trim half above ₹3,000 if NGC contract remains unsigned.
  - ARTEMISMED — was OWNED 181 sh; now HOLD 362 sh @ ₹236.67, +3%. Position is 7.4% of portfolio. Decision: TRIM to 2-3%.
- **index.html structural fixes:**
  - RAYMOND moved from `data-section="watch india"` → `"grade-b india"` (held). Action tag: "Watch · Re-buy <₹380" → "Hold · add ₹400-450".
  - GRSE duplicate watchlist row removed (was double-listed at line 1484). Action tag updated: "Hold · add at ₹1,800-2,000" → "Hold · trim above ₹3,000 if NGC unsigned".
  - SWIGGY action tag updated: "Weak Hold — Q4" → "Exit · harvest loss".
- **Memory saved** — `feedback_check_portfolio_first.md` — always read `data/portfolio.csv` before framing any stock recommendation; existing positions are HOLD/ADD/TRIM decisions, not "re-enter" decisions; lean into TRACKING POSITION calls per framework matrix instead of defaulting to WATCHLIST/AVOID.

## ✅ Completed — 2026-05-12

- **`src/refresh_portfolio.py`** — single-command portfolio refresh: reads latest broker xlsx, refreshes CMP + derived cells in index.html, computes weighted expected 3yr CAGR, inserts Portfolio Snapshot block, flags stale Status headers. Idempotent. Also generates `output/html/portfolio.html` (Groww-style standalone view, sorted by current value).
- **`output/html/portfolio.html`** — clean held-only Portfolio tab: snapshot at top, sortable columns (click headers, default Current value desc), per-stock P&L + expected 3yr CAGR, click-through to research file. Renamed "Wt %" → "% of Portfolio" with tooltip.
- **`/refresh-portfolio` slash command** — `.claude/commands/refresh-portfolio.md` so user can invoke without remembering Python command.
- **`docs/FOCUS.md`** — new "what I'm doing now" landing page. Top of page: this week's high-priority TODOs (concall reads for top 3 holdings, decided exits, price alerts, monthly capital commitment). Middle: Path-to-₹1Cr tracker with monthly checkpoints + scenario table at different injection rates. Bottom: quick links + cadence reminder. Rendered to `output/html/FOCUS.html`.
- **`docs/INVESTING_PLAYBOOK.md`** — standing investing rules: 5 focus areas (concentration cap at 12, exit 7-day rule, entry asymmetry ≥1.5x, Sunday concall read, cycle winners at 0.95× target), cadence table, "rules I commit to" (10 rules), 12-slot tracker template, "don't" list for ADHD-loud moments. The week-specific actions section now links to FOCUS.md to avoid duplication.
- **index.html + portfolio.html nav** — added `🎯 Focus` (red, prominent), `📖 Playbook` (blue) links to both pages. Focus is the high-priority landing.

## Open (next session)

- **Simplify index.html** — user feedback: page has too much noise (currently ~2800 lines, ~50+ rows mixing grades, US, tracking, watchlist, scenario). Options to consider: (a) move all 1-share tracking stubs to a separate `tracking.html` page; (b) compress grade-A/B/C into a single sortable "Research" tab; (c) make the held vs watchlist split harder (right now they share grade sections); (d) reduce number of columns visible by default — many cells are "—" for watchlist rows. Decide architecture before editing.
- **Wire FOCUS.md regeneration into `/refresh-portfolio`** — currently FOCUS.md is hand-edited. The Path-to-₹1Cr table should auto-fill from broker exports each month. The 12-slot tracker in playbook should auto-rank from portfolio.csv current value.
- **High priority — Nitheesh's concall reads:** EPACKPEB, RAYMOND, KERNEX (see FOCUS.md). I (Claude) cannot do these for him — they're personal-conviction reads. Next session start: ask if these were done.

## Open (next session, lower priority)

- **Build `src/refresh_portfolio.py`** — single command that reads latest broker export from `data/broker-exports/`, joins with portfolio.csv, generates portfolio snapshot table, refreshes CMP cells in index.html. Currently sync_holdings_from_csv.py only updates qty/avg/invested — leaves CMP cells untouched. Wire CMP refresh in.
- Decide on the SWIGGY exit (book loss) and ARTEMISMED trim (sell ~200-260 sh). Both need user execution; not autonomous.
- ETERNAL — set price alert at ₹260 to trigger exit-on-rally action.
- Watch GRSE May 8 concall transcript (not yet posted to BSE) for: NGC contract status, FY27 revenue guidance, FY28 P-17A delivery gap mitigation.
- ARTEMISMED Quality Score reconciliation — research file says 15/25 Grade C; index.html says B 16/25. Pick one and update the other.

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

### Multi-bagger study queue (learning, not buy candidates)

- See `research/learnings/_QUEUE.md` — 7 candidates queued from the "quality re-rates ahead of earnings" pattern (Astral, KEI, Varun Beverages, Deepak Nitrite, Garware Hi-Tech, Fine Organic, Cera). Order of priority: Astral → Deepak Nitrite → Varun → KEI → others. 3-4 studies expected to validate the pattern before promoting the appendix in `multibagger_patterns.md` to a main-framework hook. Queued 2026-05-10.

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
