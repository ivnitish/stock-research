#!/usr/bin/env python3
"""
Red Flag Monitor — Weekly automated check on portfolio holdings.
Checks: price vs cost basis, large moves, data freshness.
Run via launchd weekly (Sundays ~8am IST).
Output: journal/weekly/red_flags_YYYY-WXX.md
"""

import yfinance as yf
import json
import os
import sys
from datetime import datetime, date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Portfolio holdings with cost basis (manually maintained)
# Update avg_price and quantity when you trade
HOLDINGS = [
    # India — Core positions
    {"ticker": "GROWW.NS",       "name": "Groww",              "qty": 2298, "avg_price": 130.8,   "grade": "B", "score": 19},
    {"ticker": "KAYNES.NS",      "name": "Kaynes Technology",  "qty": 31,   "avg_price": 4255.3,  "grade": "B", "score": 17},
    {"ticker": "EPACKPEB.NS",    "name": "EPACK Prefab",       "qty": 451,  "avg_price": 227.9,   "grade": "B", "score": 17},
    {"ticker": "KERNEX.NS",      "name": "Kernex Microsys",    "qty": 90,   "avg_price": 1125.4,  "grade": "B", "score": 17},
    {"ticker": "ARTEMISMED.NS",  "name": "Artemis Medicare",   "qty": 181,  "avg_price": 245.9,   "grade": "B", "score": 16},
    {"ticker": "NAVA.NS",        "name": "Nava Limited",       "qty": 56,   "avg_price": 461.6,   "grade": "B", "score": 16},
    {"ticker": "BANCOINDIA.NS",  "name": "Banco Products",     "qty": 100,  "avg_price": 589.5,   "grade": "B", "score": 19},
    {"ticker": "SHILCTECH.NS",   "name": "Shilchar Tech",      "qty": 9,    "avg_price": 3046.0,  "grade": "B", "score": 18},
    {"ticker": "RAYMOND.NS",     "name": "Raymond Engineering","qty": 150,  "avg_price": 368.75,  "grade": "B", "score": 17},
    {"ticker": "ANANTRAJ.NS",    "name": "Anant Raj",          "qty": 200,  "avg_price": 460.8,   "grade": "B", "score": 17},
    {"ticker": "NEWGEN.NS",      "name": "Newgen Software",    "qty": 200,  "avg_price": 447.8,   "grade": "B", "score": 18},
    {"ticker": "RSYSTEMS.NS",    "name": "R Systems Intl",     "qty": 350,  "avg_price": 286.5,   "grade": "B", "score": 15},
    {"ticker": "SAKSOFT.NS",     "name": "Saksoft",             "qty": 450,  "avg_price": 129.41,  "grade": "B", "score": 16},
    {"ticker": "ICICIAMC.NS",    "name": "ICICI Pru AMC",      "qty": 6,    "avg_price": 2165.0,  "grade": "A", "score": 20},
    {"ticker": "NESCO.NS",       "name": "Nesco",              "qty": 1,    "avg_price": 1376.0,  "grade": "B", "score": 19},
    {"ticker": "SHAKTIPUMP.NS",  "name": "Shakti Pumps",       "qty": 200,  "avg_price": 518.95,  "grade": "B", "score": 16},
    # India — Exit candidates / low conviction
    {"ticker": "PARADEEP.NS",    "name": "Paradeep Phosphates","qty": 220, "avg_price": 175.8,   "grade": "C", "score": 11},
    {"ticker": "STLNETWORK.NS",  "name": "STL Network",         "qty": 1500, "avg_price": 31.2,    "grade": "C", "score": 12},
    {"ticker": "ETERNAL.NS",     "name": "Eternal (Zomato)",   "qty": 100,  "avg_price": 337.4,   "grade": "B", "score": 15},
    {"ticker": "SWIGGY.NS",      "name": "Swiggy",             "qty": 49,   "avg_price": 565.2,   "grade": "C", "score": 10},
    {"ticker": "531889.BO",       "name": "Integrated Ind",    "qty": 165,  "avg_price": 27.96,   "grade": "C", "score": 13},
    # US
    {"ticker": "GOOGL",          "name": "Alphabet",           "qty": 0,    "avg_price": 0,       "grade": "A", "score": 23},
    {"ticker": "AMZN",           "name": "Amazon",             "qty": 0,    "avg_price": 0,       "grade": "A", "score": 21},
    {"ticker": "NVDA",           "name": "NVIDIA",             "qty": 0,    "avg_price": 0,       "grade": "A", "score": 22},
]

# Alert thresholds
THRESHOLDS = {
    "large_drop_1w_pct":  -8,    # >8% drop in a week → flag
    "large_gain_1w_pct":  15,    # >15% gain in a week → flag (review thesis)
    "grade_c_loss_pct":  -35,    # Grade C with >35% unrealised loss → exit candidate
    "grade_b_loss_pct":  -25,    # Grade B with >25% unrealised loss → review
}


def get_week_label():
    today = date.today()
    return f"{today.year}-W{today.isocalendar()[1]:02d}"


def fetch_prices(tickers):
    """Fetch current prices for a list of tickers."""
    prices = {}
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="5d")
            if not hist.empty:
                prices[ticker] = {
                    "current": round(hist["Close"].iloc[-1], 2),
                    "prev_week": round(hist["Close"].iloc[0], 2) if len(hist) >= 5 else None,
                }
        except Exception as e:
            prices[ticker] = {"current": None, "prev_week": None, "error": str(e)}
    return prices


def build_report(holdings, prices):
    flags = []
    rows = []

    for h in holdings:
        t = h["ticker"]
        price_data = prices.get(t, {})
        cmp = price_data.get("current")
        prev = price_data.get("prev_week")

        if cmp is None:
            rows.append(f"| {h['name']:25s} | {t:15s} | ⚠️ No data | — | — | — |")
            flags.append(f"⚠️ **{h['name']}** ({t}): Could not fetch price")
            continue

        # P&L vs cost
        avg = h["avg_price"]
        if avg > 0:
            pl_pct = ((cmp - avg) / avg) * 100
            pl_str = f"{pl_pct:+.1f}%"
        else:
            pl_pct = None
            pl_str = "—"

        # Week change
        if prev and prev > 0:
            wk_chg = ((cmp - prev) / prev) * 100
            wk_str = f"{wk_chg:+.1f}%"
        else:
            wk_chg = None
            wk_str = "—"

        # Flag logic
        grade = h["grade"]
        alerts = []

        if wk_chg is not None:
            if wk_chg <= THRESHOLDS["large_drop_1w_pct"]:
                alerts.append(f"🔴 -{abs(wk_chg):.1f}% this week")
            if wk_chg >= THRESHOLDS["large_gain_1w_pct"]:
                alerts.append(f"🟢 +{wk_chg:.1f}% this week — review thesis")

        if pl_pct is not None:
            if grade == "C" and pl_pct <= THRESHOLDS["grade_c_loss_pct"]:
                alerts.append(f"🔴 Grade C at {pl_pct:+.1f}% — EXIT candidate")
            elif grade == "B" and pl_pct <= THRESHOLDS["grade_b_loss_pct"]:
                alerts.append(f"🟡 Grade B at {pl_pct:+.1f}% — review thesis")

        alert_str = " | ".join(alerts) if alerts else "✅ OK"
        flags.extend([f"**{h['name']}**: {a}" for a in alerts])

        rows.append(
            f"| {h['name']:25s} | {t:15s} | ₹{cmp:,.2f} | {pl_str:>8} | {wk_str:>8} | {alert_str} |"
        )

    return rows, flags


def write_report(rows, flags, week_label):
    out_dir = os.path.join(BASE_DIR, "journal", "weekly")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"red_flags_{week_label}.md")

    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# Red Flag Monitor — {week_label}",
        f"*Generated: {today}*",
        "",
        "## Portfolio Price Check",
        "",
        "| Stock | Ticker | CMP | vs Cost | 1W Chg | Alerts |",
        "|-------|--------|-----|---------|--------|--------|",
    ] + rows + [
        "",
        "## Alerts Summary",
        "",
    ]

    if flags:
        lines += [f"- {f}" for f in flags]
    else:
        lines += ["No alerts — all positions within normal range."]

    lines += [
        "",
        "---",
        f"*Next run: next Sunday | Source: yfinance | Thresholds: ≥8% drop flags red, Grade C ≥35% loss flags exit*",
    ]

    with open(out_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Report written: {out_path}")
    if flags:
        print(f"\n{'='*50}")
        print(f"ALERTS ({len(flags)}):")
        for f in flags:
            print(f"  {f}")
    else:
        print("No alerts.")
    return out_path


def main():
    week_label = get_week_label()
    print(f"Red Flag Monitor — {week_label}")
    print(f"Checking {len(HOLDINGS)} holdings...")

    tickers = [h["ticker"] for h in HOLDINGS]
    prices = fetch_prices(tickers)

    rows, flags = build_report(HOLDINGS, prices)
    out_path = write_report(rows, flags, week_label)
    return 0


if __name__ == "__main__":
    sys.exit(main())
