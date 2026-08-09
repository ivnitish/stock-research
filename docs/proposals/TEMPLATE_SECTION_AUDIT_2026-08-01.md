# Research Template — Section Audit
### Which sections earn their place, and which generate filler

**Date:** 2026-08-01 · **Basis:** the five notes just produced (CUMI, PROTEAN, Stovec, Triton Valves) + `research/_TEMPLATE.md`
**Status:** PROPOSAL — nothing changed yet. Pick what you want and I apply it to `_TEMPLATE.md` / `CLAUDE.md`.

---

## The one-line diagnosis

The template isn't too long — it has **four or five slots that produce the same words no matter the company**, plus **one calculation (bear/base/bull growth) derived three separate times**. Cut those and the note gets shorter *and* sharper. Everything that actually drove a recommendation this batch stays.

**Legend:**  🟢 KEEP as-is · 🔴 CUT · 🟡 MERGE (fold into another section) · 🔵 CONDITIONAL (include only when there's real data)

---

## Summary Verdict layer

| Section | Verdict | Why |
|---|---|---|
| Recommendation block (call + price ladder) | 🟢 KEEP | This is the product. Every reader decision comes from here. |
| Why this business? | 🟢 KEEP | The thesis in plain language. Load-bearing. |
| Strengths / Concerns | 🟢 KEEP | Drove all five calls. |
| How does this actually compound? (one-liner) | 🟢 KEEP | Cheap, points to Q3. Fine. |
| What does the market think — where do I disagree? | 🟢 KEEP | The edge, quantified. Keep. |
| **Second-Order Stress Test → 5-Whys ladder** | 🔵 CONDITIONAL | Sometimes drills to a real structural moat; more often restates one fact five times padded with "Why is that true? →". Keep only when the 5th answer is genuinely *structural* — else one "root cause of the moat" sentence. |
| **Second-Order Stress Test → "Market label vs reality" 6-row table** | 🔴 CUT | The template itself says half the rows answer "n/a / consensus aligned." The one useful cell (consensus vs our read) is already the whole point of "Where do I disagree?" above it. Collapse to the single *label-change-catalyst* line. |
| Multi-Bagger Math table | 🟢 KEEP | The core scenario table. Keep — but it's one of the three places the growth math is derived (see #6 below). |
| Key Metrics & Trends (P&L / BS / CF / quarterly / shareholding / ratios) | 🟢 KEEP | The factual spine of the whole note. |
| Downside Framework — what protects capital? | 🟢 KEEP | Four floors → the real floor. Drove the CUMI ₹500 anchor and Triton's ₹500 line. |
| When do I sell? (exit triggers) | 🟢 KEEP | Falsifiable conditions. Keep. |
| **Where does this rank?** | 🟢 KEEP | Came out useful this batch (CUMI-vs-Grindwell was real). Keep — but hold it to a genuine comparison, not a generic paragraph. |
| Growth Trigger Scan (6-row table) | 🟢 KEEP | Mostly "No" rows, but it's a fast cheap checklist. Borderline — I'd keep it. |
| Recent Developments / Action ladder | 🟢 KEEP | Keep. |

---

## Detailed Analysis layer

| Section | Verdict | Why |
|---|---|---|
| Deep Dives (A/B/C) | 🟢 KEEP | The best part of the detailed layer — stock-specific, not templated (CUMI's standalone-vs-consolidated walk-through was the whole thesis). |
| 1. Business Summary | 🟢 KEEP | Short, factual. Fine. |
| 2. Quality Score (threshold checks + 5-dim table) | 🟢 KEEP | Drives grade, MOS thresholds, position size. Keep. |
| 3. Q0 Operating Leverage / Q1 Incremental ROIC / Q2 Runway / Q3 Compounding math | 🟢 KEEP | The compounding engine. Q3 is where growth *should* be derived once. |
| **3. Q4 — What breaks the thesis?** | 🟡 MERGE | Duplicates the Risks table and "When do I sell." Fold into Risks. |
| **3. Q5 — Conviction anchor / "what I won't do in a drawdown"** | 🔴 CUT | Journaling, not analysis. Produces near-identical boilerplate every note ("won't average up, quality doesn't fix price, max size X%") — restates Downside Framework + Action ladder. |
| 4. Sector-Specific Operating Detail (segment metrics) | 🟢 KEEP | Genuinely stock-specific where it exists. |
| 4. Promoter Activity (8-qtr) | 🟢 KEEP | Real signal. Keep. |
| **4. Walk the Talk — Guidance vs Actuals** | 🔵 CONDITIONAL | High value *only if* we've read 2+ concalls. Otherwise it's "not available" rows — or a fabrication temptation. It's part of why Triton carries 7 "not available" markers. Include only with real concall history; else omit, don't stub. |
| 5.1 Primary Driver / 5.2 Reverse DCF / 5.3 Position Sizing | 🟢 KEEP | Core valuation. Keep. |
| **5.4 Model 1 (DCF/OE) scenario table** | 🟡 MERGE | Re-derives the *same* bear/base/bull growth as the Summary Multi-Bagger Math and Q3. Reference those numbers, don't rebuild a third table. |
| 5.5 Additional Checks (PEG, P/S band) | 🟢 KEEP | Cheap sanity checks. Keep. |
| 6. Competitive Landscape (position, peer table, re-rating) | 🟢 KEEP | Peer comparison drove the CUMI-vs-Grindwell and Stovec calls. Keep. |
| 7. Risks (full table) | 🟢 KEEP | Keep — and absorb Q4 here. |
| **8. Review Schedule** | 🟡 MERGE | Usually one trivial date + "events to watch." Fold into the Action ladder / Research Log. |
| **9. Decision History** | 🔵 CONDITIONAL | For any name we don't own — all six this batch — it's an empty table. Include only once a position exists. |
| 10. Research Log | 🟢 KEEP | The audit trail. Keep (never trimmed, per house rule). |
| Glossary | 🟢 KEEP | Useful for genuinely niche terms (rotary screen printing, PPP diagnostics). Keep, but hold it to niche terms — it drifts into re-defining things already explained inline. |

---

## #6 — The structural problem worth fixing first

The bear/base/bull **growth rate is calculated three times**:

1. Summary Verdict → **Multi-Bagger Math** table
2. Section 3 → **Q3** ("implied compounding math")
3. Section 5.4 → **Model 1** DCF scenario table

Three tables, one calculation. **Derive it once in Q3/5.1, display it once in Multi-Bagger Math, and have 5.4 reference those numbers rather than rebuild them.** This single change removes more redundant text than all the section cuts combined.

---

## Net effect if you apply everything

| Change | Type |
|---|---|
| Cut Q5 (conviction anchor) | 🔴 |
| Cut "Market label vs reality" table → keep 1 catalyst line | 🔴 |
| Fold Q4 into Risks | 🟡 |
| Fold Review Schedule into Action/Research Log | 🟡 |
| De-duplicate growth math (3 tables → 1) | 🟡 |
| Make 5-Whys, Walk-the-Talk, Decision History conditional | 🔵 |

**Nothing that drove a recommendation this batch is touched.** The note gets ~20-25% shorter, and the parts that remain are the parts you actually read.

---

*Proposal only. Tell me which rows to apply and I'll edit `_TEMPLATE.md` + the matching guidance in `CLAUDE.md`, then re-render.*
