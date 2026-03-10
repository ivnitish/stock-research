"""
Indian stock analysis: fetch NSE/BSE history, returns, and simple stats.
Usage: edit SYMBOLS below or pass as env/list; run from project root.
Symbols can be tickers (RELIANCE.NS) or stock details dicts; all normalized via stock_input.
"""
import os
import pandas as pd
import yfinance as yf
from config import OUTPUT_DIR
from stock_input import normalize_stock_inputs, StockInput


def ensure_ticker(symbol_or_details: StockInput) -> str:
    """Return Yahoo-style ticker. Accepts ticker str or stock details dict."""
    from stock_input import to_ticker
    return to_ticker(symbol_or_details)


def fetch_history(
    symbols: list[StockInput],
    period: str = "1y",
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Fetch historical OHLCV for given symbols (Indian stocks). symbols: tickers or stock-details dicts.
    period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y
    """
    tickers = [x["ticker"] for x in normalize_stock_inputs(symbols)]
    data = yf.download(
        tickers,
        period=period,
        interval=interval,
        group_by="ticker",
        auto_adjust=True,
        progress=False,
    )
    if len(symbols) == 1:
        data.columns = [c if isinstance(c, str) else c[0] for c in data.columns]
    return data


def returns_summary(series: pd.Series) -> dict:
    """Compute simple return stats from a price series."""
    if series is None or series.dropna().empty or len(series.dropna()) < 2:
        return {}
    s = series.dropna()
    total_return = (s.iloc[-1] / s.iloc[0] - 1) * 100
    return {
        "start_price": s.iloc[0],
        "end_price": s.iloc[-1],
        "total_return_pct": round(total_return, 2),
        "min": s.min(),
        "max": s.max(),
    }


def run_analysis(
    symbols: list[str] = None,
    period: str = "1y",
    save_chart: bool = True,
) -> pd.DataFrame:
    """
    Fetch history for symbols, compute return summary, optionally plot and save.
    symbols: list of tickers (str) or stock-details dicts.
    """
    symbols = symbols or ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS"]
    normalized = normalize_stock_inputs(symbols)
    tickers = [x["ticker"] for x in normalized]

    print(f"Fetching {period} history for: {tickers}")
    data = fetch_history(symbols, period=period)

    if data.empty:
        print("No data received. Check symbols (use .NS for NSE, .BO for BSE).")
        return pd.DataFrame()

    # Build summary per symbol (handle single vs multi-ticker download format)
    rows = []
    if len(tickers) == 1:
        close = data["Close"] if "Close" in data.columns else data.iloc[:, 0]
        rows.append({"symbol": tickers[0], **returns_summary(close)})
    else:
        for sym in tickers:
            close = None
            if isinstance(data.columns, pd.MultiIndex):
                if sym in data.columns.get_level_values(0):
                    close = data[sym]["Close"]
            elif "Close" in data.columns:
                close = data["Close"]
            if close is not None:
                rows.append({"symbol": sym, **returns_summary(close)})

    summary = pd.DataFrame(rows)
    print("\n--- Return summary ---")
    print(summary.to_string(index=False))

    if save_chart and not data.empty:
        try:
            import matplotlib.pyplot as plt
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            fig, ax = plt.subplots(figsize=(10, 5))
            if len(tickers) == 1:
                close = data["Close"] if "Close" in data.columns else data.iloc[:, 0]
                close = close / close.iloc[0] * 100
                close.plot(ax=ax, label=tickers[0])
            else:
                for sym in tickers:
                    c = None
                    if isinstance(data.columns, pd.MultiIndex) and sym in data.columns.get_level_values(0):
                        c = data[sym]["Close"]
                    if c is not None and not c.dropna().empty:
                        (c / c.dropna().iloc[0] * 100).plot(ax=ax, label=sym)
            ax.set_title("Normalized price (base 100)")
            ax.set_ylabel("Index")
            ax.legend()
            ax.grid(True, alpha=0.3)
            fig.tight_layout()
            path = os.path.join(OUTPUT_DIR, "stock_analysis.png")
            fig.savefig(path, dpi=150)
            plt.close(fig)
            print(f"\nChart saved: {path}")
        except Exception as e:
            print(f"Could not save chart: {e}")

    return summary


if __name__ == "__main__":
    run_analysis()
