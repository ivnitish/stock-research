# Advanced Micro Devices (AMD) — Investment Thesis

**Status:** OWNED
**Quality Score:** 16/25 (Grade B-)
**Classification:** Quality Compounder
**Last Updated:** 2026-04-04 | **CMP:** $197.75 | **Avg Cost:** $232.89 | **P&L:** -15% (-$35)
**Market Cap:** ~$320B | **Shares:** ~1.62B diluted
**Data Source:** StockAnalysis.com, MEXC/SiliconAnalysts AI market share data, Statista

> **Recommendation:** HOLD. Don't add at $197 — the FY2027 earnings recovery story is real
> (18x FY2027E EPS of $10.97) but requires aggressive operating margin expansion that is not yet
> proven. AMD is a legitimate #2 in the most important semiconductor cycle of the decade.
> The EPYC server CPU story is stronger and more defensible than the GPU story. Add below $160
> (15x FY2027E). Exit if FY2026 EPS misses by >15% — would signal AMD cannot close the
> CUDA moat gap.

---

## Summary Verdict

### Why this business?

AMD is not just a GPU challenger to NVIDIA — that framing misses the more important story. AMD's EPYC server CPUs have quietly taken 30%+ of the server CPU market from Intel, a business with high switching costs, multi-year procurement cycles, and margins that NVDA doesn't compete in at all. On top of that, AMD's MI300X and MI350 GPU accelerators have won real inference workloads at Microsoft Azure and Meta — not training, where NVIDIA's CUDA moat is near-impenetrable, but inference, where memory bandwidth matters more than ecosystem lock-in. The result is a company with $34.6B in revenue (+34% YoY), $6.7B net cash, and a data center business growing 32% annually — trading at 18x FY2027 earnings after a 15% correction from the user's average cost. This is not a screaming buy, but it is not a sell either. AMD is a high-quality #2 in a duopoly, and being #2 in semiconductors is a very good place to be.

### Strengths

1. **EPYC CPU is winning on fundamentals, not just price.** AMD EPYC has taken 30%+ server CPU market share from Intel. The performance-per-watt advantage is real and cloud providers (AWS Graviton notwithstanding) are actively deploying EPYC across data centers. Intel is in structural decline. This CPU moat is more durable than the GPU story.
2. **MI300X is competitive in inference.** For Large Language Model (LLM) inference (running models, not training them), the MI300X outperforms NVIDIA H100 on memory bandwidth — the key constraint for LLM inference. Microsoft, Meta, and Oracle have deployed MI300X at scale. This is not speculation; it is in production.
3. **Lisa Su is one of the best CEOs in tech.** She took AMD from near-bankruptcy in 2014 to a $320B company. Capital allocation decisions (Xilinx acquisition, EPYC roadmap) have been consistently correct. Management execution risk is low.
4. **Revenue CAGR is exceptional.** $16.4B (FY2021) → $34.6B (FY2025) — 2.1x in 4 years. Data center revenue alone hit $16.6B in FY2025 (+32% YoY). FY2026 analyst consensus: $47B (+36%).
5. **$6.7B net cash, low debt.** Balance sheet is clean. No financial distress risk even in a semiconductor downturn.

### Concerns

1. **CUDA ecosystem is NVIDIA's real moat — and AMD cannot replicate it easily.** NVIDIA's dominance in AI training is not about hardware specs — it's about CUDA, the software layer that every AI researcher and model developer has used for 15 years. Switching to ROCm (AMD's equivalent) requires rewriting code, retraining teams, and re-optimising models. Hyperscalers will use AMD where it wins on specs (inference, memory bandwidth) but will default to NVIDIA for training indefinitely.
2. **Operating margin is too low for a semiconductor company.** At 10.7% operating margin on $34.6B revenue, AMD leaves enormous value on the table vs NVIDIA's 60%+ operating margins. Xilinx integration costs and R&D investment depress margins now, but the FY2026 EPS jump from $2.65 to $6.72 (+153%) implies massive margin expansion that has not yet been demonstrated.
3. **Custom silicon from hyperscalers is the real long-term threat.** Google (TPU), Amazon (Trainium/Inferentia), Microsoft (Maia), Meta (MTIA) are all building custom AI chips. As these mature, they reduce dependence on both NVIDIA and AMD. AMD's GPU upside is constrained not just by NVDA but by the hyperscalers themselves.
4. **Valuation requires execution.** At $197, you're paying 74x trailing FY2025 EPS ($2.65). The bull case is entirely contingent on FY2026-27 EPS delivery. If margins disappoint, the stock re-rates sharply.
5. **PC/gaming segment is a drag.** AMD's consumer GPU (Radeon) and PC CPU (Ryzen) businesses face intense competition from Intel on CPU and NVIDIA on GPU. Margins are lower, growth is slower. This half of AMD dilutes the data centre story.

### The Compounding Equation

AMD has two compounding engines with different quality levels:

**Engine 1 — EPYC (high quality):** Intel server CPU market share was ~90% in 2018. It is ~65% today. AMD EPYC has taken ~30% share in 7 years and the trajectory continues. Cloud providers switching to EPYC save 20-30% on compute costs at equivalent performance. Each generation (Genoa, Bergamo, Turin) widens the performance gap. Once a data centre is deployed with EPYC, the switching cost back to Intel is enormous (re-certification, re-procurement, re-testing). This is a 5-7 year runway of continued share gains at improving margins.

**Engine 2 — AI GPU (lower quality, high optionality):** AMD's share of the AI accelerator market is 5-8% vs NVIDIA's 80-90%. The upside is significant — every 5pp of share gain at this market scale is billions in revenue. But CUDA lock means AMD must win on specific workload advantages (inference, memory bandwidth), not general AI training. The trajectory is positive but the ceiling is lower than the GPU revenue growth rate suggests.

Incremental ROIC: AMD deployed ~$7B in annual R&D over FY2023-25. Revenue grew $11.9B from FY2023→FY2025. Incremental R&D ROIC ≈ 170% — extreme, but semiconductor R&D is lumpy. More useful: FCF went from $1.1B (FY2023) to $6.7B (FY2025) — 6x in 2 years. The operating leverage is beginning to show.

### What does the market think — and where do I disagree?

At $197 and 74x trailing PE, the market is pricing in significant earnings growth but has moderated expectations after the post-2023 AI boom re-rated the stock from $60 to $230 then back to $197. Consensus: AMD is a buy at 32x FY2026E ($6.72) with a $261 price target.

My disagreement: I'm less certain on the EPS growth trajectory. Going from $2.65 (FY2025) to $6.72 (FY2026) requires operating margin to nearly double. AMD has not demonstrated this before. The EPYC story is solid; the GPU/EPS acceleration story requires a "show me" quarter. At $197, the risk/reward is roughly balanced — not a compelling add.

Reverse DCF: at $197, the market implies ~25% revenue CAGR and ~15% long-term operating margins. The revenue CAGR is plausible; the margin is the question.

### Multi-Bagger Math

| Scenario | FY2027 EPS | PE | Per Share | Multiple from $197 | Probability |
|----------|-----------|----|-----------|--------------------|-------------|
| Bear | $6.50 (margins disappoint) | 15x | $97 | 0.5x | 20% |
| Base | $10.97 | 18x | $197 | 1.0x (flat) | 50% |
| Bull | $12.00 (upside on MI350) | 22x | $264 | 1.3x | 30% |

**Probability-weighted: ~$175** — slightly below CMP. Not a multi-bagger from here. A Quality Compounder hold.

The math is clear: at $197, AMD needs to deliver on very aggressive EPS estimates just to stay flat. The upside is limited relative to the risk. This is a HOLD, not an ADD.

### When do I sell?

1. FY2026 EPS misses analyst consensus ($6.72) by more than 15% — signals margin expansion thesis is broken
2. EPYC server CPU market share stops growing for 2 consecutive quarters — the more defensible moat failing
3. A major hyperscaler (Microsoft, AWS, Google) publicly announces it is reducing AMD GPU deployments in favour of custom silicon
4. Lisa Su departure — single most important management risk

### Where does this rank?

Vs NVDA ($183, A · 22/25): NVDA is the superior business — CUDA moat is unbreachable, margins are 3-4x higher, revenue growth is faster. If forced to choose one AI chip stock, NVDA wins. AMD is the cheaper, higher-risk alternative for those who believe the CUDA monopoly will erode.

Vs MSFT ($370, A · 20/25): MSFT is a safer, more diversified compounder. AMD is a purer AI semiconductor bet with more volatility and more upside in a bull case.

### Action Table

| Level | Price | Action |
|-------|-------|--------|
| Exit | Above $250 | Near analyst target — take profits on this small position |
| Hold | $160–250 | Current range. Don't add, don't exit. |
| Add small | $130–160 | 15x FY2027E — better risk/reward |
| Strong buy | Below $130 | 12x FY2027E — bear case priced in, asymmetric upside |

---

## Section 1 — Business Summary

**Four segments:**
- **Data Center:** $16.6B revenue FY2025 (+32% YoY). EPYC server CPUs + Instinct MI300/350 GPU accelerators. Fastest growing, highest margin segment.
- **Client (PC CPUs):** ~$7B. Ryzen processors for laptops/desktops. Competitive with Intel.
- **Gaming (GPUs):** ~$5B and declining. Radeon GPUs face NVIDIA dominance in consumer market.
- **Embedded (Xilinx FPGAs):** ~$6B. Acquired Xilinx 2022 for $49B. Industrial, automotive, telecom. High margin but cyclical.

**Key products:** EPYC Turin (server CPU, 4th gen), MI300X/MI350 (AI GPU accelerator), Ryzen AI (laptop CPU with NPU).

---

## Section 2 — Quality Scorecard

| Dimension | Score | Evidence |
|-----------|-------|---------|
| MOAT | 3/5 | EPYC CPU moat is real (30% server share, switching costs). GPU moat is weak — CUDA prevents AMD from winning training workloads. Xilinx FPGA adds a third moat in embedded/industrial. |
| Management | 4/5 | Lisa Su — arguably best semiconductor CEO outside of Jensen Huang. Turned AMD around from near-zero. Xilinx acquisition was well-executed. |
| Financials | 3/5 | Revenue growing fast, FCF $6.7B, net cash $6.7B. But operating margin 10.7% is far below NVDA/QCOM peers. EPS acceleration requires unproven margin expansion. |
| Growth Runway | 3/5 | Data center CPU/GPU is a real multi-year tailwind. But CUDA lock caps GPU upside; custom ASIC competition is long-term headwind. EPYC runway is 5+ years. |
| Valuation | 3/5 | 74x trailing PE (expensive), but 18x FY2027E (reasonable if EPS delivers). $261 analyst target = 32% upside. Not cheap, not expensive at current levels. |
| **Total** | **16/25** | **Grade B- — Quality Compounder, not a multi-bagger from current price** |

---

## Section 3 — Compounding Engine Q&A

**Q: Can AMD actually take NVIDIA's GPU market share?**
In training workloads — unlikely in the 5-year horizon. CUDA has 15 years of momentum. Switching from NVIDIA to AMD for training means rewriting model code, retraining engineers, and re-optimising every workflow. The productivity cost is enormous. For inference (running models at scale), AMD has a real shot because inference is more commodity-like — the primary constraint is memory bandwidth, where MI300X leads H100.

**Q: Is the EPYC story more durable than the GPU story?**
Yes, significantly. Server CPU procurement is a 3-5 year cycle. Once a hyperscaler certifies EPYC for its fleet, it stays for years. Intel's Xeon roadmap has consistently disappointed while EPYC Turin leads on performance-per-watt. Every 5pp of server CPU share gain from Intel adds ~$1.5-2B in high-margin annual revenue. This is the underappreciated engine.

**Q: Why is operating margin only 10.7% if AMD is winning?**
Two reasons: (1) Xilinx acquisition ($49B) generates ~$5-6B annual goodwill/intangibles amortisation that hits operating income. (2) AMD is investing heavily in R&D ($6B+/year) to compete with both NVIDIA on AI and Intel on CPUs simultaneously. As Xilinx amortisation rolls off and R&D scales, operating margins should expand toward 20-25% by FY2028.

---

## Section 4 — Key Financial Metrics

### Income Statement

| Metric | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 | FY2026E | FY2027E |
|--------|--------|--------|--------|--------|--------|---------|---------|
| Revenue ($B) | $16.4 | $23.6 | $22.7 | $25.8 | $34.6 | $47.0 | $67.2 |
| Revenue growth | — | +44% | -4% | +14% | +34% | +36% | +43% |
| Gross Margin | 48.3% | 44.9% | 46.1% | 49.4% | 49.5% | — | — |
| Operating Margin | 22.2% | 5.4% | 1.8% | 7.4% | 10.7% | ~14% | ~16% |
| Net Income ($B) | $3.2 | $1.3 | $0.8 | $1.6 | $4.3 | — | — |
| EPS (diluted) | $2.57 | $0.84 | $0.53 | $1.00 | $2.65 | $6.72E | $10.97E |
| FCF ($B) | $3.2 | $3.1 | $1.1 | $2.4 | $6.7 | — | — |

### Balance Sheet (FY2025)

| Item | Value |
|------|-------|
| Cash + Investments | $10.6B |
| Total Debt | $3.8B |
| Net Cash | $6.7B |
| Shareholders' Equity | $63.0B |
| Net Cash per Share | ~$4.10 |

### Valuation (CMP $197.75)

| Multiple | Value | Context |
|---------|-------|---------|
| Trailing PE | 74x | Distorted by low FY2025 EPS |
| Forward PE (FY2026E) | 29x | Requires margin expansion delivery |
| Forward PE (FY2027E) | 18x | Reasonable if EPS $10.97 materialises |
| EV/Revenue (FY2025) | ~9x | Premium to market, fair for growth rate |
| Analyst avg target | $261 | +32% upside; 33 analysts, "Buy" consensus |

---

## Section 5 — Outlook

**FY2026:** Revenue $47B (+36%). EPS $6.72 (+153%). The EPS jump requires operating margin to expand from 10.7% to ~14%. Key drivers: Xilinx amortisation declining, Data Center mix improving (higher margin), MI350 ramp. This is the "show me" year.

**FY2027:** Revenue $67B (+43%). EPS $10.97 (18x PE at current price = $197). If AMD hits this, the stock is effectively flat from today — all the upside is priced in. This is why it's a HOLD, not an ADD.

**Long-term:** AMD's ceiling depends on whether ROCm can close the gap with CUDA. If it does (5-10 year timeframe), GPU margins expand significantly and AMD's data center segment could approach $30-40B. If it doesn't, AMD wins on inference/EPYC but stays structurally capped at 8-12% AI accelerator share.

---

## Section 6 — Competitive Landscape

| Competitor | Segment | Position vs AMD |
|-----------|---------|----------------|
| **NVIDIA** | AI GPU (training) | Dominant — CUDA moat is near-impenetrable for training. AMD is competitive on inference. |
| **Intel** | Server CPU | Losing share consistently. AMD EPYC Turin leads on performance-per-watt. Intel is structural headwind for AMD. |
| **Google TPU / AWS Trainium / MSFT Maia** | Custom AI ASIC | Long-term threat — hyperscalers reducing merchant GPU dependence. 5+ year risk, not immediate. |
| **Qualcomm / ARM** | Client CPU | Competing in laptop CPUs. Not a data centre threat. |

---

## Section 7 — Risks

1. **EPS misses FY2026 — most likely near-term risk.** Going from $2.65 to $6.72 EPS requires operating margin to jump from 10.7% to ~14%. If margin expansion is slower, EPS could print $4-5 → stock re-rates to $80-100 on trailing basis. This is the key number to watch in Q2/Q3 2026 earnings.
2. **Custom ASIC displacement.** Google, Amazon, Microsoft are all building proprietary AI chips. Long-term (5-7 years), this reduces the total available market for AMD GPUs in training and inference.
3. **CUDA moat never erodes.** If hyperscalers never switch from NVIDIA to AMD for training at scale, AMD's GPU upside is permanently capped at inference workloads (~20-25% of total AI chip demand).
4. **Gaming GPU decline.** Radeon continues losing share to NVIDIA in consumer GPUs. If this segment continues shrinking, it drags blended margins and creates earnings noise.

---

## Section 8 — Exit Triggers

1. FY2026 EPS misses $6.72 by >15% (prints below ~$5.70)
2. EPYC market share stalls — Intel/ARM regains server CPU ground
3. Major hyperscaler publicly reduces AMD GPU commitment
4. Lisa Su departure

---

## Section 9 — Review Schedule

- **Q2 FY2026 earnings (Jul 2026):** First real test of operating margin expansion toward 14%. Key number.
- **FY2026 full year (Jan 2027):** Does EPS hit $6.72? Does data center grow 35%+? Go/no-go decision.

---

## Section 10 — Decision History

| Date | Action | Price | Reasoning |
|------|--------|-------|-----------|
| (prior) | BUY | $232.89 | 1 share — tracking position |
| 2026-04-04 | HOLD | $197.75 | Thesis initiated. Not an add at current price. Wait for $160 or FY2026 earnings confirmation. |

---

## Section 11 — Research Log

### 2026-04-04 — Initial Thesis

**Source:** StockAnalysis.com (financials), SiliconAnalysts (AI market share), Statista (data center revenue)

Key findings:
- FY2025: Revenue $34.6B (+34%), Net Income $4.3B, EPS $2.65, FCF $6.7B, Net Cash $6.7B
- Data Center $16.6B (+32%) — EPYC + MI300X both growing
- Market share: NVDA 80-90% AI GPU, AMD 5-8%. AMD has 30%+ server CPU share vs Intel.
- FY2026E: Revenue $47B, EPS $6.72 (+153%) — requires operating margin jump to ~14%
- FY2027E: Revenue $67B, EPS $10.97 — at 18x = $197. Stock at breakeven on FY2027 basis from today.
- Quality Score: 16/25 Grade B-. Classification: Quality Compounder.
- Verdict: HOLD. Add below $160 (15x FY2027E). Exit above $250 (near analyst target).
- Key insight: EPYC CPU story > GPU story in durability. Market focuses on NVDA/GPU narrative but EPYC is the more defensible compounding engine.

---

## Version History

| Version | Date | Summary |
|---------|------|---------|
| v1 | 2026-04-04 | Initial thesis — OWNED, HOLD. 16/25 Grade B-, Quality Compounder. |
