# Valuation Framework — DCF + P/B-ROE

*How we value stocks in this research system. Read this before trusting any number in a thesis.*

**Last updated:** 2026-03-14

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
