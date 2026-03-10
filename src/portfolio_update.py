"""
Automated portfolio value update. Fetches current prices via yfinance,
updates portfolio with latest values, and saves a daily snapshot.

Designed to run as a cron job — no Claude tokens needed.

Usage:
  python src/portfolio_update.py           # Update and print summary
  python src/portfolio_update.py --quiet   # Silent (for cron)
"""
from __future__ import annotations

import os
import sys
from datetime import date

import pandas as pd
import yfinance as yf

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import PORTFOLIO_PATH, OUTPUT_DIR


def update_portfolio(quiet: bool = False) -> pd.DataFrame:
    if not os.path.exists(PORTFOLIO_PATH):
        print(f"ERROR: {PORTFOLIO_PATH} not found. Run groww_importer.py first.")
        sys.exit(1)

    df = pd.read_csv(PORTFOLIO_PATH)
    symbols = df["symbol"].tolist()

    # Fetch current prices
    prices = {}
    for sym in symbols:
        try:
            t = yf.Ticker(sym)
            info = t.info
            price = info.get("regularMarketPrice") or info.get("currentPrice") or info.get("previousClose")
            if price:
                prices[sym] = float(price)
        except Exception:
            pass

    # Update DataFrame
    df["current_price"] = df["symbol"].map(prices)
    df["current_value"] = df["current_price"] * df["quantity"]
    df["invested_value"] = df["avg_buy_price"] * df["quantity"]
    df["pnl"] = df["current_value"] - df["invested_value"]
    df["pnl_pct"] = (df["pnl"] / df["invested_value"] * 100).round(2)

    # Save updated portfolio
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = date.today().isoformat()
    snapshot_path = os.path.join(OUTPUT_DIR, f"portfolio_{today}.csv")
    df.to_csv(snapshot_path, index=False)

    if not quiet:
        total_invested = df["invested_value"].sum()
        total_current = df["current_value"].sum()
        total_pnl = total_current - total_invested
        pnl_pct = (total_pnl / total_invested * 100) if total_invested else 0

        print(f"Portfolio Update — {today}")
        print(f"  Invested:  ₹{total_invested:,.0f}")
        print(f"  Current:   ₹{total_current:,.0f}")
        print(f"  P&L:       ₹{total_pnl:,.0f} ({pnl_pct:.1f}%)")
        print(f"  Stocks:    {len(df)} ({len(prices)} prices fetched)")
        print(f"  Saved:     {snapshot_path}")

        # Top gainers and losers
        valid = df.dropna(subset=["pnl_pct"]).sort_values("pnl_pct")
        if len(valid) >= 3:
            print("\n  Top losers:")
            for _, r in valid.head(3).iterrows():
                print(f"    {r['symbol']:20s} {r['pnl_pct']:+.1f}%  ₹{r['pnl']:+,.0f}")
            print("  Top gainers:")
            for _, r in valid.tail(3).iterrows():
                print(f"    {r['symbol']:20s} {r['pnl_pct']:+.1f}%  ₹{r['pnl']:+,.0f}")

    return df


if __name__ == "__main__":
    quiet = "--quiet" in sys.argv
    update_portfolio(quiet=quiet)
