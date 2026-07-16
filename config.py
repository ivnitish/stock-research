"""
Config for Indian stock analysis.
Use NSE tickers with .NS suffix (e.g. RELIANCE.NS); for BSE use .BO.
"""
import os
import sys

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
PORTFOLIO_PATH = os.path.join(BASE_DIR, "data", "portfolio.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
RESEARCH_DIR = os.path.join(BASE_DIR, "research")
JOURNAL_DIR = os.path.join(BASE_DIR, "journal")
SKILLS_DIR = os.path.join(BASE_DIR, "skills")
GROWW_DATA_DIR = os.path.join(BASE_DIR, "data", "groww")
# NSE bhav copy: place downloaded cm*.*.csv or YYYY-MM-DD.csv here, or we try to fetch from NSE
BHAV_COPY_DIR = os.path.join(BASE_DIR, "data", "bhav")

# Add src/ to path so modules within src/ can import each other
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Load repo .env into os.environ (existing env vars win) so API keys work
# in every entry point — interactive, cron/launchd, and one-off scripts.
_ENV_PATH = os.path.join(BASE_DIR, ".env")
if os.path.exists(_ENV_PATH):
    with open(_ENV_PATH) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

# Default exchange suffix for symbols without one
DEFAULT_EXCHANGE = "NS"  # NSE; use "BO" for BSE

# Indian-Stock-Market-API (GitHub: 0xramm/Indian-Stock-Market-API). No API key. Override with env INDIAN_STOCK_API_BASE_URL.
INDIAN_STOCK_API_BASE_URL = os.environ.get(
    "INDIAN_STOCK_API_BASE_URL",
    "https://military-jobye-haiqstudios-14f59639.koyeb.app",
).rstrip("/")

# IndianAPI.in Stock Market API (marketplace at https://indianapi.in/indian-stock-market)
# Richer data: news, company profiles, financials (P&L/BS/CF), ratios, shareholding patterns, etc.
# Requires signup + API key (set INDIANAPI_KEY). Base can be overridden.
# See https://indianapi.in/sandbox/indian-stock-market and analyst.indianapi.in for endpoints.
INDIANAPI_KEY = os.environ.get("INDIANAPI_KEY")
INDIANAPI_BASE_URL = os.environ.get(
    "INDIANAPI_BASE_URL", "https://stock.indianapi.in"
).rstrip("/")
