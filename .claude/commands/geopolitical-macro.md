# Geopolitical Macro Analysis

Analyze the geopolitical event `$ARGUMENTS` and its impact on crude oil, the US dollar, Indian rupee, and Indian equity markets. Produce a full, structured research document and open it in Chrome.

---

## Instructions

You are acting as a geopolitical macro analyst with a Munger-style investing lens. The goal is not just to describe what is happening, but to:
- Identify first-principles transmission mechanisms
- Build scenario probabilities using game theory + historical base rates
- Produce actionable investor guidance for Indian equity portfolios

Work through each phase below sequentially. Use WebSearch heavily — do NOT rely on prior knowledge alone for current events. Run multiple searches in parallel where phases are independent.

---

## Phase 1: Event & Players

Search: `[EVENT] latest update [current month year]`
Search: `[EVENT] key players objectives strategy`

Document:
- What happened (dates, triggers, key actors)
- For each player: Objective | Constraint | Leverage | Vulnerability | Staying power
- Who are the HIDDEN players? (countries that benefit without being in the war, proxy actors, economic beneficiaries of prolongation)

---

## Phase 2: First Principles Economics — The Central Disruption

Identify the single most important commodity or financial variable being disrupted (e.g. oil, gas, semiconductors, shipping lanes, currency).

Then build the transmission chain:

```
Disruption
  → Supply shock in [commodity]
    → Price spike
      → Import bill increases for India
        → CAD widens
          → Rupee weakens
            → Imported inflation rises
              → Growth slows / RBI constrained
                → Equity earnings decline
```

Quantify each link where possible:
- $10/bbl oil increase = 0.4-0.5% of GDP added to India's CAD
- Every 1% rupee depreciation = X bps of imported inflation
- Use published coefficients; cite sources

---

## Phase 3: Supply Chain Reality Check

Search: `[commodity] alternative supply routes bypass [event]`
Search: `[commodity] who is actually hurt [event] analysis`

Challenge the obvious narrative. Ask:
- Are there bypass routes that reduce the disruption?
- Is it a total blockade or a selective one?
- Who is being told they're hurt but actually has workarounds?
- Who is being told they're fine but is actually exposed?

Document the **actual** disrupted volumes vs the headline claim.

---

## Phase 4: Currency & Macro Impact (India-Specific)

Search: `Indian rupee [event] impact forecast [year]`
Search: `RBI response [event] forex reserves intervention [year]`
Search: `India current account deficit [event] [year]`

Cover:
- CAD trajectory (pre-event baseline → projected peak)
- Rupee level and forecast (Goldman, MUFG, BofA targets)
- RBI intervention: spot sales, OMOs, forex reserve depletion rate
- RBI policy dilemma: stagflation = can't hike (kills growth) or cut (worsens currency)
- India's forex reserve adequacy (months of import cover)

---

## Phase 5: Equity Market Impact (India)

Search: `Nifty [event] sector impact [year]`
Search: `FII outflows India [event] [year]`

Build the time-lag model:

| Phase | Timing | What Happens | Nifty Impact |
|-------|--------|--------------|--------------|
| Fear phase | Week 1-3 | Sentiment selloff, FII exit | Initial drop (quantify %) |
| Damage phase | Weeks 4-10 | Actual earnings hit | Further drop |
| Earnings phase | Month 3-4 | Results season, downgrades | Trough |
| Recovery | Month 5-6 | Resolution signals priced in | Rally begins |

Sector breakdown table:
- Which sectors are severely hurt, moderately hurt, insulated, or benefit
- Why (specific cost/revenue mechanism, not just "it's cyclical")

---

## Phase 6: Player Incentive Analysis (Game Theory)

For each major player, build the payoff matrix:

```
                    PLAYER B
                 Negotiate    Fight On
Player A  Neg  [outcome 1]  [outcome 2]
         Fight [outcome 3]  [outcome 4]
```

Answer for each player:
- What is their dominant strategy?
- What conditions would make them deviate?
- What is their exit condition (what does "winning" look like for them)?
- What is their breaking point (when do they accept a worse outcome)?

Hidden player check (mandatory):
- Who benefits from prolongation that is NOT a direct party?
- Are they supplying intelligence, arms, financial support, or diplomatic cover?
- What would it take to remove this hidden support?

---

## Phase 7: Historical Reference Class (Tetlock Discipline)

Search: `[event] historical comparison [comparable past event]`

Find 3-5 comparable events. For each:
- Duration from start to ceasefire/resolution
- Commodity price impact (% change, peak, normalization time)
- Resolution mechanism (diplomacy, military victory, exhaustion, economic collapse)
- India-specific outcome (CAD, rupee, Nifty, any crisis events)

Base rate conclusion: What is the median duration? What drove outliers longer or shorter?

---

## Phase 8: Prediction Markets

Search: `Polymarket [event] odds probability [year]`
Search: `Metaculus [event] forecast [year]`

Pull real-money probability estimates. Use these as a sanity check:
- Where do your scenario probabilities diverge from market consensus?
- If you're more pessimistic than the market, why? What does the market know that you don't, or vice versa?

---

## Phase 9: Scenario Construction

Build exactly 4 scenarios:

**Scenario A: Resolution** (optimistic)
**Scenario B: Base Case** (most likely — grinding prolonged state)
**Scenario C: Escalation** (tail risk, bad)
**Scenario D: Wildcard** (low probability, high impact either direction)

For each scenario:

| Field | Value |
|-------|-------|
| Probability | X% |
| Duration | X weeks/months |
| Central commodity price range | $X-Y |
| Nifty peak-to-trough | -X% to -Y% |
| Nifty trough timing | Month/Quarter |
| INR/USD | X-Y range |
| India CAD | X% of GDP |
| Key trigger that causes this scenario | ... |
| Observable signals (2-3 specific, watchable) | ... |
| Best investor action | ... |

Then compute the probability-weighted expected Nifty outcome:
`(P_A × outcome_A) + (P_B × outcome_B) + (P_C × outcome_C) + (P_D × outcome_D)`

---

## Phase 10: Mandatory Blind Spot Check

Before finalizing, explicitly search for and answer:

1. **Hidden prolongers:** "Who benefits if this continues?"
2. **Bypass routes:** "[commodity] alternative route [event] [year]" — does the supply disruption have a workaround?
3. **Pre-existing constraints:** Are there existing treaties, trade deals, or political commitments that change how key players can respond? (e.g. India-US oil deal constraining Russian oil purchases)
4. **Internal dynamics:** Is there a power struggle inside the key belligerent? Who is in charge, and are they a hawk or pragmatist?
5. **Second-order shocks:** Beyond the direct commodity shock, what else breaks? (supply chains, food prices, LNG markets, shipping lanes)

---

## Phase 11: Signals Dashboard

Produce a clean table:

| Signal | What It Confirms | Scenario | Investor Action |
|--------|-----------------|----------|-----------------|
| [specific observable event] | [what it means] | [A/B/C/D] | [buy/sell/hold/specific sector] |

Minimum 6 signals. Make them specific and observable — not "peace talks" but "Turkey FM visits Tehran for bilateral meetings."

---

## Phase 12: Output

Write the complete analysis to `/tmp/geopolitical_macro_[slug].md` where `[slug]` is a short identifier for the event (e.g. `iran_war_2026`).

Structure the document as:
1. Executive Summary (5 bullet points max)
2. The Event (Phase 1 output)
3. First Principles: The Transmission Chain (Phase 2 output)
4. Supply Chain Reality Check (Phase 3 output)
5. India-Specific Macro Impact (Phase 4 output)
6. Indian Equity Market Impact (Phase 5 output)
7. Player Incentives & Game Theory (Phase 6 output)
8. Historical Parallels (Phase 7 output)
9. Prediction Market Data (Phase 8 output)
10. Scenario Analysis (Phase 9 output)
11. Blind Spots Checked (Phase 10 output)
12. Signals Dashboard (Phase 11 output)

Then render to HTML:
```
python3 /tmp/render_plan.py /tmp/geopolitical_macro_[slug].md
```

Then open in Chrome:
```
open /tmp/geopolitical_macro_[slug].html
```

---

## Quality Rules

- Every number must have a source (publication, date, analyst name)
- Never fabricate prices, probabilities, or market data
- Scenario probabilities must sum to 100%
- Challenge the consensus — the first-pass obvious narrative is usually incomplete
- The blind spot check (Phase 10) is mandatory, not optional
- Historical base rates (Phase 7) must anchor scenario probabilities — do not assign probabilities based on narrative alone
