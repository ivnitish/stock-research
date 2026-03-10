"""
Single source of truth for stock identity across the repo.
Every script and module accepts either a stock ticker (str) or stock details (dict).
Use normalize_stock_input() once at the boundary; pass the result or .ticker to downstream code.
"""
from __future__ import annotations

from typing import Any

from config import DEFAULT_EXCHANGE

# Accept either a ticker string (RELIANCE, RELIANCE.NS) or details dict (symbol, series, exchange)
StockInput = str | dict[str, Any]


def normalize_stock_input(
    ticker_or_details: StockInput,
    default_exchange: str | None = None,
) -> dict[str, Any]:
    """
    Normalize ticker or stock-details into one canonical dict. Use this at entry points
    (CLI, API, portfolio row) so the rest of the repo gets a single shape.

    Input examples:
      - "RELIANCE" or "RELIANCE.NS" or "RELIANCE.BO"
      - {"symbol": "TCS", "series": "EQ"}
      - {"symbol": "INFY", "exchange": "BO"}  # BSE
      - {"SYMBOL": "HDFCBANK", "SERIES": "EQ"}

    Returns dict with:
      - symbol: plain symbol (RELIANCE)
      - series: EQ default
      - exchange: "NS" | "BO" (default from config)
      - ticker: Yahoo-style for default exchange (RELIANCE.NS)
      - ticker_nse: RELIANCE.NS
      - ticker_bse: RELIANCE.BO
    """
    ex = (default_exchange or DEFAULT_EXCHANGE).upper()
    if ex not in ("NS", "BO"):
        ex = "NS"

    if isinstance(ticker_or_details, dict):
        d = ticker_or_details
        symbol = (d.get("symbol") or d.get("SYMBOL") or "").strip().upper()
        series = (d.get("series") or d.get("SERIES") or "EQ").strip().upper()
        exchange = (d.get("exchange") or d.get("EXCHANGE") or ex).upper()
        if exchange not in ("NS", "BO"):
            exchange = "NS"
    else:
        s = (ticker_or_details or "").strip().upper()
        if s.endswith(".NS"):
            symbol, series, exchange = s[:-3], "EQ", "NS"
        elif s.endswith(".BO"):
            symbol, series, exchange = s[:-3], "EQ", "BO"
        else:
            symbol, series, exchange = s, "EQ", ex

    ticker_nse = f"{symbol}.NS" if symbol else ""
    ticker_bse = f"{symbol}.BO" if symbol else ""
    ticker = ticker_nse if exchange == "NS" else ticker_bse

    return {
        "symbol": symbol,
        "series": series,
        "exchange": exchange,
        "ticker": ticker,
        "ticker_nse": ticker_nse,
        "ticker_bse": ticker_bse,
    }


def normalize_stock_inputs(
    tickers_or_details: list[StockInput],
    default_exchange: str | None = None,
) -> list[dict[str, Any]]:
    """Normalize a list of tickers or details. Skips empty; returns list of canonical dicts."""
    out = []
    for x in tickers_or_details:
        n = normalize_stock_input(x, default_exchange=default_exchange)
        if n.get("symbol"):
            out.append(n)
    return out


def to_ticker(ticker_or_details: StockInput, exchange: str | None = None) -> str:
    """Return Yahoo-style ticker (e.g. RELIANCE.NS) for the given input. Optional exchange override."""
    n = normalize_stock_input(ticker_or_details, default_exchange=exchange)
    if exchange and exchange.upper() == "BO":
        return n["ticker_bse"]
    return n["ticker"]


def to_symbol_series(ticker_or_details: StockInput) -> tuple[str, str]:
    """Return (symbol, series) for NSE bhav copy / EQ lookup."""
    n = normalize_stock_input(ticker_or_details)
    return n["symbol"], n["series"]
