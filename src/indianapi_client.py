"""
Client for IndianAPI.in Stock Market API (https://indianapi.in).

This is the paid marketplace API (distinct from the free GitHub indian_stock_api.py).

Capabilities (based on docs):
- News: /news , company-specific news, AI-curated insights
- Stock details + financials: quarterly/yearly P&L, balance sheets, cash flows,
  ratios (P/E, ROCE, ROE etc.), shareholding patterns, key metrics, analyst views.

Setup:
1. Sign up at https://indianapi.in/
2. Subscribe to the Stock / Indian Stock Exchange API (sandbox at /sandbox/indian-stock-market)
3. Export INDIANAPI_KEY=your_key
4. Optionally override INDIANAPI_BASE_URL (default https://stock.indianapi.in)

Usage examples:
    from indianapi_client import get_news, get_stock, get_company_news, get_fundamentals

    news = get_news(limit=10)
    stock = get_stock("SOLEX")
    fundamentals = get_fundamentals("SOLEX.NS")

TODO (user reminder 2026-07-07): Test this later. User said "we will test indian api later then - remember".
When ready: set INDIANAPI_KEY, run test_connection(), get_fundamentals on theme stocks (SOLEX, ASM, Bondada, MTAR, etc.), verify news + financials payloads, then enhance further (PDF tables, morning brief, batch for 2026 themes).
Current integration: already wired into src/fundamental_valuation.py as richer source when key present.
"""

from __future__ import annotations

import os
import urllib.parse
import urllib.request
import json
from typing import Any

from config import INDIANAPI_KEY, INDIANAPI_BASE_URL
from stock_input import StockInput, to_ticker, normalize_stock_input, normalize_stock_inputs

_TIMEOUT = 20
_DEFAULT_LIMIT = 20


def _headers() -> dict[str, str]:
    if not INDIANAPI_KEY:
        return {}
    # Docs use both 'x-api-key' and 'X-API-Key'. We use lowercase as primary.
    return {"x-api-key": INDIANAPI_KEY}


def _get(path: str, params: dict | None = None, base: str | None = None) -> dict | list:
    """
    Internal GET helper. Returns parsed JSON or error dict.
    """
    if not INDIANAPI_KEY:
        return {"error": "INDIANAPI_KEY not set. Get one from https://indianapi.in/ and export it."}

    base_url = (base or INDIANAPI_BASE_URL).rstrip("/")
    url = f"{base_url}{path}"
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})

    req = urllib.request.Request(url, method="GET")
    for k, v in _headers().items():
        req.add_header(k, v)

    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8")
        except Exception:
            err_body = str(e)
        return {"error": f"HTTP {e.code}", "body": err_body}
    except Exception as e:
        return {"error": str(e)}


def is_configured() -> bool:
    """Quick check if the API key is present."""
    return bool(INDIANAPI_KEY)


def get_news(limit: int = _DEFAULT_LIMIT, category: str | None = None) -> list[dict]:
    """
    Fetch latest stock market / general news.
    """
    params = {"limit": limit}
    if category:
        params["category"] = category
    data = _get("/news", params)
    if isinstance(data, dict) and "error" in data:
        return []
    if isinstance(data, list):
        return data
    # Common response shapes
    return data.get("news", data.get("data", data.get("results", []))) or []


def get_company_news(symbol_or_details: StockInput, limit: int = 10) -> list[dict]:
    """
    Company-specific news.
    """
    n = normalize_stock_input(symbol_or_details)
    symbol = n["symbol"]
    data = _get("/company_news", {"symbol": symbol, "limit": limit})
    if isinstance(data, dict) and "error" in data:
        return []
    if isinstance(data, list):
        return data
    return data.get("news", data.get("data", [])) or []


def get_ai_news(limit: int = 10, topic: str | None = None) -> list[dict]:
    """AI-curated financial insights/news (if the endpoint exists)."""
    params = {"limit": limit}
    if topic:
        params["topic"] = topic
    data = _get("/ai_news", params)
    if isinstance(data, dict) and "error" in data:
        return []
    return data.get("news", data.get("data", [])) or [] if not isinstance(data, list) else data


def get_stock(symbol_or_details: StockInput, **extra_params) -> dict | None:
    """
    Get detailed stock information. Often includes price, profile, key metrics,
    and in richer responses: financial statements or links to them.
    """
    n = normalize_stock_input(symbol_or_details)
    symbol = n["symbol"]
    params = {"symbol": symbol, **extra_params}
    data = _get("/stock", params)
    if isinstance(data, dict) and "error" in data:
        return None
    if isinstance(data, dict):
        return data.get("data", data)
    return data


def get_stock_list(symbols: list[StockInput]) -> list[dict]:
    """Batch stock details if the endpoint supports comma-separated symbols."""
    if not symbols:
        return []
    tickers = [normalize_stock_input(s)["symbol"] for s in symbols]
    data = _get("/stock/list", {"symbols": ",".join(tickers)})
    if isinstance(data, dict) and "error" in data:
        return []
    return data.get("stocks", data.get("data", [])) or []


def get_financials(symbol_or_details: StockInput, period: str = "quarterly") -> dict | None:
    """
    Attempt to fetch detailed financials (P&L, balance sheet, cash flow).
    The exact path may vary — common candidates: /financials, /results, /statements.
    Returns raw response so you can inspect structure.
    """
    n = normalize_stock_input(symbol_or_details)
    symbol = n["symbol"]
    # Try the most likely paths
    for path in ["/financials", "/results", "/statements", f"/financials/{symbol}"]:
        data = _get(path, {"symbol": symbol, "period": period})
        if isinstance(data, dict) and "error" not in data and data:
            return data
    # Fallback: sometimes financials are embedded in /stock
    stock = get_stock(symbol_or_details)
    if stock and any(k in str(stock).lower() for k in ["profit", "balance", "cashflow", "pl", "pnl"]):
        return {"embedded_in_stock": True, "stock_data": stock}
    return None


def get_ratios(symbol_or_details: StockInput) -> dict | None:
    """Key ratios if separate endpoint exists."""
    n = normalize_stock_input(symbol_or_details)
    symbol = n["symbol"]
    for path in ["/ratios", "/key_ratios"]:
        data = _get(path, {"symbol": symbol})
        if isinstance(data, dict) and "error" not in data and data:
            return data
    return None


def get_shareholding(symbol_or_details: StockInput) -> dict | None:
    """Shareholding pattern (promoter %, FII, DII, etc.)."""
    n = normalize_stock_input(symbol_or_details)
    symbol = n["symbol"]
    for path in ["/shareholding", "/shareholding_pattern", "/holdings"]:
        data = _get(path, {"symbol": symbol})
        if isinstance(data, dict) and "error" not in data and data:
            return data
    return None


def get_fundamentals(symbol_or_details: StockInput) -> dict:
    """
    Best-effort Screener-like snapshot.
    Tries to combine stock details + financials + ratios + shareholding.
    Returns a normalized dict + raw sections for full inspection.
    """
    n = normalize_stock_input(symbol_or_details)
    symbol = n["symbol"]
    ticker = n["ticker"]

    out = {
        "symbol": symbol,
        "ticker": ticker,
        "source": "indianapi.in",
        "error": None,
    }

    stock = get_stock(symbol)
    if stock:
        out["stock_raw"] = stock
        # Try common field names
        out["name"] = stock.get("company_name") or stock.get("name") or stock.get("longName")
        out["current_price"] = stock.get("last_price") or stock.get("price") or stock.get("close")
        out["market_cap"] = stock.get("market_cap") or stock.get("marketCap")
        out["pe_ratio"] = stock.get("pe") or stock.get("pe_ratio") or stock.get("trailingPE")
        out["sector"] = stock.get("sector") or stock.get("industry")

    # Enrich with separate calls if available
    fin = get_financials(symbol)
    if fin:
        out["financials_raw"] = fin

    ratios = get_ratios(symbol)
    if ratios:
        out["ratios_raw"] = ratios
        # Try to pull common ratios
        out["roe"] = ratios.get("roe") or ratios.get("return_on_equity")
        out["roce"] = ratios.get("roce") or ratios.get("return_on_capital_employed")
        out["debt_to_equity"] = ratios.get("debt_to_equity")

    sh = get_shareholding(symbol)
    if sh:
        out["shareholding_raw"] = sh
        out["promoter_holding"] = sh.get("promoter") or sh.get("promoters")

    if not any(k in out for k in ["market_cap", "pe_ratio", "financials_raw"]):
        out["error"] = "Limited data returned. Check exact endpoints in the sandbox for this symbol."

    return out


def test_connection() -> dict:
    """Quick health check + sample news."""
    if not is_configured():
        return {"status": "not_configured", "message": "Set INDIANAPI_KEY env var"}

    news = get_news(limit=3)
    sample_stock = get_stock("RELIANCE")
    return {
        "status": "ok" if news or sample_stock else "partial",
        "news_sample_count": len(news),
        "sample_stock_keys": list(sample_stock.keys()) if isinstance(sample_stock, dict) else None,
        "base_url": INDIANAPI_BASE_URL,
    }


if __name__ == "__main__":
    print("IndianAPI client test")
    print("Configured:", is_configured())
    print("Connection test:", test_connection())

    if is_configured():
        print("\n--- Sample news ---")
        print(get_news(limit=5)[:2])

        print("\n--- Sample stock (RELIANCE) ---")
        print(get_stock("RELIANCE"))

        print("\n--- Fundamentals for a theme stock (try SOLEX or your pick) ---")
        print(get_fundamentals("SOLEX"))
