# Call Post-Mortem & Predict-Better Method

*Started 2026-08-09. Purpose: score past recommendations against outcomes, decompose why a stock moved, and turn each miss into a rule that improves the next call.*

---

## The method (how to understand why something is up, and predict better)

Every sharp move decomposes into two things and only two things:

```
Total return ≈ change in earnings (EPS)  ×  change in the multiple (P/E)
```

Step 1 — **Decompose the move.** Split the return into "the business delivered" (EPS grew) versus "the market re-rated" (multiple expanded). This single split tells you *why* it's up. Keltech: 0% earnings, all multiple. Eternal: all earnings (multiple actually fell). These are opposite situations that a headline "+40%" hides.

Step 2 — **If it's multiple-driven, name the driver and tag whether it was knowable.** Re-ratings come from observable things: a live sector theme, a catalyst window (annual report, order announcement, regulatory date), a thin/retail float, an order book that dwarfs current sales. All of these are visible *before* the move. If the driver was observable and I didn't weight it, that's a fixable miss. If it was pure unprovoked sentiment with no observable trigger, I call it unpredictable and don't pretend otherwise.

Step 3 — **Reflexivity flag.** Ask: does this re-rating *need* a future event to fire, or is theme + flow + tight float self-sustaining? If self-sustaining, the DCF price ceiling is the wrong tool — these names do not pull back to it. This is the specific blind spot below.

Step 4 — **Log the call and revisit.** Every BUY / HOLD / TRIM / AVOID goes in the scorecard with price-at-call. Revisit at ~8–12 weeks and tag it: RIGHT, RIGHT-THESIS-WRONG-SIZING, or WRONG. Over time the base rates recalibrate my probability weights — e.g. I put Keltech's bull case at 15%; the realised frequency of thin-float thematic doubles is clearly higher than that.

---

## Scorecard (2026-08-09)

| Name | Call (date) | Price then | Price now | ΔEPS vs ΔMultiple | Verdict | Lesson |
|---|---|---|---|---|---|---|
| **Keltech** | AVOID (Jun 1) | ₹5,010 | ₹9,750 | Almost all multiple (17x→37x), no earnings change, no defence order | Fundamentally RIGHT, tradeably MISSED | Reflexive re-rating; DCF right about business, useless about 3-month price |
| **Kernex** | TRIM 50% (Jun 2) | ₹1,895 | ₹2,452 (+29%) | Re-rating on ₹3,268 Cr order book (12.6x sales); P/E→51x | RIGHT-THESIS-WRONG-SIZING | Trimmed a thin-float defence name mid-re-rating on an asymmetry-number veto |
| **Raymond** | HOLD, don't add >₹500 (May 25) | ₹466 | ₹615 (+32%) | Aerospace re-rating + real earnings; P/E 24x | THESIS RIGHT, add-ceiling WRONG | Hard "don't chase above ₹X" ceiling on a working re-rating that never gave the pullback |
| **Swiggy** | EXIT (Mar 11) | ₹285 | ₹281 | Nothing — still loss-making, flat | RIGHT | Refusing to pay for hope with no earnings works — keep this |
| **Eternal** | HOLD, don't add at 937x (Mar 11) | ₹224 | ₹315 (+40%) | All earnings — P/E fell 937x→115x | RIGHT | Held and captured the +40%; correctly refused to add at 937x; gain came from the monitored trigger (Blinkit profit) |

---

## The systematic error (the pattern across the misses)

The framework is well-calibrated on one side and blind on the other.

**Where it is right (keep it):** refusing to pay for a multiple with no earnings underneath. Swiggy exit — correct. Not adding to Eternal at 937x — correct, and I still captured the move by holding because the gain came from earnings, not from a bigger multiple. The discipline that says "don't overpay for hope" is sound and I should not loosen it.

**Where it is blind (fix it):** applying a mean-reversion price ceiling to names that are already in a reflexive re-rating. Keltech (AVOID, no position → captured 0% of a double), Kernex (TRIM → gave up +29% on the trimmed half), Raymond (add-ceiling at ₹500 → never added, stock at ₹615). In all three the driver was observable in advance: a live theme, a tight or retail-heavy float, and a catalyst or order book far larger than trailing sales. These names do not respect a DCF ceiling. My 2x-asymmetry gate and "don't chase above ₹X" rule — correct for protecting a compounder entry — repeatedly cut off upside on momentum/thematic names.

The distinction that separates the two, and that I must make explicitly on every call: **is this an overvalued stock that will revert (Swiggy, 937x Eternal), or a reflexive re-rating with a real observable driver that will keep running (Keltech, Kernex, Raymond)?** Same "expensive" label, opposite correct action.

---

## Rules logged from this post-mortem

1. **Decompose before judging.** No verdict on a moved stock until the return is split into EPS vs multiple. "It's up 40%" is not analysis; "it's up 40% and all of it is earnings" is.
2. **Reflexive re-rating ≠ overvaluation.** When the driver is theme + tight float + live catalyst/order book, drop the hard price ceiling. Do not TRIM purely because an asymmetry number prints below 2x, and do not set a "don't add above ₹X" wall that assumes a pullback these names don't give.
3. **Size, don't gate.** For a working re-rating I already own (Kernex, Raymond), the question is target weight and trailing-stop discipline, not a binary add/trim toggle off a valuation ceiling. Trim on thesis-break or concentration, not on price alone.
4. **Recalibrate the bull weight.** Thin-float thematic doubles happen more often than the 10–15% I assign them. Raise the base rate when theme + float + catalyst all line up.
5. **Keep the Swiggy discipline.** None of the above loosens the refusal to buy loss-making or absurd-multiple names with no earnings path. That call was right and stays.

---

## To do

- Turn this into a running tracker: log every new call with price-at-call; a cron re-scores at +8/+12 weeks and appends the verdict. Cheap to run, and the accumulating base rates are what actually fix the probability weights.
- Back-fill the rest of the book (Anant Raj, Artemis, GRSE, Ather, etc.) into the scorecard so the calibration sample is the whole portfolio, not just the memorable misses.

---

<!-- AUTO-SCORECARD -->

## Auto-scorecard (bhavcopy close 2026-08-07)

Regenerated by `scripts/update_call_tracker.py`. Edit the calls in `data/call_tracker.csv`, not this block.

| Symbol | Call | Date | Ref ₹ | Now ₹ | Move | Flag | Note |
|---|---|---|---:|---:|---:|---|---|
| KELTECH.BO | AVOID | 2026-06-01 | 5,010.00 | — |  |  | Thin-float defence theme; AVOID on fundamentals; re-rated on flow |
| KERNEX.NS | TRIM | 2026-06-02 | 1,895.00 | 2,451.80 | +29% |  | Trimmed 50% on asymmetry<2x; order book kept it running |
| RAYMOND.NS | HOLD_ADD_CEILING | 2026-05-25 | 466.00 | 614.95 | +32% |  | Aerospace re-rate; add-ceiling at 500 too tight |
| SWIGGY.NS | EXIT | 2026-03-11 | 285.00 | 280.75 | -1% |  | Loss-making; exit correct - flat since |
| ETERNAL.NS | HOLD_NO_ADD | 2026-03-11 | 224.00 | 315.00 | +41% |  | Held; refused add at 937x; earnings caught up |
| THRIVE.BO | EXIT | 2026-06-02 | — | 81.57 |  |  | Exit call; kept falling - correct |
| STLNETWORK.NS | EXIT | 2026-03-11 | 18.90 | 24.89 | +32% |  | Distress exit; bounced +32% since - defensible |
| ATHERENERG.NS | MONITOR_NO_CALL | 2026-05-02 | 665.05 | 1,481.50 | +123% |  | Never underwrote; ran without a decision |
| BHEL.NS | MONITOR_NO_CALL | 2026-05-02 | 254.00 | 405.20 | +60% |  | Never underwrote; ran without a decision |
| SOUTHWEST.NS | MONITOR_NO_CALL | 2026-05-02 | 172.38 | 232.06 | +35% |  | Never underwrote; ran without a decision |
| ZENTEC.NS | MONITOR_NO_CALL | 2026-05-02 | 1,479.20 | 1,721.10 | +16% |  | Never underwrote; ran without a decision |
| DREDGECORP.NS | WATCHLIST | 2026-05-02 | 898.45 | 1,071.30 | +19% |  | Parked on watchlist; ran |
| PPAP.NS | BUY_AT_LOWER | 2026-06-01 | 256.00 | 321.35 | +26% |  | Standing order never filled; ran to 321 |
| ANANTRAJ.NS | HOLD | 2026-05-02 | 460.80 | 615.90 | +34% |  | Owned; thesis working |
| ARTEMISMED.NS | HOLD | 2026-05-02 | 236.67 | 316.30 | +34% |  | Owned; thesis working |
| BANCOINDIA.NS | HOLD | 2026-05-02 | 589.50 | 686.95 | +17% |  | Owned; thesis working |
| GRSE.NS | HOLD | 2026-05-02 | 2,267.42 | 2,599.00 | +15% |  | Owned; thesis working |
| ICICIAMC.NS | HOLD | 2026-05-02 | 2,165.00 | 3,072.80 | +42% |  | Owned; thesis working |
| NEWGEN.NS | HOLD | 2026-05-02 | 447.78 | 551.00 | +23% |  | Owned; thesis working |
| SHILCTECH.NS | HOLD | 2026-05-02 | 4,559.69 | 4,620.10 | +1% |  | Owned; thesis working |
| NESCO.NS | HOLD | 2026-05-02 | 1,150.00 | 1,047.10 | -9% |  | Owned; slightly down |
| NWIL.BO | HOLD | 2026-05-02 | 27.96 | 24.20 | -13% |  | Owned; down |
