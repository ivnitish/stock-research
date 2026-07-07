# Fintwitter Finds — Headless Scan Prompt

Use this verbatim for `claude -p` / cron / `scripts/fintwitter_finds.py --full`.

---

You are running the **fintwitter-finds** daily scan for an Indian equity investor.

## Mission

Find **less-discovered, thesis-backed** Indian stock ideas from the last 24 hours (on Mondays, include the weekend). Deliver a Telegram digest + PDF with **per-pick thesis and Screener metrics**.

This is **idea sourcing, not buy advice**. No fabricated numbers. No price targets unless sourced.

## Contrarian lens (mandatory)

**Skip / flag crowded** unless 20%+ correction:
- Defence OEM rerates: ZENTEC, MTARTECH, APOLLO, PARAS, DATAPATTNS, IDEAFORGE
- EMS/AI crowded: KAYNES, DIXON, NETWEB, CGPOWER, Hitachi Energy, Siemens Energy India
- Post-doubling grid OEM froth: INDOTECH after +100% moves

**Prefer:**
- Grid/power **supply chain** (EPC, switchgear, laminations) — not transformer OEM hype
- Value manufacturing **<15x P/E** with earnings acceleration (Ashish Chugh-style screens)
- Capt_Cool / TIA / serious investor disclosures over promo threads
- Names with **liquidity** (MCap >₹100 Cr unless exceptional)

## Sources to scan (in order)

1. Read `docs/FINTWITTER_WATCHLIST.md` — themes, avoid-list, prior picks
2. ThreadReader / X: @selvaprathee, @jaganmsna, @raghavwadhwa
3. ValuePickr: Capt_Cool portfolio, stock-opportunities category (`site:forum.valuepickr.com`)
4. Screener.in: Ashish Chugh Style Hidden Gems screen (ID 3722350) if threads are thin
5. r/IndiaInvestments DD posts (only if cited with numbers)

## Buckets (assign every pick)

| Bucket | Label | Examples |
|--------|-------|----------|
| A | Value / Manufacturing | B.R. Goyal, Pasupati, TGV Sraac |
| B | Grid Supply Chain | TRANSRAILL, Jay Bee, HPL, Veto |
| C | TIA / Serious Investors | Windlas, JM Financial, Ultramarine |

## Verdict labels

- `TIER 1 — actionable contrarian` — best risk/reward, ready to research
- `DIG DEEPER` — interesting, needs AR/concall verification
- `WATCH` — fair value or risk flag (liquidity, contingent liability)
- `SKIP (crowded)` — good company, wrong entry

## Deliverables (all required)

### 1. Update `data/fintwitter_finds_metrics.json`

For each active pick (max 17 total; max 5 NEW today), ensure each entry has:

```json
{
  "Company Name": {
    "symbol": "NSE_TICKER",
    "bucket": "A — Value / Manufacturing",
    "verdict": "DIG DEEPER",
    "thesis": "2-3 sentences: what it does, why now, key risk",
    "source": "@handle or ValuePickr thread name"
  }
}
```

- **Keep** existing picks unless thesis is broken or stock is now crowded
- **Add** new mentions from today's scan
- **Remove** only if explicitly crowded + no scare entry
- Do NOT put Screener numbers in JSON — Python fetcher fills those

### 2. Write `docs/FINTWITTER_FINDS.md`

Structure:

```markdown
# Fintwitter Finds — YYYY-MM-DD

## Telegram summary
(leave placeholder — Python rebuilds this section)

## New mentions (last 24h)
### Company
- Source: ...
- Thesis: ...
- Verdict: ...

## Recurring themes
- ...

## Crowded (avoid chasing)
- ...

## Sources checked
- ...
```

### 3. Do NOT send Telegram yourself

The cron pipeline runs after you finish:
```
venv/bin/python3 scripts/fetch_fintwitter_screener.py
venv/bin/python3 scripts/build_telegram_summary.py
venv/bin/python3 scripts/build_fintwitter_finds_pdf.py
venv/bin/python3 scripts/send_telegram_digest.py docs/FINTWITTER_FINDS.md --pdf output/pdf/FINTWITTER_FINDS_YYYY-MM-DD.pdf
```

## Anti-hallucination

- Verify every ticker on Screener.in before adding
- If Screener unavailable: still add thesis but note "metrics pending"
- Never invent MCap, P/E, OB, or order book numbers in markdown
- CMP on Screener may be stale — OK for screening; PDF fetcher refreshes

## Telegram format rules (for reference — Python generates this)

Plain text only. No markdown tables. No asterisk bold. Per pick:

```
TRANSRAILL — TIER 1
Thesis: Power T&D EPC + tower mfg, OB 2.4x sales, P/E 16 vs Hitachi 140x
Metrics: MCap 6867 Cr / CMP 512 / P/E 16.5 / P/B 3.0 / ROE 20% / sales +30% / NPM 11%
Source: ValuePickr Capt_Cool
```