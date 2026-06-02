---
title: "The AI Supercycle"
subtitle: "An Investor's Field Guide to the Largest Capex Wave in Modern History"
author: "Research Note — Multi-Bagger Framework Lens"
date: "June 2026"
geometry: margin=2cm
fontsize: 11pt
mainfont: "Georgia"
colorlinks: true
linkcolor: "blue"
urlcolor: "blue"
toc: true
toc-depth: 2
---

\newpage

# Executive Summary

The AI buildout in 2025–2026 is the largest concentrated capital expenditure cycle in technology history, and likely in any industry since the post-war US highway and electrification programmes. In a single calendar year, the five US hyperscalers — Amazon, Alphabet, Meta, Microsoft, and Oracle — are committing roughly \$700–725 billion to capex. That is more than the entire annual GDP of Switzerland, spent in twelve months, by five companies, on a single thesis.

This is not a marketing claim. It is the visible, contracted spending. Add the parallel buildouts now committed in India (Reliance \$110bn, Adani \$100bn, Tata Group multi-GW), the sovereign AI investments in the Gulf and Europe, and the second-order capex by power, cooling, networking, and packaging suppliers, and the cycle is meaningfully bigger than even the headline number suggests.

A capex cycle of this magnitude does one of two things. Either it earns a return on the money invested that justifies it — in which case the supply chain feeding it (compute, memory, packaging, power, grid equipment, real estate) compounds for a decade — or it does not, in which case the next two to three years see escalating write-downs starting with the weakest balance sheets. The bull and bear cases share the same set of facts; they differ in their estimate of how long the gap between capex and revenue will persist.

This report is structured as a layer-by-layer field guide. The goal is not to predict whether the supercycle "succeeds" — that question is unanswerable in the present tense. The goal is to identify which physical layers of the buildout are most constrained, which have the strongest pricing power, which are most exposed to the bear case, and where the investable opportunity sits for a long-horizon equity investor.

The compressed thesis is this:

1. The capex is real, the demand is real, and the constraint is no longer demand — it is the supply of compute, memory, advanced packaging, and electricity. Multiple layers of the stack are now sold out through end-2026.
2. The biggest gap between expectation and reality sits in the application layer. Foundation models and consumer AI products are scaling revenue fast, but enterprise GenAI deployments are converting to measurable P&L impact at a much lower rate than the capex commitment implies. This is the single most important variable to track.
3. India is positioning to capture the second-largest piece of the global AI infrastructure build, with \$310bn+ of committed capex from Reliance, Adani, and Tata over the next decade. The cost-advantage from co-locating data centres with captive renewable energy assets is structural and meaningful.
4. The investable layers, ranked by quality of business model and durability of pricing power, are: advanced packaging and HBM memory (most constrained), gas turbines and grid equipment (multi-year backlog, oligopoly), foundation model compute (Nvidia, with a widening but real moat), Indian data centre operators (capacity buildout phase), and last the application layer (highest revenue growth but lowest visibility on terminal economics).

\newpage

# Section 1 — What is the AI Supercycle?

A supercycle, in commodity and industrial language, refers to a multi-decade demand expansion in which sustained capital investment lifts the trend line of an entire industry above its historical norm. The 1950s–1970s post-war industrialisation, the 1980s–2000s consumer electronics build, and the 2003–2014 China commodity demand cycle are the canonical examples. Each was characterised by three things: a structural change in end-demand (war reconstruction, globalisation, urbanisation), a long lead time on supply (factories, refineries, mines), and a price signal — sustained inflation in the constrained input — that pulled fresh capital into the cycle until supply caught up.

The AI supercycle has the same shape. The end-demand change is the move from rule-based software to learned software — a shift in how every business processes information that creates a per-unit compute requirement orders of magnitude higher than the previous generation of digital infrastructure. The long lead time sits in the supply of advanced semiconductor packaging (24+ months to build new CoWoS capacity), high-bandwidth memory (18–24 months from wafer start to qualified HBM stack), grid-scale electricity (3–7 years to build new gas-fired generation, 8–12 for nuclear), and physical data centre real estate (24–48 months for a hyperscale build).

The price signal is now everywhere in the supply chain. HBM3E pricing has been raised approximately 20% for 2026 orders against a baseline of strong AI accelerator demand — and this is an unusual move because new technology generations normally bring prices down. Nvidia data centre revenue grew from roughly \$18bn in Q4 FY24 to a record \$62.3bn in Q4 FY26, with the next quarter (Q1 FY27) printing \$75.2bn, up 92% year-on-year. Gas turbine orders at GE Vernova and Siemens Energy are running multi-year backlogs. The CoWoS packaging capacity at TSMC is expanding from 35,000 wafers per month in late 2024 to a planned 120,000–140,000 by end-2026, an 80% compound annual growth rate, and is still sold out.

The dollar number that captures the scale: hyperscaler capex in 2026 is roughly \$700 billion, up from \$410 billion in 2025 and \$220 billion in 2023. Three-year growth: 3.2x. For comparison, total US private non-residential construction spending — across every sector of the economy — runs around \$1.1 trillion per year. The Big Five hyperscalers, on AI alone, will spend close to two-thirds of that in 2026.

Whether the AI supercycle eventually produces returns commensurate with this capex is the central debate of the cycle. But the fact of the cycle — the physical buildout, the contracted spending, the supply constraints — is not a debate. It is happening, in concrete and steel and silicon, and the equity investor's job is to identify which layers of the cycle have durable economics and which are commodity passthroughs.

\newpage

# Section 2 — The Capex Engine: Hyperscaler Spending in 2026

## 2.1 The Headline Number

The Big Five US hyperscalers — Amazon, Alphabet (Google), Meta, Microsoft, and Oracle — have guided 2026 capex as follows:

| Company   | 2025 Capex | 2026 Capex Guidance | YoY Growth |
|-----------|-----------|---------------------|------------|
| Amazon    | \$125 bn  | \$200 bn            | +60%       |
| Alphabet  | \$91 bn   | \$175–185 bn        | +98%       |
| Meta      | \$72 bn   | \$115–135 bn        | +74%       |
| Microsoft | \$90 bn   | \$110–120 bn        | +28%       |
| Oracle    | \$32 bn   | \$80+ bn            | +150%      |
| **Total** | **~\$410 bn** | **~\$700–725 bn** | **+72%**   |

Source: Company guidance Q4 2025 / Q1 2026 earnings; Tom's Hardware, CNBC, Futurum aggregations.

Two important features of this table are worth highlighting. First, the growth rate is accelerating, not decelerating, in 2026 — the standard interpretation of "late-cycle capex" expects deceleration as marginal returns compress. That is not yet visible. Second, the absolute numbers are now large enough that meaningful slices of them are no longer chip-related: Microsoft has stated that roughly \$25bn of its 2026 capex is direct component price inflation, not additional volume.

## 2.2 Where the Money Actually Goes

The composition of hyperscaler AI capex has shifted meaningfully over the last 24 months. The popular framing — that hyperscaler capex is mostly Nvidia GPUs — is no longer accurate. Industry estimates now suggest that GPU and accelerator silicon represents 30–40% of the capex bill. The remaining 60–70% is land, data centre construction, mechanical and electrical infrastructure (cooling, power distribution, switchgear), networking equipment, and increasingly direct power infrastructure investment — i.e., the hyperscalers are now signing long-term power purchase agreements and in some cases directly funding generation assets.

This composition matters because it determines which equity baskets benefit. A capex dollar spent on a Nvidia GB200 system flows to Nvidia, TSMC, SK Hynix, and Foxconn. A capex dollar spent on a 200 MW data centre flows to construction firms, electrical equipment vendors (GE Vernova, ABB, Schneider, Eaton), cooling system specialists (Vertiv, Munters), and the grid utility. A capex dollar spent on power generation flows to gas turbine OEMs (GE Vernova, Siemens Energy, Mitsubishi Heavy), nuclear operators (Constellation, Vistra, NuScale, Oklo), and natural gas producers.

## 2.3 Funding the Buildout

The bear case rests partly on the cash flow implications of this spend. The bull case rests on the fact that the hyperscalers can afford it. Both are partially correct. Among the Big Five, four of the companies (excluding Oracle) can fund their 2026 capex entirely from operating cash flow with modest cushion. Oracle is the structural outlier: it has committed \$80bn+ of capex against a much smaller operating cash flow base, and is therefore raising substantial debt to fund the build. Oracle's leverage and the quality of its anchor customers (OpenAI, principally) is the single most concentrated bet on AI capex by a public company today.

The cash impact is real even for the cash-generative names. Free cash flow at the Big Four has compressed sharply in late 2025 and early 2026 as capex absorbs a rising share of operating cash flow. For Meta in particular, the gap between operating cash flow and capex has narrowed to the point that any meaningful slowdown in advertising revenue would put the company in net cash outflow at the operating level. This is a real risk, and one of the cleaner near-term signals to watch.

\newpage

# Section 3 — The Semiconductor Stack: Compute, Memory, Packaging

## 3.1 Compute: Nvidia and the Architecture Cadence

Nvidia data centre revenue trajectory:

| Quarter      | DC Revenue  | YoY    |
|--------------|-------------|--------|
| Q4 FY25      | \$35.6 bn   | +93%   |
| Q1 FY26      | \$39.1 bn   | +73%   |
| Q2 FY26      | \$41.1 bn   | +56%   |
| Q3 FY26      | \$51.0 bn   | +75%   |
| Q4 FY26      | \$62.3 bn   | +75%   |
| Q1 FY27      | \$75.2 bn   | +92%   |

Source: Nvidia 8-K filings, Q4 FY26 and Q1 FY27 CFO commentary.

The forward visibility is now extraordinary. Nvidia's CFO has disclosed \$500 billion in Blackwell and Rubin revenue visibility from the start of calendar 2025 through end of calendar 2026 — i.e., a single product family generating half a trillion dollars in revenue over a two-year period, with most of that backlog already booked. Blackwell systems are sold out through mid-2026. Rubin is on schedule for H2 calendar 2026 ramp.

The competitive position is the most important question. The cheap interpretation is "Nvidia has a temporary monopoly on training and inference; AMD, custom silicon, and Chinese alternatives will erode it." The first-principles interpretation is different. Nvidia's moat is not the GPU; it is the combination of CUDA software stack, NVLink interconnect, the system-level integration that makes a GB200 NVL72 rack work as a single coherent training cluster, and increasingly the networking layer (InfiniBand and Spectrum-X Ethernet). Custom accelerators (Google TPU, Amazon Trainium, Meta MTIA) are real and growing, but they remain optimised for the home buyer's workload — not a substitute for general-purpose AI compute that the rest of the market needs.

The honest read on Nvidia: the moat narrows in inference (where margins are already lower and competitive entrants more capable), but widens in training (where rack-scale system integration is harder to replicate than people think). Margin compression from a 75% gross margin peak is the base case, but to 60–65%, not to 40%.

## 3.2 Memory: The Tightest Layer in the Stack

High-bandwidth memory (HBM) is structurally the most supply-constrained layer in the AI stack today, and the layer where pricing power is most asymmetric.

HBM market share, mid-2026:

| Supplier  | Market Share | Position                            |
|-----------|--------------|-------------------------------------|
| SK Hynix  | 50–55%       | Leader; first to ship HBM4 samples  |
| Samsung   | 35–40%       | Closing gap; first HBM4 shipments Q1 2026 |
| Micron    | 5–10%        | Smallest but growing share          |

Source: TrendForce, Presenc AI HBM Market Share research.

The pricing dynamic is the more important story. HBM3E prices were raised approximately 20% for 2026 orders despite the simultaneous ramp of HBM4. This is unusual — new-generation chips normally bring down prices on the prior generation. The interpretation: demand is so much higher than the supply ramp that even with HBM4 entering the market, there is no surplus capacity for HBM3E to compete for. Hyperscalers have effectively locked up the 2026 production of all three suppliers.

For an Indian investor, none of the HBM suppliers are listed on Indian exchanges. SK Hynix is listed in Korea (KRX: 000660), Samsung is listed in Korea (KRX: 005930), and Micron is listed in the US (NASDAQ: MU). SK Hynix in particular has crossed \$1 trillion in market capitalisation in 2026 — a meaningful re-rating from where the company traded pre-AI cycle.

## 3.3 Packaging: The Bottleneck Layer

The most under-appreciated layer in the AI hardware stack is advanced packaging — the process by which GPU dies, HBM stacks, and interconnect substrates are assembled into the finished accelerator. TSMC's CoWoS (Chip-on-Wafer-on-Substrate) is the dominant technology, and capacity has been the single hardest physical bottleneck in the entire supply chain for 18 months running.

CoWoS capacity expansion:

| Period       | Capacity (wafers/month) |
|--------------|-------------------------|
| Late 2024    | ~35,000                 |
| End 2025     | ~80,000                 |
| End 2026     | 120,000–140,000         |

Growth rate: ~80% CAGR. Still sold out. TSMC has reportedly outsourced some packaging steps to ASE Technology and Amkor to relieve the bottleneck, and ASE expects advanced packaging revenue to double in 2026.

TSMC's 2026 capex is \$56 billion, of which 10–20% is dedicated specifically to packaging. The implication: the company is now investing in packaging at a rate that would have been considered absurd by 2022 standards, and demand still exceeds supply.

For Indian exposure, the most direct play is through Tata Electronics, which is building India's first OSAT (outsourced semiconductor assembly and test) facility in Assam — a packaging-focused plant. This is not listed equity yet but is part of the Tata Sons consolidated entity. Closer to listed: Kaynes Technology (KAYNES) and Dixon Technologies (DIXON) have stated intent to participate in the Indian semiconductor packaging ecosystem, though current revenue contribution is minimal.

## 3.4 Equipment: ASML and the EUV Chokepoint

ASML's position is structurally strong but the 2026 read is more nuanced. TSMC has confirmed it will not deploy ASML's high-NA EUV lithography machines through at least 2029, which removes the principal customer-funded ramp for the high-NA product line. ASML's revenue target of €60bn by 2030 now depends on Samsung and Intel adoption of high-NA, neither of which approaches TSMC's volume.

The interpretation: ASML remains a structurally protected monopoly in standard EUV (essential for every AI accelerator), but the marginal upside from high-NA is delayed. This is a moat-intact-but-growth-deferred situation, and the multiple is responding accordingly.

\newpage

# Section 4 — The Power Problem: Grid, Gas, Nuclear

## 4.1 The Physical Constraint

The single most under-appreciated constraint on the AI supercycle is electricity. By IEA estimates, global data centre power consumption will approach 1,050 TWh by 2026 — if data centres were a country, they would rank as the fifth largest electricity consumer in the world, between Japan and Russia. In the US specifically, the Department of Energy projects data centres could consume up to 12% of total US electricity by 2030, up from roughly 4% today.

This translates into a physical requirement of approximately 90–100 GW of incremental power demand globally by 2030, concentrated in a small number of geographies (Virginia, Oregon, Ireland, the Nordics, and now increasingly Texas, Arizona, and parts of India). The grid in most of these locations was not built for this load growth profile. New generation capacity is being added, but lead times are long — 3–5 years for a new gas-fired plant, 8–12 years for a nuclear unit (excluding SMR designs which are unproven at commercial scale).

The economic consequence: power has become the binding constraint on data centre deployment. Reports of hyperscalers signing 20-year power purchase agreements at high fixed prices, paying for grid upgrades themselves, and in some cases directly funding generation capacity are now common. This is a structural transfer of value from the data centre operator to the power generator.

## 4.2 Gas Turbines: The Near-Term Winner

The fastest path to incremental baseload generation for AI data centres is natural gas combined-cycle generation. This is why gas turbine OEMs are the cleanest near-term play on AI power demand.

GE Vernova Q1 2026 highlights:
- Backlog grew by more than \$13 billion quarter-over-quarter
- Electrification segment booked \$2.4 billion in equipment orders for data centres in Q1 alone — more than all of 2025
- Combined gas turbine backlog and slot reservation agreements expected to reach 110 GW by end of 2026
- Electrification revenue projected to grow 44% in 2026 to \$13.9 billion
- Data centre-related electrification orders expected to grow 29% YoY to \$24.8 billion in 2026

The three companies that dominate the global gas turbine market — GE Vernova, Siemens Energy, and Mitsubishi Heavy Industries — collectively control more than 70% of production capacity. All three have multi-year order backlogs and have publicly stated they cannot meet demand. This is an oligopoly with pricing power, capacity expansion lead times of 18–36 months, and a customer base (hyperscalers, utilities) that is highly capable of paying.

## 4.3 Nuclear: The Long-Term Bet

The interesting structural development in 2025–2026 is the rehabilitation of nuclear energy as the preferred long-term baseload for AI data centres. The case is clean: 24/7 reliability, carbon-free, capable of being colocated with a data centre campus, and politically less contested today than at any point in 25 years.

The visible signals:
- Constellation Energy signed a 20-year power purchase agreement with Meta from its Clinton Clean Energy Center, with evaluation of an SMR at the site
- Microsoft restarted the Three Mile Island plant under a 20-year agreement with Constellation
- Amazon acquired Talen Energy's nuclear-adjacent Cumulus data centre campus
- GE Vernova and Hitachi are commercialising the BWRX-300 SMR; the first commercial unit is scheduled for Ontario in 2029
- Oklo, Kairos, TerraPower, and NuScale are advancing alternative SMR designs at various stages

The SMR market is small today (\$6.9bn in 2025) but the growth rate to \$13.8bn by 2032 is the conservative scenario. The market-moving scenario is one in which a handful of SMR designs achieve commercial deployment at scale by 2030–2032, which would lock in a structural energy supply for the AI supercycle and create a durable equity opportunity in SMR operators and OEMs.

For Indian exposure, the play is limited. India's nuclear programme has historically been state-controlled through NPCIL. The 2025 budget announcement of a Bharat Small Modular Reactor (BSMR) programme opens this slightly, but commercial private participation remains uncertain. Companies like L&T (manufacturing capability for reactor components) and Hindustan Aeronautics (precision engineering) are tangential plays.

## 4.4 Grid Equipment: The Quiet Compounders

A meaningful portion of hyperscaler capex is now flowing into grid equipment — transformers, switchgear, high-voltage cables, substations. The companies that supply this equipment have multi-year order books, pricing power, and a customer base willing to pay almost any premium for delivery slots.

The names: GE Vernova (Electrification segment), Schneider Electric, ABB, Eaton, Siemens AG, and the cable manufacturers (Prysmian, NKT, Nexans). On the Indian side, the closest analogues are KEI Industries, Polycab India, ABB India, Siemens India, Hitachi Energy India, and GE T&D India. The Indian cable and switchgear majors have all seen meaningful order book expansion in 2025–2026 from a combination of domestic grid investment, data centre buildout, and export demand.

\newpage

# Section 5 — The Software Layer: Foundation Models and Applications

## 5.1 Foundation Model Revenue Growth

The two leading frontier model labs in the West have both scaled revenue at rates that have no precedent in enterprise software history.

| Company   | Jan 2024 | Jan 2025 | Jan 2026 | May 2026 (est.) |
|-----------|----------|----------|----------|------------------|
| OpenAI    | \$2 bn   | \$6 bn   | \$20 bn  | \$33 bn          |
| Anthropic | \$0.3 bn | \$1 bn   | \$13 bn  | \$45 bn          |

Source: Sacra, Epoch AI, public reporting, SaaStr.

Two observations matter. First, both companies are scaling revenue at rates that, if sustained, would make them among the largest enterprise software businesses ever built. Second, Anthropic has accelerated faster than OpenAI in 2026 — a 30x increase from a small base, versus OpenAI's 2x. The Anthropic acceleration is concentrated in enterprise — approximately 80% of Anthropic's revenue is from business customers, versus a more consumer-heavy mix at OpenAI. Eight of the Fortune 10 are now Claude customers; over 500 enterprises spend more than \$1 million per year.

The structural read on the foundation model layer is that the underlying economics are not yet stable. Training costs are still growing — OpenAI is projected to spend roughly \$125 billion per year on training by 2030, against Anthropic's projected \$30 billion. Both numbers are large enough that the revenue growth must continue at near-current rates to generate any reasonable return on training capex. The race is not over; the question is whether either company will achieve positive unit economics at scale before the capex cycle compresses.

For an equity investor, neither OpenAI nor Anthropic is publicly listed. The exposure is indirect:
- Microsoft has the OpenAI investment and platform economics
- Amazon has a large Anthropic stake and AWS hosting relationship
- Google has its own Gemini stack and full vertical integration

## 5.2 The Application Layer

The application layer is where the bull-bear debate becomes most acute. The capex assumes that AI will generate trillions of dollars in productivity gains across enterprise software, customer service, coding, research, and content generation. The question is whether that productivity is being captured by venture-funded AI native companies, by incumbent SaaS players who layer AI on top, or simply does not yet exist in measurable form.

The evidence is mixed. The most successful AI-native application companies are showing the fastest revenue growth in enterprise software history:

- Glean: \$100m ARR (late 2024) → \$300m ARR (May 2026)
- Perplexity: ~\$50m ARR (early 2025) → \$450m+ ARR (March 2026)
- Cursor: valued at \$29.3 billion; AI coding platform, revenue not publicly disclosed but reportedly in similar range
- Anthropic's Claude Code: 5.5x growth post Claude 4 launch

However, the MIT Project NANDA study found that 95% of enterprise GenAI pilots produce zero measurable P&L impact. Sequoia's David Cahn calculated a \$600 billion annual revenue gap between current AI capex run-rate and the revenue required to justify it.

Both can be true. The application layer is bifurcating. AI-native companies attacking specific enterprise workflows (knowledge search, coding, research) are showing real product-market fit and rapid scaling. Generic GenAI deployments by enterprises hoping for productivity gains are mostly failing. The lesson, as in every prior technology cycle, is that the platform shift creates real value, but the value is captured by specific narrow applications, not by horizontal AI infrastructure plays at the enterprise.

\newpage

# Section 6 — India's AI Buildout

## 6.1 The Capex Commitment

India is now the second-largest committed AI infrastructure buildout in the world by capital, behind only the US hyperscalers.

| Player              | Committed Capex | Timeline   | Use                              |
|---------------------|-----------------|------------|----------------------------------|
| Reliance / Jio      | \$110 bn        | 7 years    | Multi-GW AI DC + edge compute    |
| Adani Group         | \$100 bn        | 10 years   | 2 GW → 5 GW data centre capacity |
| Tata Group / TCS    | (multi-GW; \$ undisclosed) | 5+ years | OpenAI as anchor tenant |
| Total committed     | \$300 bn+       | 10 years   |                                  |

Source: TechCrunch, CNBC, Bloomberg, IBTimes India aggregations of public announcements February–May 2026.

The Reliance plan deserves specific attention because it is the most strategically coherent. The combination of:
- Up to 10 GW of captive renewable energy capacity (solar in Kutch and Andhra Pradesh)
- The Jio nationwide telecom and edge compute network
- Existing relationships with Meta (WhatsApp), Google, and increasingly Microsoft
- A multi-decade history of building physical infrastructure at a cost advantage

…makes Reliance the single most credible Indian play on the global AI infrastructure cycle. The captive renewable energy is the differentiator. Globally, data centre operators pay grid power prices that are rising rapidly. Reliance can effectively transfer-price its own green electricity at marginal cost, generating a structural cost advantage of estimated 20–35% versus a US-based hyperscale data centre running on grid power.

Adani's plan is similar in shape but more concentrated in commercial real estate and renewable energy. The 2 GW current capacity scaling to 5 GW positions Adani as the largest pure-play data centre operator in India.

Tata's plan is the most under-discussed but potentially significant. The partnership with OpenAI as anchor tenant, combined with Tata's existing manufacturing, real estate, and electronics businesses, suggests Tata is building a vertically integrated AI infrastructure stack — including the announced semiconductor fab in Dholera and OSAT facility in Assam.

## 6.2 The Indian IT Services Layer

The Indian IT services majors (TCS, Infosys, HCLTech, Wipro, LTIMindtree, Tech Mahindra, Persistent) have spent the last 18 months pivoting to AI services delivery. The deal pipeline data is encouraging:

| Company   | Recent Deal Wins | AI-Themed Deal Share |
|-----------|------------------|-----------------------|
| TCS       | 106 deals        | 81 (76%)              |
| Wipro     | 99 deals         | 83 (84%)              |
| Infosys   | 55% net-new on \$14.9bn large deals | High |

Source: Q4 FY26 / Q1 FY27 earnings calls and SEC 6-K filings.

The bull read on Indian IT is that this is the largest enterprise consulting opportunity since the Y2K cycle and digital transformation of 2015–2020 combined. Every Fortune 500 enterprise needs to figure out AI deployment, data infrastructure, and process re-engineering. The Indian IT majors have the scale, delivery capability, and existing customer relationships to capture a meaningful share of that spend.

The bear read is that the unit economics of AI services are unclear. Traditional Indian IT margins (22–25%) were built on bodyshop economics. AI-themed engagements involve more software and less labour, which compresses revenue per consultant but raises the question of whether margins expand (good) or whether the entire revenue base contracts (bad). The next four quarters of margin prints will be informative.

## 6.3 Indian Listed Names with AI Exposure

A partial map of the listed Indian universe with AI exposure:

| Layer                | Listed Names                                                  |
|----------------------|---------------------------------------------------------------|
| Data centre operators | RELIANCE, ADANIENT, ADANIPORTS (Mundra DC), TATA group       |
| Power generation     | NTPC, ADANIGREEN, TATAPOWER, JSWENERGY, COALINDIA            |
| Grid / electricals   | KEI, POLYCAB, ABB India, SIEMENS, GE T&D, HITACHIENERGY      |
| IT services          | TCS, INFY, HCLTECH, WIPRO, LTIM, TECHM, PERSISTENT, COFORGE  |
| Semis / EMS          | KAYNES, DIXON, AMBER, SYRMA, CYIENT                          |
| Cooling / industrial | BLUESTARCO, VOLTAS, CUMMINSIND, KIRLOSKAR                    |

This is not a recommendation list; it is the universe to evaluate. Each name in this list requires its own Phase 0-5 framework run to determine whether the AI thesis maps to durable economics for that specific company, or whether the company is a passing beneficiary that will be re-rated downward when the cycle compresses.

\newpage

# Section 7 — Geopolitics and Sovereign AI

The AI supercycle is the first large industrial cycle in 70 years to be conducted under conditions of explicit great-power technology competition. This matters for two reasons. First, US export controls are now the single largest determinant of how the global AI semiconductor market segments — between a US-Allied supply chain centred on Nvidia, TSMC, and ASML, and a Chinese supply chain centred on Huawei, SMIC, and increasingly domestic memory and packaging. Second, sovereign AI investment by governments (US, UAE, Saudi Arabia, France, UK, India, Japan, Korea) is now a meaningful share of incremental data centre capacity globally.

## 7.1 China's Position

Huawei's Ascend chip programme has accelerated significantly through 2025–2026. The Ascend 950PR has been launched as a 1.56 PFLOP AI inference chip with claimed 2.8x the FP4 performance of Nvidia's H20 (the export-version GPU that was previously allowed for China). Huawei has stated capacity of approximately 750,000 Ascend 950PR units for 2026, with ByteDance committing \$5.6 billion in orders. DeepSeek's V4 model has been optimised for Ascend silicon, which removes the historical software portability advantage Nvidia held in China.

The bear case on China's AI position — that it is locked out of the cycle by export controls — is now substantially weaker than it was in 2024. The bull case for Nvidia and the US-Allied supply chain — that China cannot catch up — needs to be qualified. China is catching up in inference and in deployment, and is closing the gap on training. The principal remaining constraint is access to advanced lithography (ASML) and HBM memory, both of which are export-controlled. As long as those constraints hold, China runs a parallel and slightly behind AI infrastructure stack.

## 7.2 Sovereign AI Investments

The Gulf states have committed approximately \$200 billion in combined AI infrastructure spending across UAE (G42, MGX), Saudi Arabia (HUMAIN), and Qatar. These are sovereign wealth fund driven investments with explicit strategic objectives: capture a position in the global AI infrastructure stack as a sovereign hedge against oil revenue decline, and host hyperscale AI capacity to attract Western talent and investment.

France, UK, Germany, and the Nordics each have announced national AI compute strategies of varying scale. None individually matches the Gulf commitments. The collective European position is significant but fragmented.

## 7.3 The Indian Geopolitical Position

India's position in the AI supercycle is strategically advantageous in a way that has been under-discussed. The country has:
- A large engineering talent base (largest tech-skilled labour force globally)
- Domestic data demand at scale (1.4 billion people, growing digital economy)
- Geographic position outside the US-China bilateral competition (option value)
- Government willingness to spend on AI infrastructure (Bharat AI Mission, semiconductor PLI)
- Captive renewable energy (Reliance, Adani both invest heavily in solar)

The combination makes India a credible third pole in the global AI infrastructure stack — not at the scale of US or China, but at a scale meaningful enough to host hyperscale capacity, host Western model training (Tata–OpenAI deal), and attract investment from both US and Chinese-adjacent capital. The strategic position is rare and valuable.

\newpage

# Section 8 — The Bear Case

A serious investor must engage with the bear case directly. The bear case for the AI supercycle has three components.

## 8.1 The Revenue Gap

Sequoia's David Cahn computed that hyperscaler AI capex run-rate now implies roughly \$600 billion in annual revenue would need to flow to AI to justify it at conventional returns on capital. Current visible AI revenue (across foundation models, application layer, AI services) is in the range of \$150–200 billion. The gap is real and large. The question is the trajectory: how fast does enterprise AI revenue scale to close the gap, and how patient are equity markets while it scales?

Multiple plausible scenarios:
1. Revenue scales fast enough (75–100% YoY through 2027–2028) and the gap closes by 2029–2030 — bull case, every layer of the stack is a multi-bagger
2. Revenue scales at 40–60% YoY and the gap closes by 2031–2033 — base case, multi-baggers concentrated in supply-constrained layers (memory, packaging, power), multiples compress in compute and software
3. Revenue scales at 20–30% YoY and the gap persists — bear case, capex writes down, hyperscalers cut spending, supply chain compresses

The most useful tracking variable is enterprise AI revenue conversion. If by mid-2027 we see hyperscaler AI segment revenue (Azure AI, AWS Bedrock + Anthropic, Google Cloud AI) collectively crossing \$200 billion annualised, scenario 1 or 2. If it remains under \$100 billion, scenario 3 is the working case.

## 8.2 The 95% Enterprise Failure Rate

The MIT Project NANDA finding that 95% of enterprise GenAI pilots produce zero measurable P&L impact is the most damaging single data point for the supercycle thesis. The defence is that pilots are not deployments, and that the 5% that do succeed are scaling fast. The attack is that enterprise software cycles historically have higher pilot-to-deployment conversion rates than 5%, and that this number suggests the technology is not yet ready for general enterprise use.

The truthful read sits in between. AI is delivering measurable value in narrow, well-defined workflows (coding assistance, customer service deflection, enterprise search, document summarisation). It is failing in broader, fuzzier mandates (digital transformation, end-to-end process automation). Equity investors should weight the narrow use case providers (Cursor, Glean, Anthropic Claude Code) more heavily than horizontal enterprise AI plays.

## 8.3 The Capex Cycle Itself

The historical pattern of any large capex cycle is overshoot followed by correction. Railroads in the 1870s, fibre-optics in 2000–2001, oil and gas shale in 2014–2016, solar in 2018–2019. The supercycle thesis must engage with the question: at what point does the AI capex cycle hit its overshoot point?

The honest answer is that we do not yet see it. Demand is still outstripping supply at every layer of the stack. Utilisation rates at hyperscaler AI clusters remain high (Nvidia management has repeatedly indicated 80%+ utilisation across major customers). Order books are growing, not contracting. Lead times are extending, not compressing.

The cleanest forward signals to watch are:
1. Hyperscaler AI segment utilisation rates dropping below 60%
2. Nvidia order book growth decelerating below 30% YoY
3. HBM pricing declining (either through reduced demand or expanded supply)
4. Hyperscaler capex guidance being revised down for the first time in a forward year
5. Major write-downs of AI infrastructure assets

None of these signals are currently flashing. When two or more flash simultaneously, the cycle is rolling over.

\newpage

# Section 9 — Investment Positioning Framework

## 9.1 The Layer-by-Layer Quality Scorecard

The relative attractiveness of each layer in the AI supercycle is a function of three factors: supply constraint (how hard is it to add capacity), pricing power (how much of the value flows to producers vs customers), and durability (how long does the layer's economics persist beyond the current cycle).

| Layer                       | Supply Constraint | Pricing Power | Durability | Composite |
|-----------------------------|-------------------|---------------|------------|-----------|
| HBM memory                  | Very high         | High          | Medium     | A         |
| Advanced packaging (CoWoS)  | Very high         | High          | Medium-High| A         |
| Gas turbines                | High              | High          | Medium     | A-        |
| Nvidia (training)           | Medium-High       | Very high     | Medium-High| A-        |
| Grid equipment              | Medium-High       | Medium-High   | High       | A-        |
| Nuclear / SMR               | Medium (today)    | Medium        | Very high  | B+        |
| Data centre operators (India)| Medium-High      | Medium        | High       | B+        |
| Hyperscalers                | Low (they buy)    | Very high (cloud) | Very high | B+      |
| Indian IT services          | Low               | Medium        | Medium     | B         |
| Foundation model labs       | Low (capital)     | Decreasing    | Uncertain  | B-        |
| AI-native applications      | Low               | Variable      | Variable   | B-        |
| Cooling / electrical commodity| Medium          | Medium        | Medium     | C+        |
| Generic enterprise GenAI    | None              | Low           | Low        | C         |

Composite grades are this report's qualitative scoring, not formal Phase 0-5 Quality Scores. Individual stock evaluation requires the full framework.

## 9.2 The Indian Investor Lens

For an Indian investor whose portfolio is concentrated in INR-denominated assets, the AI supercycle creates three distinct opportunity sets.

The first opportunity is direct Indian AI infrastructure. Reliance, Adani, and Tata (where listed entities exist) provide capex-cycle exposure with the structural cost advantage of co-located renewable energy. The risk is execution and the level at which equity markets are already pricing the AI optionality.

The second opportunity is Indian electrical and grid equipment. KEI Industries, Polycab, ABB India, Siemens India, Hitachi Energy India — companies with multi-year order books, expanding margins, and direct revenue capture from data centre and grid upgrade capex. This is the highest-quality value chain exposure available on Indian exchanges.

The third opportunity is Indian IT services. The risk-reward here is more contingent. If Indian IT executes the AI services pivot at the margin profile of the last decade, these are multi-bagger candidates. If the AI services pivot compresses margins (more software, less labour), the multiples re-rate downward. The next four quarters of margin prints are the resolving signal.

For US/international exposure (where the investor has access), the cleanest multi-bagger candidates sit in HBM memory, advanced packaging, gas turbines, and grid equipment — all of which have the supply constraint, pricing power, and physical capacity buildout that define the most attractive industrial cycles in history.

## 9.3 What the Framework Says

Applying the multi-bagger framework principles to the AI supercycle as a whole:

- Phase 0 (Threshold checks): The cycle survives. Capital structure of major participants is strong; governance is reasonable; demand is real.
- Phase 1 (Compounding engine): Compute, memory, and power supply constraints create high ROIC for capacity owners. Foundation model and application layer ROIC is unproven.
- Phase 2 (Runway): The TAM expansion is real. Global enterprise software is a multi-trillion dollar opportunity; AI captures a meaningful share of it.
- Phase 3 (Competitive position): Nvidia's moat is narrowing but real. Memory and packaging oligopolies are durable. Foundation model competition is intensifying.
- Phase 4 (Management quality): Variable by name. Hyperscaler CEOs are exceptional capital allocators; foundation model leadership is mixed; Indian conglomerate execution risk is real.
- Phase 4.5 (Stress test): The 5-Whys for the AI cycle leads to a systemic answer (computational complexity of intelligent software), not a fragile one. The world-state under base case in 2028–2030 includes either tight constraint and multi-bagger returns for capacity owners, or capex overshoot and concentrated write-downs.
- Phase 5 (Valuation): This is where the cycle is most expensive. PEG ratios across the AI ecosystem are elevated. The cleanest margin of safety sits in supply-constrained physical assets (memory, packaging, power) and in Indian infrastructure plays where market has not yet fully priced the AI capex.

\newpage

# Section 10 — Stocks to Watch (Layer-Mapped, Not a Recommendation List)

This section is a research universe, not a buy list. Each entry requires individual Phase 0-5 evaluation before any position is taken.

## Global

| Ticker      | Company                  | Layer                  | Why on List                              |
|-------------|--------------------------|------------------------|------------------------------------------|
| NVDA        | Nvidia                   | Compute (training)     | Dominant; widening moat in training      |
| 000660.KS   | SK Hynix                 | HBM Memory             | Tightest layer; HBM4 first-mover         |
| MU          | Micron                   | HBM Memory             | Smallest but accelerating share          |
| 005930.KS   | Samsung Electronics      | HBM Memory + Foundry   | HBM4 ramp; competing with TSMC           |
| 2330.TW     | TSMC                     | Foundry + Packaging    | CoWoS dominant; 80% CAGR capacity build  |
| ASML.AS     | ASML                     | Lithography            | Monopoly in EUV; high-NA delayed         |
| GEV         | GE Vernova               | Gas turbines + grid    | 110 GW backlog by end-2026; data centre orders accelerating |
| ENR.DE      | Siemens Energy           | Gas turbines           | Multi-year backlog                       |
| CEG         | Constellation Energy     | Nuclear                | Meta + Microsoft PPAs; SMR optionality   |
| VST         | Vistra                   | Nuclear + gas          | Nuclear fleet exposure                   |
| VRT         | Vertiv                   | Cooling                | Direct DC cooling and power infrastructure |
| ETN         | Eaton                    | Electricals            | Switchgear, power distribution           |
| ABB.SW      | ABB                      | Electricals            | Grid + automation                        |
| SU.PA       | Schneider Electric       | Electricals            | DC power, EcoStruxure                    |
| AVGO        | Broadcom                 | Networking + custom Si | Networking ASICs; growing AI exposure    |
| MSFT        | Microsoft                | Hyperscaler            | OpenAI relationship; Azure AI            |
| GOOGL       | Alphabet                 | Hyperscaler + models   | TPU + Gemini fully vertical              |
| AMZN        | Amazon                   | Hyperscaler + Anthropic | AWS Bedrock + Trainium                  |
| META        | Meta Platforms           | Hyperscaler + models   | Llama, captive AI capex                  |
| ORCL        | Oracle                   | Hyperscaler            | OpenAI anchor; highest leverage          |

## India

| Ticker      | Company                  | Layer                  | Why on List                              |
|-------------|--------------------------|------------------------|------------------------------------------|
| RELIANCE    | Reliance Industries      | DC + captive power     | \$110bn AI plan; captive renewable energy |
| ADANIENT    | Adani Enterprises        | DC operator            | \$100bn capex plan; 2 → 5 GW             |
| ADANIPORTS  | Adani Ports              | Adjacent infrastructure| Mundra DC complex                        |
| TATAELXSI   | Tata Elxsi               | Engineering services   | Tata group AI infrastructure exposure    |
| TCS         | Tata Consultancy Services| IT services            | 76% AI deal share; \$14.9bn large deals  |
| INFY        | Infosys                  | IT services            | \$20bn revenue base; AI deals scaling    |
| HCLTECH     | HCL Technologies         | IT services            | Mid-tier AI services capability          |
| WIPRO       | Wipro                    | IT services            | 84% AI deal share                        |
| LTIM        | LTIMindtree              | IT services            | Mid-cap AI services scale                |
| PERSISTENT  | Persistent Systems       | IT services            | Smaller, faster-growing AI exposure      |
| KEI         | KEI Industries           | Electrical cables      | Data centre + grid orders                |
| POLYCAB     | Polycab India            | Electrical cables      | Largest Indian cable player              |
| ABB         | ABB India                | Switchgear + automation| Direct DC equipment exposure             |
| SIEMENS     | Siemens India            | Switchgear + electricals| Multi-year order growth                 |
| HITACHIENER | Hitachi Energy India     | Grid + transformers    | High-voltage equipment monopolist        |
| GET&D       | GE T&D India             | Grid + transformers    | Transmission equipment                   |
| BLUESTARCO  | Blue Star                | Cooling                | HVAC for data centres                    |
| VOLTAS      | Voltas                   | Cooling                | Industrial HVAC                          |
| CUMMINSIND  | Cummins India            | Power generation       | Backup gensets for DC                    |
| NTPC        | NTPC                     | Power generation       | Largest Indian generator                 |
| ADANIGREEN  | Adani Green Energy       | Renewable generation   | Captive supply for Adani DC              |
| TATAPOWER   | Tata Power               | Renewable + DC power   | Multiple AI-adjacent businesses          |
| KAYNES      | Kaynes Technology        | EMS + packaging        | Semicon ecosystem positioning            |
| DIXON       | Dixon Technologies       | EMS                    | Indian electronics manufacturing scale   |

\newpage

# Section 11 — Conclusion

The AI supercycle is the dominant industrial story of the late 2020s. It is real, it is large, and it has at least 5–10 years of structural capex ahead of it. The cycle will compound real economic value, and at the same time, will produce significant capital destruction in the layers of the stack that are least supply-constrained.

The investable opportunity for a long-horizon equity investor is not "buy AI" — that horizontal exposure captures the average outcome of the cycle, which includes the bear scenarios. The investable opportunity is specific: own the layers of the cycle that are physically supply-constrained (memory, advanced packaging, gas turbines, grid equipment, captive-power data centres) and avoid the layers that are demand-led but supply-elastic (generic enterprise GenAI, commodity cooling, undifferentiated cloud).

For an Indian investor, the supercycle creates a uniquely attractive opportunity set. India is positioned as the second-largest committed AI infrastructure build globally, with structural cost advantages from captive renewable power and a deep engineering labour pool. The listed Indian electrical, cable, grid equipment, IT services, and conglomerate names provide multiple ways to participate. Each requires individual framework evaluation before commitment.

The principal risk to the cycle is not whether AI works as a technology — it does. The risk is whether enterprise revenue scales fast enough to justify the capex. Tracking variables: hyperscaler AI segment utilisation (target >60%), Nvidia order book growth (target >30% YoY), HBM pricing direction (target stable to up), and the cadence of enterprise AI revenue conversion at the major foundation model labs.

The cycle is not yet at its overshoot. The signals to watch for the rollover are clear, observable, and quantifiable. Until those signals flash, the working hypothesis is that the AI supercycle is the dominant equity opportunity of the next decade, with the largest concentrations of value flowing to the most physically constrained layers of the buildout.

This report is a framework, not a recommendation. Position sizing, individual stock evaluation, and entry timing remain dependent on the full Phase 0-5 multi-bagger framework applied to each candidate.

\newpage

# Sources

Hyperscaler capex:

- Tom's Hardware — Big Tech AI Spending Plans Reach \$725 Billion
- CNBC — Tech AI spending approaches \$700 billion in 2026
- Futurum Group — AI Capex 2026: The \$690B Infrastructure Sprint
- Yahoo Finance — Hyperscalers Hit \$700 Billion in 2026 AI Spending Plans

Nvidia and compute:

- Nvidia 8-K filings, Q4 FY26 and Q1 FY27 CFO commentary (SEC EDGAR)
- Seeking Alpha — NVIDIA targets \$65B Q4 revenue and \$0.5T Blackwell & Rubin sales through 2026
- Futurum — NVIDIA Q3 FY 2026 Earnings: Record Data Center Revenue

Memory (HBM):

- TrendForce — Samsung, SK hynix HBM3E Price Hike for 2026
- CNBC — SK Hynix posts record first-quarter profit on AI memory shortage
- Presenc AI — HBM Market Share 2026

Packaging:

- TSMC quarterly reports
- Digitimes — CoWoS capacity emerges as AI bottleneck
- SemiWiki — CoWoS Capacity Set to Skyrocket by 2026
- Financial Content — TSMC \$56 Billion 2026 Capex

Power and grid:

- IEA Data Centre Energy Report
- US Department of Energy / Lawrence Berkeley National Laboratory data centre projections
- GE Vernova 8-K filings, Q1 2026 (SEC EDGAR)
- Bloomberg — Siemens Energy, Mitsubishi Struggle to Keep Up With AI-Driven Demand
- S\&P Global — GE Vernova to ride electrification wave

Nuclear and SMR:

- Constellation Energy and Meta PPA announcements
- IRecruit — SMR Data Centers
- GE Vernova–Hitachi BWRX-300 commercial timeline

Foundation models:

- Sacra — Anthropic Revenue, Valuation and Funding
- Epoch AI — Anthropic OpenAI Revenue comparison
- SaaStr — Anthropic Just Passed OpenAI in Revenue

Applications:

- TechCrunch — Glean ARR \$300m
- PYMNTS — Perplexity Revenue Surge
- Futurum — Glean Doubles ARR to \$200M

India buildout:

- TechCrunch — Reliance \$110B AI Plan
- CNBC — Adani \$100B AI Data Centre Investment
- Lightreading — Reliance Adani \$210B AI Infra Commitment
- IBTimes India — Ambani Tata Adani Sovereign Intelligence Revolution

Geopolitics:

- CSIS — DeepSeek, Huawei, Export Controls
- Tom's Hardware — Huawei Ascend 950PR Launch
- Council on Foreign Relations — China's AI Chip Deficit

Bear case:

- Investing.com — AI Token Pricing Crisis
- Investorplace — AI Capex Debate: Misallocation or Generational ROIC
- Lambda Finance — 1999 Dot-Com Bubble vs 2026 AI Bubble
- MIT Project NANDA — Enterprise GenAI Pilot Study

Indian IT services:

- The Tribune — Indian IT industry sharp recovery 2026
- Infosys 6-K filings, Q4 FY26 (SEC EDGAR)
- ANI News — Indian IT industry AI-led deal pipeline
