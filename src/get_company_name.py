"""
Utility: given a stock ticker or stock details, print the company name.
Uses Indian-Stock-Market-API; falls back to yfinance if API fails.
Usage: python get_company_name.py RELIANCE
       python get_company_name.py TCS.NS
       python get_company_name.py '{"symbol":"INFY","exchange":"BO"}'
"""
import json
import sys

from indian_stock_api import get_company_name as api_name
from stock_input import StockInput


def get_company_name(ticker_or_details: StockInput) -> str | None:
    """Get company name from Indian-Stock-Market-API, else yfinance. Accepts ticker or stock details dict."""
    name = api_name(ticker_or_details, ensure_suffix=True)
    if name:
        return name
    try:
        import yfinance as yf
        from stock_input import to_ticker
        t = yf.Ticker(to_ticker(ticker_or_details))
        info = t.info
        return info.get("longName") or info.get("shortName")
    except Exception:
        return None


def _parse_arg(s: str) -> StockInput:
    """Parse CLI arg: ticker string or JSON object for stock details."""
    s = s.strip()
    if s.startswith("{") and s.endswith("}"):
        return json.loads(s)
    return s


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_company_name.py <SYMBOL or JSON>", file=sys.stderr)
        print("Example: python get_company_name.py RELIANCE", file=sys.stderr)
        sys.exit(1)
    stock_input = _parse_arg(sys.argv[1])
    name = get_company_name(stock_input)
    if name:
        print(name)
    else:
        print("Not found", file=sys.stderr)
        sys.exit(1)

