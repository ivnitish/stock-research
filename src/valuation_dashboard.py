#!/usr/bin/env python3
"""
Valuation Dashboard — fetches live CMP and computes upside vs 3Y fair value targets.

Outputs: output/html/valuation_data.js   (loaded by index.html)

Run:  cd "/Users/nitish/stocks automation" && python3 src/valuation_dashboard.py
Cron: daily at 6pm IST (after NSE close)

Methodology:
  upside_pct = (fair_value / cmp - 1) × 100  — always vs CMP, never vs entry price
  multibagger_x = fair_value / cmp            — potential from current price
  "Multibagger" in old dashboard was manual; this script makes it computed + CMP-based.
"""

import yfinance as yf
import json, os, sys
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Fair value targets — 3Y analyst / model-derived
# key       = short ticker as in index.html onclick="go('TICKER.html')"
# yf        = yfinance symbol
# fair      = target price (₹ for India, $ for US). None = EXIT
# method    = valuation approach shown as tooltip
TARGETS = {
    # ── HOLDINGS ────────────────────────────────────────────────────────────
    "GROWW":      {"yf": "GROWW.NS",       "fair": 192,   "method": "P/E 40x FY27E (base)"},
    "KAYNES":     {"yf": "KAYNES.NS",      "fair": 5400,  "method": "P/E 60x FY27E"},
    "EPACKPEB":   {"yf": "EPACKPEB.NS",    "fair": 800,   "method": "P/E 25x FY27E"},
    "KERNEX":     {"yf": "KERNEX.NS",      "fair": 1444,  "method": "P/E 20x FY27E"},
    "ARTEMISMED": {"yf": "ARTEMISMED.NS",  "fair": 279,   "method": "EV/EBITDA 20x"},
    "NAVA":       {"yf": "NAVA.NS",        "fair": 838,   "method": "Sum-of-parts"},
    "BANCOINDIA": {"yf": "BANCOINDIA.NS",  "fair": 701,   "method": "P/E 15x FY27E"},
    "SHILCTECH":  {"yf": "SHILCTECH.NS",   "fair": 3596,  "method": "P/E 30x FY27E"},
    "STLTECH":    {"yf": "STLTECH.NS",     "fair": 60,    "method": "Turnaround FCF"},
    "ETERNAL":    {"yf": "ETERNAL.NS",     "fair": 218,   "method": "EV/GMV"},
    "SWIGGY":     {"yf": "SWIGGY.NS",      "fair": 385,   "method": "EV/GMV"},
    "PARADEEP":   {"yf": "PARADEEP.NS",    "fair": None,  "method": "EXIT"},

    # ── WATCHLIST — India ───────────────────────────────────────────────────
    "ICICIAMC":   {"yf": "ICICIAMC.NS",    "fair": 3520,  "method": "P/E 35x FY27E"},
    "NEWGEN":     {"yf": "NEWGEN.NS",      "fair": 640,   "method": "P/E 30x FY27E"},
    "ANANTRAJ":   {"yf": "ANANTRAJ.NS",    "fair": 660,   "method": "P/E 40x FY27E"},
    "SHAKTIPUMP": {"yf": "SHAKTIPUMP.NS",  "fair": 720,   "method": "P/E 30x FY27E"},
    "SAKSOFT":    {"yf": "SAKSOFT.NS",     "fair": 320,   "method": "P/E 25x FY27E"},
    "RAYMOND":    {"yf": "RAYMOND.NS",     "fair": 493,   "method": "Sum-of-parts"},
    "RSYSTEMS":   {"yf": "RSYSTEMS.NS",    "fair": 408,   "method": "P/E 25x FY27E"},
    "STLNETWORK": {"yf": "STLTECH.NS",     "fair": 30,    "method": "Turnaround"},
    "JUSTDIAL":   {"yf": "JUSTDIAL.NS",    "fair": 963,   "method": "P/E 20x + cash"},

    # ── US ──────────────────────────────────────────────────────────────────
    "NVDA":       {"yf": "NVDA",           "fair": 1210,  "method": "P/E 30x FY26E"},
    "GOOGL":      {"yf": "GOOGL",          "fair": 220,   "method": "DCF"},
    "AMZN":       {"yf": "AMZN",           "fair": 240,   "method": "DCF"},
}


def verdict(upside_pct):
    if upside_pct is None:   return "N/A"
    if upside_pct >= 50:     return "Deep Value"
    if upside_pct >= 20:     return "Undervalued"
    if upside_pct >= -10:    return "Fair"
    if upside_pct >= -30:    return "Rich"
    return "Overvalued"


def fetch_prices(yf_tickers):
    """Fetch latest close prices for a list of yfinance tickers."""
    prices = {}
    # Try batch download first (faster)
    unique = list(set(yf_tickers))
    try:
        import pandas as pd
        data = yf.download(unique, period="3d", auto_adjust=True, progress=False)
        close = data["Close"] if isinstance(data.columns, pd.MultiIndex) else data
        for t in unique:
            try:
                series = close[t] if t in close.columns else close.iloc[:, 0]
                prices[t] = round(float(series.dropna().iloc[-1]), 2)
            except Exception:
                prices[t] = None
    except Exception as e:
        print(f"  Batch failed ({e}), falling back to individual fetches")
        for t in unique:
            try:
                h = yf.Ticker(t).history(period="3d")
                prices[t] = round(float(h["Close"].iloc[-1]), 2) if not h.empty else None
            except Exception:
                prices[t] = None
    return prices


def main():
    today = date.today().isoformat()
    yf_tickers = [v["yf"] for v in TARGETS.values() if v.get("yf")]

    print(f"Valuation Dashboard — {today}")
    print(f"Fetching prices for {len(set(yf_tickers))} tickers...\n")
    prices = fetch_prices(yf_tickers)

    result = {}
    print(f"  {'Ticker':<14} {'CMP':>10}  {'Fair':>8}  {'Upside':>8}  {'Verdict'}")
    print("  " + "-" * 58)

    for key, cfg in TARGETS.items():
        yf_t   = cfg.get("yf")
        fair   = cfg.get("fair")
        cmp    = prices.get(yf_t) if yf_t else None

        if fair is None:
            result[key] = {
                "cmp": cmp, "fair": None, "upside_pct": None,
                "multibagger_x": None, "verdict": "Exit",
                "method": cfg.get("method", ""), "updated": today,
            }
            print(f"  {key:<14} {'N/A':>10}  {'EXIT':>8}  {'—':>8}  Exit")
            continue

        if cmp and cmp > 0:
            upside = round((fair / cmp - 1) * 100, 1)
            mx     = round(fair / cmp, 2)
        else:
            upside = mx = None

        v = verdict(upside)
        result[key] = {
            "cmp": cmp, "fair": fair, "upside_pct": upside,
            "multibagger_x": mx, "verdict": v,
            "method": cfg.get("method", ""), "updated": today,
        }

        cmp_str    = f"{cmp:,.0f}" if cmp else "N/A"
        upside_str = f"{upside:+.0f}%" if upside is not None else "N/A"
        print(f"  {key:<14} {cmp_str:>10}  {fair:>8,}  {upside_str:>8}  {v}")

    out = os.path.join(BASE_DIR, "output", "html", "valuation_data.js")
    with open(out, "w") as f:
        f.write(f"// Valuation data — generated {today}\n")
        f.write(f"// upside_pct and multibagger_x are ALWAYS vs CMP (not entry price)\n")
        f.write(f"// Re-run: python3 src/valuation_dashboard.py\n")
        f.write(f"const VALUATION_DATA = {json.dumps(result, indent=2)};\n")

    print(f"\nWrote: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
