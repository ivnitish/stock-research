# Valuation Framework — DCF + P/B-ROE

*How we value stocks in this research system. Read this before trusting any number in a thesis.*

**Last updated:** 2026-03-19

---

## Why Two Models?

No single valuation model is complete. We use two models because they stress-test different assumptions:

| | **DCF** | **P/B-ROE** |
|---|---|---|
| **Question asked** | What are future cash flows worth today? | Is the business earning above its cost of equity? |
| **Best for** | Asset-light compounders, predictable FCF | Financial firms, high-ROE businesses |
| **Fails when** | FCF is lumpy or negative (capex cycle) | Book value is understated (intangibles) |
| **Verdict when they agree** | High conviction | High conviction |
| **Verdict when they disagree** | Dig deeper — one assumption is wrong | Dig deeper — one assumption is wrong |

**Rule:** If DCF says overvalued but P/B-ROE says undervalued (or vice versa), the disagreement *is* the insight. It means the market is betting on whether ROE sustains. Our job is to have a view on that.

---

## Model 1: DCF (Discounted Cash Flow)

### Theory

A business is worth the present value of all future free cash flows, discounted back at the investor's required return.

```
Enterprise Value = Σ [FCF_t / (1 + r)^t]  +  Terminal Value
Terminal Value   = FCF_n × (1 + g) / (r - g)      ← Gordon Growth
Value per Share  = Enterprise Value / Shares Outstanding
```

Where:
- `FCF_t` = Free cash flow in year t (we use net profit as proxy if FCF isn't available)
- `r` = Discount rate (our required return, typically 12% for India)
- `g` = Terminal growth rate (typically 5% for India — nominal GDP growth)
- `n` = Projection period (we use 5 years)

### Our Assumptions (India defaults)

| Parameter | Default | Rationale |
|-----------|---------|-----------|
| Discount rate | **12%** | India risk-free rate 7% (10Y G-Sec) + equity risk premium 5% |
| Terminal growth | **5%** | India nominal GDP CAGR (4% real + 1% productivity) |
| Projection period | **5 years** | Balances predictability with relevance |
| FCF proxy | Net profit | Used when reported FCF not available / lumpy |

> **Note on discount rate:** 12% is our floor. For small/micro-cap stocks (higher execution risk), we use 14-15%. For very high-quality compounders with predictable FCF, 12% is appropriate.

### 3-Scenario Framework

We always run 3 scenarios rather than one point estimate:

| Scenario | Growth assumption | Interpretation |
|----------|------------------|----------------|
| **Bear** | Slow-down: 15% → 6% | Management disappoints, competition intensifies |
| **Base** | Moderate: 25% → 12% | Current trends continue, some normalization |
| **Bull** | Strong: 35% → 15% | Thesis plays out, new products add revenue |

The range between bear and bull fair value tells you the **uncertainty premium** — how much depends on execution.

### Reverse DCF — The Most Useful Tool

Instead of "what is it worth?", ask: **"What growth rate does the current price already assume?"**

```
Solve for g* such that:  DCF(FCF, g*, r=12%, terminal=5%) = Current Market Cap
```

If the implied growth rate is unrealistically high → stock is expensive.
If it's below what you believe is achievable → margin of safety exists.

**Example (GROWW at ₹157):**
Market cap = ₹95,728 Cr. With ₹1,824 Cr FCF → implied growth = **39% CAGR for 5 years**.
That's aggressive. Even Amazon/Google didn't sustain 39% FCF CAGR for 5 years.

---

## Model 2: P/B-ROE (Justified Price-to-Book)

### Theory

A company's price-to-book ratio should reflect how much its ROE exceeds the cost of equity. This comes from the residual income / Gordon Growth model:

```
Justified P/B = (ROE - g) / (CoE - g)
Fair Value    = Book Value per Share × Justified P/B
```

Where:
- `ROE` = Return on Equity (net profit / shareholders' equity)
- `g` = Expected long-term earnings growth rate
- `CoE` = Cost of equity (our required return, same as discount rate = 12%)

### Intuition

| Situation | P/B Implication |
|-----------|----------------|
| ROE = CoE | P/B = 1.0 (fair = book value) |
| ROE > CoE | P/B > 1.0 (premium deserved — business creates value) |
| ROE < CoE | P/B < 1.0 (discount warranted — business destroys value) |
| ROE >> CoE | Very high P/B justified — but only if ROE *sustains* |

**Example:** GROWW ROE = 50%, CoE = 12%, g = 12% → Justified P/B = (50-12)/(12-12) → model breaks (g = CoE). At g=6%: P/B = (50-6)/(12-6) = **7.3x**. Fair value = ₹11.9 × 7.3 = ₹87.

Wait, that seems lower. But in the base case (g=12%), the formula produces a very high P/B because ROE so far exceeds CoE. This is a reminder: **high-ROE businesses with reinvestment opportunities deserve very high P/B multiples.**

### Implied ROE — The Reverse Version

```
Implied ROE = (Current P/B) × (CoE - g) + g
```

This tells you: "**What ROE is the market assuming this company sustains forever?**"

If the implied ROE is above what you believe is achievable → overvalued.
If it's below what you believe is sustainable → undervalued.

**Example (GROWW at P/B 12.6x, g=10%):** Implied ROE = 12.6 × (12-10) + 10 = **35.2%**. Current ROE is 50%. So the market is actually *discounting* a meaningful ROE decline already. That's more reasonable than DCF suggests.

### Our P/B-ROE Scenario Assumptions

| Scenario | ROE Assumption | Growth (g) | Interpretation |
|----------|---------------|------------|----------------|
| **Bear** | 25% (halved) | 8% | ROE compresses significantly, business matures |
| **Base** | 40% (moderate decline) | 12% | Good business, some ROE normalization |
| **Bull** | 50% (current ROE sustained) | 18% | Platform moat sustains, new products reinforce ROE |

---

## When the Two Models Disagree

This is the most important section. When DCF says overvalued and P/B-ROE says undervalued:

```
DCF is essentially saying: "Future cash flows aren't that large"
P/B-ROE is saying: "But this business generates massive value per rupee of equity"
```

The reconciliation is always the **ROE sustainability question**:
- If ROE declines (as DCF implicitly assumes in its growth slowdown), then P/B will compress too
- If ROE sustains (as the P/B-ROE base/bull case assumes), the P/B-ROE model is right

**Heuristic:** For **capital-light, platform businesses** (GROWW, ICICIAMC, SAKSOFT), trust P/B-ROE more — their ROE is structurally high because they don't need much equity to grow. For **capital-heavy businesses** (KAYNES, EPACKPEB), trust DCF more — they need to constantly reinvest equity, so ROE is harder to sustain.

---

## Worked Examples

### Example 1: GROWW (Capital-light, high ROE)

**Inputs:**
- FCF (FY25): ₹1,824 Cr | Shares: 628 Cr | CMP: ₹155
- Book Value: ₹11.9/share | ROE: 50% | CoE: 12%

**DCF Results:**

| Scenario | 5-Yr Growth | Fair Value | vs ₹155 |
|----------|------------|------------|---------|
| Bear | 15% → 6% | ₹55 | -65% |
| Base | 25% → 12% | ₹74 | -53% |
| Bull | 35% → 15% | ₹97 | -38% |
| **Implied** | **39% flat** | **₹155** | — |

DCF verdict: **Expensive.** Market pricing 39% FCF CAGR.

**P/B-ROE Results:**

| Scenario | Sustainable ROE | Justified P/B | Fair Value | vs ₹155 |
|----------|----------------|---------------|------------|---------|
| Bear | 25% | 4.2x | ₹50 | -68% |
| Base | 40% | 24.3x | ₹290 | +87% |
| Bull | 50% | 32.7x | ₹389 | +151% |
| **Implied** | **35%** | **13x** | — | — |

P/B-ROE verdict: **Market implying 35% sustainable ROE — already pricing in decline from 50%. If base case (40% ROE) holds, stock is cheap.**

**Synthesis:** The central question is whether GROWW can sustain 35-40% ROE as book value compounds. Given capital-light platform model + product diversification (MTF, AMC, loans), base case ROE >35% is plausible. This is a 15-25% CAGR compounder at ₹155, not a 5x.

---

### Example 2: JUSTDIAL (Asset-heavy + investments > market cap)

**Inputs:**
- FCF: ~₹400 Cr/yr | CMP: ₹523 | Book Value (incl. investments): ₹669/share
- Investments (FinancialMark): ₹5,703 Cr | Market Cap: ₹3,592 Cr | ROE: ~15%

**Special consideration:** JUSTDIAL is a SOTP (Sum-of-Parts) play. The operating business + investment portfolio must be valued separately.

**SOTP:**

| Component | Value |
|-----------|-------|
| Investments (FinancialMark, FDs, bonds) | ₹5,703 Cr (₹831/share) |
| Operating business (@ 10x FCF, bear) | ₹4,000 Cr (₹584/share) |
| Less: any tax/liquidity discount on investments | (₹1,500 Cr) |
| **SOTP fair value** | **₹1,200–₹1,400/share** |

**Current price ₹523 implies:** You buy ₹831 of investments for ₹523. The operating business is effectively **free (or negative cost)**. This is the floor case thesis.

**Standard DCF:** Not very useful here because operating FCF (~₹400 Cr) doesn't capture the investment portfolio value. P/B-ROE (ROE 15% → justified P/B ~1.0x, fair value ~₹523) correctly identifies floor value.

**Synthesis:** Pure DCF misses the thesis. SOTP + floor value analysis is the right framework. Exit triggers: delisting below ₹700 would be unfair value (fight it); above ₹700 is acceptable exit.

---

## India-Specific Notes

1. **Use Consolidated financials** — Standalone misses subsidiaries. Always Consolidated from Screener.in.
2. **P/E for growth stocks is misleading** — Use PEG (P/E ÷ growth rate). PEG < 1 is generally attractive.
3. **ROCE > ROE preference** — ROCE (return on capital employed) is harder to game than ROE (which can be inflated by leverage). We track ROCE as primary efficiency metric.
4. **Promoter holding matters** — Declining promoter holding (especially below 40%) is a red flag that no valuation model captures. Always overlay with governance check.
5. **Indian terminal growth = 5%** — India's nominal GDP is ~7% but company-level growth is mean-reverting. 5% is conservative but honest.
6. **Debt-funded ROE is a trap** — If ROE is high but ROCE is low, the company is using debt to inflate equity returns. Check: ROE - ROCE gap. If gap > 10%, it's leverage-driven.

---

## Growth Rate Anchoring Framework

*Why your growth assumption is the most important — and most often wrong — input in any DCF.*

---

### The Problem: Why Mechanical Declining Rates Fail

The standard DCF template goes something like: "20% growth in Year 1, declining linearly to 10% by Year 5, then 5% terminal." This is intellectually lazy, and it causes real analytical errors.

The problem is that a declining rate curve has a shape — and every company gets the same shape, regardless of what the business is actually doing. A company doubling its manufacturing capacity is not the same as a mature FMCG brand selling the same SKUs it did in 2018. Yet both get "20%→10%→5%" in the model. The result is systematic mispricing: high-growth, capital-expanding businesses get undervalued because the model assumes their growth rate must fall according to a generic curve, not according to the physical and commercial reality of their business.

**SHILCTECH is the proof case.** The old DCF used 12%→6% growth rates. It said: overvalued at ₹3,727. At that same moment, the business had an order book of ₹750-800 Cr against ₹737 Cr annual revenue, was actively doubling manufacturing capacity to 14,000 MVA by April 2027, and was operating in an industry (India T&D) growing 18-22% CAGR. A 12% base case growth assumption implies SHILCTECH is losing market share — which is the exact opposite of what the order book, the capex commitment, and the industry tailwind are telling you. The model was wrong because the inputs were wrong. The fix is not to tweak the curve; it is to anchor the growth rate to the business reality.

---

### The Anchoring Framework: Four Methods

#### Method 1: Capacity-Constrained Revenue Model

**(a) What it is:** Build revenue from the ground up. New capacity × utilization rate × average selling price = revenue ceiling. The growth rate is the *output* of this calculation, not the input.

**(b) Why this is the right anchor:** Manufacturing businesses are capacity-constrained in growth, not demand-constrained. If a company is building a plant that doubles output by FY27, growth in FY27-28 is physically bounded by that new capacity — it cannot suddenly revert to 10% just because the old DCF template says so. The constraint is the factory floor, not a spreadsheet curve.

**(c) When to use it:** Any manufacturer with announced expansion — SHILCTECH, KAYNES, EPACKPEB, SHAKTIPUMP, or any company where a concrete capex plan is publicly disclosed.

**(d) Worked example — SHILCTECH:**
- Current capacity: 7,500 MVA. Revenue: ₹737 Cr. Revenue per MVA = ₹737 Cr ÷ 7,500 = ₹9.8L per MVA.
- New capacity by April 2027: 14,000 MVA (87% volume increase).
- At 82% utilization (current implied rate): 14,000 × 0.82 × ₹9.8L = **₹1,127 Cr** revenue by FY28.
- Implied CAGR FY25→FY28: (1,127/737)^(1/3) - 1 = **15.3%** — and that is the *floor* for the base case at full capacity, not the ceiling. Near-term tailwind (industry 18-22%) pushes the base case higher.
- The old DCF's 12% growth assumption is below the capacity-implied floor. It was modelling market share loss without realising it.

---

#### Method 2: Order Book Coverage Ratio

**(a) What it is:** Order book ÷ annual revenue = revenue visibility in years. The rate at which new orders arrive (the book-to-bill ratio) drives the growth floor. Coverage ratio >1x means the next 12 months of revenue is already committed.

**(b) Why this is the right anchor:** An order book is a signed commitment from a customer. It is not a forecast; it is a contract. If a company has 2x annual revenue in its order book, the next 18-24 months of revenue is effectively certain (barring cancellations, which are historically rare in infrastructure). The DCF base case should start with the order book as its floor, not with an arbitrary declining growth assumption.

**(c) When to use it:** Project-based businesses where revenue recognition follows project execution — KERNEX (railway signaling orders), RAYMOND engineering (aerospace LTAs), EPACKPEB (pre-engineered building project orders).

**(d) Worked example — KERNEX:**
- Order book: ₹2,800 Cr. Annual revenue: ₹220 Cr. Coverage ratio: **12.7x**.
- Growth for the next 3 years is essentially mechanical — it is execution of the existing order book, not a forecast. The constraint is not demand; it is installation capacity.
- Bear case growth is NOT 10%. It is "how fast can they execute?" Given the 12.7x coverage, even the pessimistic scenario implies **40-60% CAGR for 2-3 years**. Below that, you are assuming order cancellations at massive scale, which requires a separate argument.

---

#### Method 3: Management Guidance + Expansion Signals

**(a) What it is:** When management gives explicit forward guidance (revenue growth %, capacity targets, order intake rate), use it as the base case. Apply a ~20% discount for the bear scenario and a ~20% premium for the bull scenario.

**(b) Why this is the right anchor:** Management has material non-public information that analysts don't — the live order pipeline, customer conversations, tender win rates, and their own cost structure. When a company commits ₹510 Cr to a new plant in Andhra Pradesh (RAYMOND aerospace) or ₹1,000 Cr to capacity expansion (KAYNES), that capex is itself a forward demand signal. Companies do not commit large capex into uncertain demand. They see the demand on their desk before they sign the construction contract.

**(c) When to use it:** Any company with explicit public guidance or significant capex announcements in the last 12 months. If management has put numbers on the table, use those numbers as the anchor.

**(d) Worked example — RAYMOND engineering:**
- RAYMOND guided approximately 30% revenue growth for the engineering division in FY26.
- Base case DCF should start at **30%**. Bear: **20%** (one-third haircut for execution delays). Bull: **40%** (guidance beat, which has been their track record).
- Using a generic declining curve from 20%→10% is not an independent analysis; it is ignoring public information.

---

#### Method 4: Industry TAM Growth Rate as the Floor

**(a) What it is:** The industry's own growth rate sets the floor below which a company growing faster than the industry should not fall, *unless* you are explicitly modelling market share loss. If the transformer industry is growing 18-20% and your company has an order book equal to 1x+ annual revenue, a 10% growth assumption is inconsistent — it implies the company is ceding share to competitors.

**(b) Why this is the right anchor:** A company growing below its industry's rate is losing market share by definition. If your thesis is that the company is well-positioned in a structural tailwind — which is the only reason to own it — then the base case growth cannot fall below the industry growth rate without a specific explanation for why share is being lost.

**(c) When to use it:** Every holding. For every stock, ask: "What is the industry growing at?" If your assumed growth is below that number, you are implicitly modelling market share loss. Be explicit about why.

**(d) Key India industry growth rates for reference:**

| Industry | CAGR Estimate | Key Drivers |
|----------|--------------|-------------|
| T&D / Transformers | 18-22% | RDSS scheme, RE 500GW target, data centers, grid modernisation |
| EMS / Electronics manufacturing | 20-25% | PLI schemes, China+1 sourcing shift |
| Pre-engineered buildings | 25-30% | Industrial capex, warehousing, data centers |
| Railway signaling | 30-40% | Kavach 34,000 km mandate |
| Aerospace precision components | 25-35% | OEM order backlogs, Make in India defence |
| AMC / Asset management | 15-18% AUM | SIP penetration, household financialisation |
| IT services (mid-cap) | 12-18% revenue | Digital transformation spend |

---

### Setting Margin Assumptions — Not Just Growth

Growth without margin discipline is half the analysis. Every DCF must have an explicit margin assumption with a stated rationale. Never assume margins stay flat or compress "arbitrarily." State the mechanism.

**Operating Leverage (margins expand with scale):** Fixed costs — plant depreciation, senior management, regulatory compliance — are absorbed over a larger revenue base as revenue grows. The unit economics improve. Expect this when: revenue is growing >20% AND the cost structure has meaningful fixed components. Examples: EPACKPEB (factory fixed overhead), KERNEX (signaling technology R&D already sunk).

**Mix Shift (margins expand if product mix improves):** Moving toward higher-value products changes the blended margin even if individual product margins are unchanged. SHILCTECH is shifting toward renewable/inverter-duty transformers, which carry higher margins than standard distribution transformers. RAYMOND aerospace (21% EBITDA) growing faster than auto components (14% EBITDA) causes blended margins to expand at the group level without any individual product improving.

**Commodity Risk (margins compress under pressure):** If raw materials are a major cost component and prices are volatile, margin compression is the honest bear case assumption. SHILCTECH's key inputs are copper, aluminium, and CRGO steel — all cyclical. Back-to-back ordering hedges execution-period risk but not multi-year commodity cycle risk. In the bear case for exposed manufacturers: model OPM compressing 1-2% from base.

**Pricing Power vs Competition (the honest check):** Ask directly — can this company raise prices without losing customers? SHILCTECH deliberately avoids government clients and serves private utilities → **Yes, strong pricing power**. EPACKPEB sells to both private developers and government contractors → **Mixed**. KERNEX provides Kavach signaling for which there is no alternative vendor → **High, near-monopoly**.

**Rule:** For every DCF in this system, explicitly state the margin assumption AND the one-sentence rationale. Format:

> "OPM 28% (down from 30%) because: copper prices likely elevated in FY27; back-to-back ordering limits but does not eliminate multi-year commodity cycle exposure."

---

### Selecting Terminal Growth Rate

The default of 5% (India nominal GDP) is the right answer for mature companies in competitive markets. It is the wrong answer for companies in structural, policy-mandated growth sectors.

The terminal growth rate should reflect the long-run growth of the industry the company operates in — not just the economy. India's RE target (500 GW by 2030), Kavach mandate (34,000 km of railways), and household financialisation are not cyclical trends that normalise to GDP. They are decade-long structural programmes. Companies at the centre of these programmes have a terminal growth rate argument above 5%.

| Sector | Suggested Terminal Growth | Rationale |
|--------|--------------------------|-----------|
| Power / T&D infrastructure | 7-8% | India electrification + RE integration is a 15-20 year structural theme, not a cycle |
| Defence electronics | 8-10% | Government mandate-driven (Kavach, ASAT, Make in India defence). Policy is the demand floor. |
| AMC / Financial services | 6-7% | India household financialisation still in early stages; above nominal GDP for 10+ years |
| IT services (mid-cap) | 5-6% | Competitive global market; terminal = GDP default is appropriate |
| Real estate | 5% | Cyclical; default terminal applies |
| Commodity manufacturers | 4-5% | Price-cycle dependent; conservative terminal is the right choice |

**Rule:** Justify your terminal growth rate in one sentence. If using anything above 5%, cite the specific structural driver that sustains above-GDP growth in perpetuity.

---

### Documentation Requirement

Every DCF in this system must include, for each scenario, a "Rationale" column explaining: (1) why this growth rate was chosen, (2) why this margin assumption, and (3) why this terminal growth rate. A number without a rationale is not analysis; it is a guess.

Use this column format in all thesis files:

```
| Scenario | Growth Rates | Rationale | OPM Assumption | Terminal g | Fair Value |
```

---

## Quality Score → Valuation Parameters (The Direct Link)

*Last added: 2026-03-21*

---

### Why Quality Must Connect to Valuation

Our Quality Score has five dimensions — MOAT, Management, Financials, Growth Runway, Valuation. But historically we've run the same DCF assumptions (12% discount rate, 5% terminal growth, 75% FCF conversion) regardless of whether the company scored 8/25 or 22/25. That's inconsistent: a wider moat means more durable cash flows, which means lower uncertainty, which means a lower required return. The valuation inputs *must* reflect what the quality analysis concluded.

Buffett/Munger never do a formal DCF — but their thinking is: "If I'm certain about the earnings 10 years from now, I can pay a higher multiple today." Certainty is worth money. This section systematises that intuition.

---

### Step 1 — Quality Grade → Valuation Method

Before picking parameters, pick the right method. Different quality levels require fundamentally different approaches:

| Grade | Score | Method | Why |
|-------|-------|--------|-----|
| **A** | 20–25 | **Owner Earnings multiple** | Certainty is high enough that you don't need a multi-year projection. Just pay a fair multiple on normalised owner earnings. DCF terminal value dominates anyway — skip the noise and go straight to the terminal. |
| **B** | 15–19 | **Quality-adjusted DCF** | Good business, quantifiable growth anchor (order book / capacity / TAM). Standard DCF structure works; adjust the three parameters below using the dimension scores. |
| **C** | 10–14 | **Graham margin-of-safety** | Uncertain execution, weak moat, or financial risk. Require ≥40% discount to intrinsic value. Use earnings yield floor: pay ≤6–7x owner earnings (≥15% earnings yield). Do not give credit for growth you cannot quantify. |
| **D** | <10 | **Asset / NAV value only** | Cannot forecast earnings with any confidence. Value what physically exists today. For operating businesses: EV/Revenue 0.5–1.5x at best. For asset plays: replacement cost minus debt. |

**The Buffett test (apply in sequence):**
1. Can I estimate owner earnings 10 years from now with >70% confidence? → Grade A method
2. Do I have a hard quantitative anchor for 5-year growth (order book, capacity plan, TAM)? → Grade B method
3. Is book value meaningful (asset-heavy, physical assets)? → P/B-ROE or Graham floor
4. Can I only value current assets? → Grade D, asset NAV only

---

### Step 2 — Quality Score Dimensions → DCF Parameters

For Grade B companies using DCF, each dimension score adjusts a specific input:

#### MOAT Score → Terminal Growth Rate

*Mechanism: A wider moat means the business can sustain above-GDP growth for longer before competition erodes returns. The terminal growth rate should reflect the durable competitive position, not just the GDP average.*

| MOAT Score | Adjustment to Sector Default Terminal g |
|------------|----------------------------------------|
| 5 | +2% (e.g. sector default 6% → use 8%) |
| 4 | +1% |
| 3 | ±0% (use sector default) |
| 2 | −1% |
| 1 | −2% (or floor at 3%) |

**Example:** KERNEX (MOAT 4/5) in railway signaling (sector default 8-10%). Apply +1% → terminal g = 9-10%. DREDGECORP (MOAT 2/5) in port infrastructure (sector default 5%) → terminal g = 4%.

#### Management Score → FCF / PAT Conversion Rate

*Mechanism: Good management allocates capital efficiently, avoids value-destructive acquisitions, and converts earnings to cash. Poor management overstates profits, builds working capital, or burns cash on unproductive capex.*

| Management Score | FCF / PAT Conversion |
|-----------------|---------------------|
| 5 | 90% |
| 4 | 82% |
| 3 | 75% (default) |
| 2 | 65% |
| 1 | 55% |

**Example:** BOSCHLTD (Management 4/5) → use 82% FCF conversion. SWANDEF (Management 2/5) → 65%; they have ₹2,505 Cr debt and negative OCF — actual conversion is negative, so 65% overstates it (use asset method instead, which is correct for Grade D).

#### Financials Score → Discount Rate

*Mechanism: Financial strength (low debt, positive FCF, healthy ROCE) reduces the probability of distress and earnings volatility. Lower risk deserves a lower required return.*

| Financials Score | Discount Rate |
|-----------------|---------------|
| 5 | 11% |
| 4 | 12% (default) |
| 3 | 13% |
| 2 | 14% |
| 1 | 15–16% |

**Example:** KERNEX (Financials 4/5) → 12%. SWANDEF (Financials 1/5) → 16% (or skip DCF entirely — Grade D).

#### Growth Runway Score → Projection Period

*Mechanism: A large, underpenetrated TAM or long order book means you can project growth with confidence for longer. A mature or shrinking TAM means your high-growth assumption runs out of runway faster.*

| Growth Runway Score | Explicit Projection Period |
|--------------------|---------------------------|
| 5 | 8 years |
| 4 | 6 years |
| 3 | 5 years (default) |
| 2 | 4 years |
| 1 | 3 years |

**Example:** EPACKPEB (Growth 5/5, India PEB penetration 15% vs 70% global) → 8-year projection. DREDGECORP (Growth 3/5) → 5 years, standard.

---

### Step 3 — Quick Parameter Lookup by Quality Score

For a Grade B company, use this table to set DCF inputs in one step:

| Total QS | Typical Grade | Discount Rate | Terminal g (above sector default) | FCF % | Projection Period |
|----------|--------------|---------------|-----------------------------------|-------|-------------------|
| 20–25 | A | Owner earnings multiple — skip DCF | | | |
| 17–19 | B+ | 11–12% | +1 to +2% | 82–90% | 6–8 yr |
| 14–16 | B / B– | 12% | ±0% | 75–82% | 5–6 yr |
| 10–13 | C+ / C | 13–14% | −1% | 65–75% | 4–5 yr |
| <10 | D | Asset value — skip DCF | | | |

---

### Owner Earnings Method (For Grade A Companies)

Buffett defines owner earnings as: **Net income + D&A − maintenance capex**. This is the cash the business *actually* generates for the owner each year, stripped of accounting noise.

**Valuation:** Owner Earnings × Justified Multiple = Fair Value

**Justified multiple for a Grade A business:**
```
Justified P/OE = 1 / (Required Return − Sustainable Growth)
              = 1 / (CoE − g)

Example: CoE = 12%, g = 8% (strong moat, structural sector)
Justified P/OE = 1 / (0.12 − 0.08) = 25x
```

| Quality Context | CoE | g | Justified P/OE |
|----------------|-----|---|----------------|
| A grade, strong moat, structural sector (e.g. AMC, defence EMS) | 11% | 8% | 33x |
| A grade, capital-light, moderate tailwind | 12% | 7% | 20x |
| B+ grade, good moat, industry tailwind | 12% | 6% | 17x |
| B grade, moderate moat | 13% | 5% | 13x |

**Why this is better than DCF for Grade A:** DCF forces you to project year-by-year cash flows, which introduces noise and fake precision. For a great business, the dominant value driver is the terminal value anyway (60–75% of total DCF value). Owner Earnings directly capitalises the terminal, cutting out 5 years of speculative projections.

---

### Grade C — Graham Margin-of-Safety Floor

For uncertain businesses (Grade C), do not give credit for growth. The floor value:

```
Graham Floor = Owner Earnings × (8.5 + 2g)     [Graham's formula, g in %, use 0 for uncertain]

At g=0 (no-growth assumption):
Graham Floor = Owner Earnings × 8.5  →  This is ~12% earnings yield
```

**Require a 40% margin of safety:** Buy only if CMP ≤ 60% of Graham Floor.

**Example — PATELSAIR (C+ 13/25):** Owner earnings ≈ ₹17 Cr. Graham Floor at g=0: ₹17 × 8.5 = ₹144. 60% of ₹144 = ₹86. Current CMP ₹219 is above Graham floor — not a Graham buy. But if you believe Q4 FY26 confirms FY25 was a timing issue (not structural), then normalised earnings are ₹30–35 Cr, Graham Floor = ₹255–298, 60% floor = ₹153–179. Entry below ₹175 with Q4 confirmation = margin of safety exists.

---

*Framework connections: Damodaran's "Quality-adjusted Cost of Capital" (damodaran.com), Greenwald's EPV (Columbia Business School), Buffett's owner earnings definition (1986 Berkshire letter)*

---

## Decision Integration

After running both models, the output feeds the **Quick Summary** section at the top of each thesis:

```
Buy / Add level  = DCF base case or P/B-ROE bear case (whichever is lower)
Hold range       = Between buy level and fair value
Exit trigger     = Fundamental (ROCE decline, promoter sale, etc.) — NOT price targets
```

**We do not use fair value as an automatic sell trigger.** Thesis breaks on fundamentals, not on the stock reaching a valuation target. The exit trigger is always a business or governance change, not "stock hit my DCF fair value."

---

## Code Reference

```python
from src.dcf_model import dcf_3_scenarios, reverse_dcf
from src.pb_roe_model import pb_roe_scenarios, implied_roe

# DCF
scenarios = dcf_3_scenarios(current_fcf=1824, shares_crores=628)
rev = reverse_dcf(current_price=155, current_fcf=1824, shares_crores=628)

# P/B-ROE
pb_scenarios = pb_roe_scenarios(book_value_per_share=11.9, current_price=155)
imp = implied_roe(current_price=155, book_value_per_share=11.9)
```

Full source: `src/dcf_model.py`, `src/pb_roe_model.py`

---

*Framework derived from: CFA Institute (DCF), Aswath Damodaran (Justified P/B), Anu Maheshwari/361 AMC (P/B-ROE for Indian markets)*
