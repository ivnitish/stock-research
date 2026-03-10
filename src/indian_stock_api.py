"""
Client for Indian-Stock-Market-API (GitHub: 0xramm/Indian-Stock-Market-API).
Free REST API for NSE/BSE prices and company info; no API key.
Accepts stock ticker (str) or stock details (dict); uses stock_input for normalization.
"""
import urllib.parse
import urllib.request
import json

from config import INDIAN_STOCK_API_BASE_URL
from stock_input import to_ticker, normalize_stock_inputs, StockInput

_TIMEOUT = 15


def _get(path: str, params: dict = None) -> dict:
    """GET request to the Indian Stock API. Returns JSON body as dict."""
    url = f"{INDIAN_STOCK_API_BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
        return json.loads(resp.read().decode())


def search(query: str) -> list[dict]:
    """
    Search for stocks by company name or symbol.
    Returns list of matches with symbol, company_name, nse_url, bse_url, etc.
    """
    data = _get("/search", {"q": query})
    if data.get("status") == "error":
        return []
    return data.get("results", [])


def get_stock(symbol_or_details: StockInput, res: str = "num") -> dict | None:
    """
    Get single stock details (price, PE, volume, sector, etc.).
    symbol_or_details: ticker (RELIANCE, RELIANCE.NS) or dict e.g. {"symbol": "TCS", "exchange": "BO"}.
    res: 'num' for numbers only, 'val' for values with units (Crores/Lakhs).
    Returns data dict or None if not found.
    """
    ticker = to_ticker(symbol_or_details)
    data = _get("/stock", {"symbol": ticker, "res": res})
    if data.get("status") != "success":
        return None
    return data.get("data")


def get_stock_list(symbols: list[StockInput], res: str = "num") -> list[dict]:
    """
    Get multiple stocks in one request. symbols: list of tickers or stock-details dicts.
    Returns list of stock objects (symbol, ticker, last_price, pe_ratio, sector, etc.).
    """
    if not symbols:
        return []
    tickers = [to_ticker(s) for s in symbols]
    symbols_param = ",".join(tickers)
    data = _get("/stock/list", {"symbols": symbols_param, "res": res})
    if data.get("status") != "success":
        return []
    return data.get("stocks", [])


def fetch_prices(symbols: list[StockInput]) -> dict[str, float]:
    """
    Fetch latest price for each symbol. symbols: list of tickers or stock-details dicts.
    Returns dict mapping ticker (e.g. RELIANCE.NS) to last_price, or float('nan') if missing.
    """
    normalized = normalize_stock_inputs(symbols)
    tickers = [n["ticker"] for n in normalized]
    stocks = get_stock_list(symbols, res="num")
    out = {t: float("nan") for t in tickers}
    for st in stocks:
        ticker = st.get("ticker")
        price = st.get("last_price")
        if ticker is not None and price is not None:
            out[ticker] = float(price)
    return out


def list_symbols() -> list[dict]:
    """Get list of pre-cached symbols with NSE/BSE tickers (from API /symbols)."""
    data = _get("/symbols")
    if data.get("status") != "success":
        return []
    return data.get("symbols", [])


def get_company_name(symbol_or_details: StockInput, ensure_suffix: bool = True) -> str | None:
    """
    Return company name for a given stock. symbol_or_details: ticker or stock details dict.
    Uses Indian-Stock-Market-API. Returns None if not found.
    """
    ticker = to_ticker(symbol_or_details)
    data = get_stock(ticker, res="num")
    if data:
        return data.get("company_name")
    return None


if __name__ == "__main__":
    # Quick test: search, single stock, list, and fetch_prices
    print("Search 'reliance':", search("reliance")[:2])
    print("Stock RELIANCE.NS:", get_stock("RELIANCE.NS", "num") and "OK")
    print("List ITC, TCS:", [s.get("ticker") for s in get_stock_list(["ITC", "TCS.NS"], "num")])
    print("Fetch prices:", fetch_prices(["RELIANCE.NS", "TCS.NS"]))
