"""
Generate portfolio overview: allocation, sector mapping, concentration analysis.
Outputs research/PORTFOLIO_OVERVIEW.md

Usage:
  python src/portfolio_overview.py
"""
from __future__ import annotations

import os
import sys
from datetime import date

import pandas as pd
import yfinance as yf

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import PORTFOLIO_PATH, RESEARCH_DIR

# Manual sector mapping for portfolio stocks
SECTOR_MAP = {
    "GROWW.NS": "Fintech",
    "KAYNES.NS": "Electronics Manufacturing",
    "EPACKPEB.NS": "Prefab / Infrastructure",
    "KERNEX.NS": "Defence / Rail Tech",
    "ARTEMISMED.NS": "Healthcare",
    "PARADEEP.NS": "Fertilizers / Chemicals",
    "STLNETWORK.NS": "Telecom Infra",
    "SWIGGY.NS": "Food Delivery / Tech",
    "ETERNAL.NS": "Food Delivery / Tech",
    "BANCOINDIA.NS": "Auto Components",
    "NAVA.NS": "Energy / Mining",
    "SHILCTECH.NS": "Transformers / Power",
    "ATHERENERG.NS": "EV / Auto",
    "BHEL.NS": "Capital Goods",
    "BRIGADE.NS": "Real Estate",
    "CGCL.NS": "NBFC / Lending",
    "DREDGECORP.NS": "Infrastructure",
    "FABTECH.NS": "Engineering",
    "GATECH.NS": "Technology",
    "GRSE.NS": "Defence / Shipbuilding",
    "ICICIAMC.NS": "Asset Management",
    "NIPPOBATRY.NS": "Auto Components",
    "IZMO.NS": "Logistics Tech",
    "KPITTECH.NS": "Auto Tech / IT",
    "NDTV.NS": "Media",
    "NESCO.NS": "Real Estate / IT Park",
    "NETWEB.NS": "IT Hardware / HPC",
    "POLICYBZR.NS": "Insurtech",
    "SAGILITY.NS": "Healthcare IT",
    "SATIN.NS": "Microfinance",
    "SOUTHWEST.NS": "IT Services",
    "TTKHLTCARE.NS": "Healthcare / Consumer",
    "URBANCO.NS": "Gig Economy / Services",
    "VSTIND.NS": "Tobacco / FMCG",
    "ZENTEC.NS": "Defence Tech",
    "IIL$.NS": "Industrials",
    "PATELSAI$.NS": "Engineering",
}


def generate_overview() -> str:
    if not os.path.exists(PORTFOLIO_PATH):
        print("ERROR: Run groww_importer.py first")
        sys.exit(1)

    df = pd.read_csv(PORTFOLIO_PATH)
    df["invested"] = df["quantity"] * df["avg_buy_price"]
    total_invested = df["invested"].sum()
    df["alloc_pct"] = (df["invested"] / total_invested * 100).round(1)
    df["sector"] = df["symbol"].map(SECTOR_MAP).fillna("Other")

    # Fetch current prices
    prices = {}
    for sym in df["symbol"].tolist():
        try:
            t = yf.Ticker(sym)
            info = t.info
            p = info.get("regularMarketPrice") or info.get("currentPrice") or info.get("previousClose")
            pe = info.get("trailingPE")
            pb = info.get("priceToBook")
            roe = info.get("returnOnEquity")
            mcap = info.get("marketCap")
            prices[sym] = {"price": p, "pe": pe, "pb": pb, "roe": roe, "mcap": mcap}
        except Exception:
            prices[sym] = {}

    df["current_price"] = df["symbol"].map(lambda s: (prices.get(s) or {}).get("price"))
    df["current_value"] = df["current_price"] * df["quantity"]
    df["pnl"] = df["current_value"] - df["invested"]
    df["pnl_pct"] = (df["pnl"] / df["invested"] * 100).round(1)
    df["pe"] = df["symbol"].map(lambda s: (prices.get(s) or {}).get("pe"))
    df["pb"] = df["symbol"].map(lambda s: (prices.get(s) or {}).get("pb"))
    df["roe"] = df["symbol"].map(lambda s: (prices.get(s) or {}).get("roe"))

    total_current = df["current_value"].sum()
    total_pnl = total_current - total_invested

    # Sort by allocation
    df = df.sort_values("alloc_pct", ascending=False)

    # Build markdown
    today = date.today().isoformat()
    lines = [
        f"# Portfolio Overview — {today}",
        "",
        f"**Invested:** ₹{total_invested:,.0f} | **Current:** ₹{total_current:,.0f} | **P&L:** ₹{total_pnl:,.0f} ({total_pnl/total_invested*100:.1f}%)",
        f"**Stocks:** {len(df)} | **Sectors:** {df['sector'].nunique()}",
        "",
        "---",
        "",
        "## Holdings by Allocation",
        "",
        "| # | Stock | Sector | Alloc% | Invested | P&L% | P/E | P/B | ROE% |",
        "|---|-------|--------|--------|----------|------|-----|-----|------|",
    ]

    for i, (_, r) in enumerate(df.iterrows(), 1):
        sym = r["symbol"].replace(".NS", "")
        alloc = f"{r['alloc_pct']:.1f}%"
        inv = f"₹{r['invested']:,.0f}"
        pnl = f"{r['pnl_pct']:+.1f}%" if pd.notna(r.get("pnl_pct")) else "—"
        pe = f"{r['pe']:.1f}" if pd.notna(r.get("pe")) else "—"
        pb = f"{r['pb']:.1f}" if pd.notna(r.get("pb")) else "—"
        roe = f"{r['roe']*100:.0f}%" if pd.notna(r.get("roe")) else "—"
        lines.append(f"| {i} | {sym} | {r['sector']} | {alloc} | {inv} | {pnl} | {pe} | {pb} | {roe} |")

    # Concentration analysis
    top5_alloc = df.head(5)["alloc_pct"].sum()
    lines.extend([
        "",
        "---",
        "",
        "## Concentration Analysis",
        "",
        f"- **Top 1 stock:** {df.iloc[0]['symbol'].replace('.NS','')} = {df.iloc[0]['alloc_pct']:.1f}% of portfolio",
        f"- **Top 5 stocks:** {top5_alloc:.1f}% of portfolio",
        f"- **Single-share positions:** {len(df[df['quantity'] == 1])} stocks (tracking positions)",
        "",
    ])

    # Sector breakdown
    sector_alloc = df.groupby("sector")["alloc_pct"].sum().sort_values(ascending=False)
    lines.extend([
        "## Sector Exposure",
        "",
        "| Sector | Allocation% |",
        "|--------|-------------|",
    ])
    for sector, alloc in sector_alloc.items():
        lines.append(f"| {sector} | {alloc:.1f}% |")

    # Winners and losers
    valid = df.dropna(subset=["pnl_pct"])
    if len(valid) > 0:
        losers = valid.nsmallest(5, "pnl_pct")
        winners = valid.nlargest(5, "pnl_pct")
        lines.extend([
            "",
            "## Top Losers",
            "",
            "| Stock | P&L% | P&L ₹ | Sector |",
            "|-------|------|-------|--------|",
        ])
        for _, r in losers.iterrows():
            lines.append(f"| {r['symbol'].replace('.NS','')} | {r['pnl_pct']:+.1f}% | ₹{r['pnl']:+,.0f} | {r['sector']} |")

        lines.extend([
            "",
            "## Top Winners",
            "",
            "| Stock | P&L% | P&L ₹ | Sector |",
            "|-------|------|-------|--------|",
        ])
        for _, r in winners.iterrows():
            lines.append(f"| {r['symbol'].replace('.NS','')} | {r['pnl_pct']:+.1f}% | ₹{r['pnl']:+,.0f} | {r['sector']} |")

    # Action items
    lines.extend([
        "",
        "---",
        "",
        "## Action Items",
        "",
        "- [ ] Review concentration: Is 35%+ in GROWW justified for Grade B conviction?",
        "- [ ] Write thesis for core positions: KAYNES, EPACK, KERNEX",
        "- [ ] Evaluate biggest losers: SWIGGY, STL, ETERNAL — hold or exit?",
        "- [ ] Single-share positions: research or clean up?",
        "",
        f"*Generated: {today} by `python src/portfolio_overview.py`*",
    ])

    md = "\n".join(lines)
    out_path = os.path.join(RESEARCH_DIR, "PORTFOLIO_OVERVIEW.md")
    os.makedirs(RESEARCH_DIR, exist_ok=True)
    with open(out_path, "w") as f:
        f.write(md)
    print(f"Portfolio overview → {out_path}")
    return out_path


if __name__ == "__main__":
    generate_overview()
