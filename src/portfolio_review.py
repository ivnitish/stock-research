"""
Indian stock portfolio review: load holdings, fetch live NSE/BSE prices,
compute P&L and allocation. Run from project root.
Supports two price sources: yfinance (default) or Indian-Stock-Market-API (free, no key).
Portfolio CSV symbol column: ticker (RELIANCE.NS) or plain symbol (RELIANCE); optional JSON for details.
"""
import os
import pandas as pd
import yfinance as yf
from config import PORTFOLIO_PATH, OUTPUT_DIR
from stock_input import to_ticker


def ensure_ticker(symbol_or_details) -> str:
    """Ensure symbol has Yahoo suffix (.NS or .BO). Accepts ticker str or stock details dict."""
    return to_ticker(symbol_or_details)


def load_portfolio(path: str = None) -> pd.DataFrame:
    """Load portfolio from CSV. Expected columns: symbol, quantity, avg_buy_price[, exchange]."""
    path = path or PORTFOLIO_PATH
    df = pd.read_csv(path)
    df["symbol"] = df["symbol"].apply(ensure_ticker)
    df["cost"] = df["quantity"] * df["avg_buy_price"]
    return df


def fetch_prices_yfinance(symbols: list[str]) -> dict[str, float]:
    """Fetch latest close price for each symbol (Indian stocks via yfinance)."""
    out = {}
    for s in symbols:
        try:
            t = yf.Ticker(s)
            hist = t.history(period="5d")
            if hist is not None and not hist.empty:
                out[s] = float(hist["Close"].iloc[-1])
            else:
                out[s] = float("nan")
        except Exception as e:
            print(f"Warning: could not fetch {s}: {e}")
            out[s] = float("nan")
    return out


def fetch_prices(symbols: list[str], source: str = None) -> dict[str, float]:
    """
    Fetch latest price for each symbol. source: 'yfinance' | 'indian_api'.
    Default: env USE_INDIAN_STOCK_API=1 → indian_api, else yfinance.
    """
    if source is None:
        source = "indian_api" if os.environ.get("USE_INDIAN_STOCK_API") else "yfinance"
    if source == "indian_api":
        try:
            from indian_stock_api import fetch_prices as api_fetch_prices
            return api_fetch_prices(symbols)
        except Exception as e:
            print(f"Warning: Indian-Stock-Market-API failed ({e}), falling back to yfinance")
            return fetch_prices_yfinance(symbols)
    return fetch_prices_yfinance(symbols)


def run_review(
    portfolio_path: str = None,
    save_csv: bool = True,
    price_source: str = None,
) -> pd.DataFrame:
    """
    Load portfolio, fetch prices, compute current value, P&L and allocation.
    price_source: 'yfinance' | 'indian_api' (or set env USE_INDIAN_STOCK_API=1 for indian_api).
    Returns summary DataFrame; optionally saves to output/portfolio_review.csv.
    """
    df = load_portfolio(portfolio_path)
    symbols = df["symbol"].unique().tolist()
    prices = fetch_prices(symbols, source=price_source)
    df["current_price"] = df["symbol"].map(prices)
    df["current_value"] = df["quantity"] * df["current_price"]
    df["pnl"] = df["current_value"] - df["cost"]
    df["pnl_pct"] = (df["pnl"] / df["cost"] * 100).round(2)

    total_cost = df["cost"].sum()
    total_value = df["current_value"].sum()
    df["allocation_pct"] = (df["current_value"] / total_value * 100).round(2)

    summary = df[
        [
            "symbol",
            "quantity",
            "avg_buy_price",
            "current_price",
            "cost",
            "current_value",
            "pnl",
            "pnl_pct",
            "allocation_pct",
        ]
    ].copy()
    summary.columns = [
        "Symbol",
        "Qty",
        "Avg Buy",
        "Current Price",
        "Cost",
        "Current Value",
        "P&L",
        "P&L %",
        "Allocation %",
    ]

    print("\n--- Portfolio summary ---")
    print(summary.to_string(index=False))
    print(f"\nTotal cost:    ₹{total_cost:,.2f}")
    print(f"Total value:   ₹{total_value:,.2f}")
    print(f"Total P&L:     ₹{total_value - total_cost:,.2f} ({(total_value / total_cost - 1) * 100:.2f}%)")

    if save_csv:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        out_path = os.path.join(OUTPUT_DIR, "portfolio_review.csv")
        summary.to_csv(out_path, index=False)
        print(f"\nSaved: {out_path}")

    return summary


if __name__ == "__main__":
    run_review()
