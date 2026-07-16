"""
Client for IndianAPI.in Stock Market API (https://indianapi.in).

This is the paid marketplace API (distinct from the free GitHub indian_stock_api.py).

QUOTA — 500 requests/month on the current plan (user directive 2026-07-17:
use judiciously). Two protections built in:
  1. Every response is disk-cached under data/cache/indianapi/ (default TTL:
     3 days for /stock, 1 hour for /news). Repeat lookups cost nothing.
  2. Every real network hit increments data/cache/indianapi/usage_YYYY-MM.json.
     A stderr warning fires at 450+. Check remaining budget with get_usage().

Verified endpoints (live-tested 2026-07-17):
  GET /stock?name=X        — the workhorse. Accepts company name ("Solex Energy")
                             OR ticker symbol ("SOLEX") as `name`. One call returns:
                             profile, live NSE/BSE price, 8yr annual + quarterly
                             statements (INC/BAL/CAS), keyMetrics (ROE, ROI, margins,
                             D/E, P/E, P/B, PEG, growth rates), shareholding history
                             (promoter/FII/DII), analystView, recentNews, technicals.
  GET /news                — market news list.
  GET /trending            — top gainers/losers.
  GET /historical_data?stock_name=&period=&filter=   (filter is REQUIRED)
  GET /historical_stats?stock_name=&stats=            (e.g. stats=quarter_results)
  Documented but untested: /industry_search, /mutual_fund_search, /price_shockers,
  /commodities, /stock_target_price, /stock_forecasts, /NSE_most_active,
  /BSE_most_active, /fetch_52_week_high_low_data, /mutual_funds.

Endpoints that DO NOT exist (404 "Endpoint not allowed", removed 2026-07-17):
  /company_news, /ai_news, /stock/list, /financials, /ratios, /shareholding —
  all of that data is embedded in the single /stock response.

Auth: header `x-api-key`. Base https://stock.indianapi.in (INDIANAPI_BASE_URL to override).
Key lives in repo .env as INDIANAPI_KEY (config.py loads .env automatically).

UNITS QUIRK in /stock payload (verified against SOLEX Screener numbers):
  - statement maps (INC/BAL/CAS values) and priceandVolume.marketCap: ₹ Cr
  - money fields in other keyMetrics sections (incomeStatement etc.): ₹ millions
    (divide by 10 for ₹ Cr)
  - ratios, percentages, per-share data: unitless / as labelled
Also: keyMetrics key names are dirty (trailing ")", embedded spaces, typos like
"returnOnAverageAssetsMostRecenFiscalYear") — always look up via _km() which
normalizes keys, never by exact string.

Current integration: wired into src/fundamental_valuation.py as richer source
when the key is present.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

from config import BASE_DIR, INDIANAPI_KEY, INDIANAPI_BASE_URL
from stock_input import StockInput, normalize_stock_input

_TIMEOUT = 20
_CACHE_DIR = Path(BASE_DIR) / "data" / "cache" / "indianapi"
_STOCK_TTL = 3 * 86400   # fundamentals: 3 days is fresh enough for research
_NEWS_TTL = 3600         # news: 1 hour
_USAGE_WARN_AT = 450     # of the 500/month plan


# ---------------------------------------------------------------- plumbing

def is_configured() -> bool:
    return bool(INDIANAPI_KEY)


def _cache_path(path: str, params: dict | None) -> Path:
    raw = path + "?" + urllib.parse.urlencode(sorted((params or {}).items()))
    h = hashlib.md5(raw.encode()).hexdigest()[:16]
    slug = re.sub(r"[^A-Za-z0-9]+", "_", raw).strip("_")[:60]
    return _CACHE_DIR / f"{slug}_{h}.json"


def _usage_path() -> Path:
    return _CACHE_DIR / f"usage_{datetime.now():%Y-%m}.json"


def get_usage() -> int:
    """Requests consumed this calendar month (network hits only, cache hits free)."""
    try:
        return json.loads(_usage_path().read_text())["count"]
    except Exception:
        return 0


def _count_usage() -> int:
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    n = get_usage() + 1
    _usage_path().write_text(json.dumps({"count": n}))
    if n >= _USAGE_WARN_AT:
        print(f"WARNING: IndianAPI usage {n}/500 this month — nearly exhausted",
              file=sys.stderr)
    return n


def _get(path: str, params: dict | None = None, ttl: int | None = _STOCK_TTL,
         base: str | None = None) -> dict | list:
    """GET with disk cache. ttl=None forces a network hit (still counted)."""
    if not INDIANAPI_KEY:
        return {"error": "INDIANAPI_KEY not set. Get one from https://indianapi.in/ "
                         "and put it in the repo .env."}

    cp = _cache_path(path, params)
    if ttl and cp.exists() and (time.time() - cp.stat().st_mtime) < ttl:
        try:
            return json.loads(cp.read_text())
        except Exception:
            pass  # corrupt cache — refetch

    base_url = (base or INDIANAPI_BASE_URL).rstrip("/")
    url = f"{base_url}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(
            {k: v for k, v in params.items() if v is not None})

    req = urllib.request.Request(url, method="GET")
    req.add_header("x-api-key", INDIANAPI_KEY)

    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8")
        except Exception:
            err_body = str(e)
        _count_usage()  # failed calls still count against the quota
        return {"error": f"HTTP {e.code}", "body": err_body}
    except Exception as e:
        return {"error": str(e)}

    _count_usage()
    try:
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cp.write_text(json.dumps(data))
    except Exception:
        pass
    return data


def _num(x) -> float | None:
    try:
        return float(str(x).replace(",", ""))
    except (TypeError, ValueError):
        return None


def _norm_key(k: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (k or "").lower())


def _km(stock: dict, section: str, *key_candidates: str) -> float | None:
    """Look up a keyMetrics value with normalized keys; first candidate that hits wins."""
    items = (stock.get("keyMetrics") or {}).get(section) or []
    table = {_norm_key(i.get("key", "")): i.get("value") for i in items
             if isinstance(i, dict)}
    for cand in key_candidates:
        v = table.get(_norm_key(cand))
        if v is not None:
            return _num(v)
    return None


# ---------------------------------------------------------------- endpoints

def get_news(limit: int = 20) -> list[dict]:
    """Latest market news (1h cache)."""
    data = _get("/news", None, ttl=_NEWS_TTL)
    if isinstance(data, list):
        return data[:limit]
    return []


def get_trending() -> dict | None:
    """Top gainers/losers snapshot (1h cache)."""
    data = _get("/trending", None, ttl=_NEWS_TTL)
    return None if isinstance(data, dict) and "error" in data else data


def get_stock(symbol_or_details: StockInput, ttl: int = _STOCK_TTL) -> dict | None:
    """
    Full stock payload from GET /stock?name=. Accepts ticker ("SOLEX", "SOLEX.NS")
    or company name ("Solex Energy"). This is ONE quota request (or free on cache hit).
    """
    n = normalize_stock_input(symbol_or_details)
    name = n["symbol"]  # bare symbol works as name; strip .NS/.BO handled upstream
    data = _get("/stock", {"name": name}, ttl=ttl)
    if isinstance(data, dict) and "error" not in data and data.get("companyName"):
        return data
    return None


def get_company_news(symbol_or_details: StockInput) -> list[dict]:
    """Company news embedded in the /stock payload (no separate endpoint exists)."""
    stock = get_stock(symbol_or_details)
    if not stock:
        return []
    return [x for x in (stock.get("recentNews") or []) if x]


def get_historical_data(stock_name: str, period: str = "1yr",
                        filter: str = "price") -> dict | None:
    """GET /historical_data — `filter` is required by the API (e.g. price, pe, sm)."""
    data = _get("/historical_data",
                {"stock_name": stock_name, "period": period, "filter": filter})
    return None if isinstance(data, dict) and "error" in data else data


def get_historical_stats(stock_name: str, stats: str = "quarter_results") -> dict | None:
    """GET /historical_stats — e.g. stats=quarter_results for quarterly table."""
    data = _get("/historical_stats", {"stock_name": stock_name, "stats": stats})
    return None if isinstance(data, dict) and "error" in data else data


# ---------------------------------------------------------------- fundamentals

def get_fundamentals(symbol_or_details: StockInput) -> dict:
    """
    Screener-like snapshot parsed from a SINGLE /stock call.

    Returns normalized fields (None when absent) plus raw sections. Field notes:
    - roce is actually Refinitiv-style Return on Investment (closest available proxy)
    - market_cap in ₹ Cr; revenue_ttm/pat_ttm converted from millions to ₹ Cr
    - promoter_holding = latest quarter %, promoter_trend = full history
    """
    n = normalize_stock_input(symbol_or_details)
    out: dict[str, Any] = {
        "symbol": n["symbol"], "ticker": n["ticker"],
        "source": "indianapi.in", "error": None,
    }

    stock = get_stock(symbol_or_details)
    if not stock:
        out["error"] = "no /stock data returned"
        return out

    out["name"] = stock.get("companyName")
    out["sector"] = stock.get("industry")

    cp = stock.get("currentPrice") or {}
    out["current_price"] = _num(cp.get("NSE")) or _num(cp.get("BSE"))
    out["year_high"] = _num(stock.get("yearHigh"))
    out["year_low"] = _num(stock.get("yearLow"))

    out["market_cap"] = _km(stock, "priceandVolume", "marketCap")          # ₹ Cr
    out["beta"] = _km(stock, "priceandVolume", "beta")

    out["pe_ratio"] = _km(stock, "valuation",
                          "pPerEBasicExcludingExtraordinaryItemsTTM",
                          "pPerEIncludingExtraordinaryItemsTTM",
                          "pPerEExcludingExtraordinaryItemsMostRecentFiscalYear")
    out["pb_ratio"] = _km(stock, "valuation",
                          "priceToBookMostRecentQuarter",
                          "priceToBookMostRecentFiscalYear")
    out["peg_ratio"] = _km(stock, "valuation", "pegRatio")

    out["roe"] = _km(stock, "mgmtEffectiveness",
                     "returnOnAverageEquityMostRecentFiscalYear)",
                     "returnOnAverageEquityTrailing12Month",
                     "returnOnAverageEquity5YearAverage")
    out["roce"] = _km(stock, "mgmtEffectiveness",   # ROI = closest proxy to ROCE here
                      "returnOnInvestmentMostRecentFiscalYear",
                      "returnOnInvestmentTrailing12Month")
    out["debt_to_equity"] = _km(stock, "financialstrength",
                                "totalDebtPerTotalEquityMostRecentQuarter",
                                "totalDebtPerTotalEquityMostRecentFiscalYear")
    out["interest_coverage"] = _km(stock, "financialstrength",
                                   "netInterestCoverageMostRecentFiscalYear")
    out["opm_ttm"] = _km(stock, "margins", "operatingMarginTrailing12Month")
    out["npm_ttm"] = _km(stock, "margins", "netProfitMarginPercentTrailing12Month")

    rev_m = _km(stock, "incomeStatement", "revenueTrailing12Month)")
    pat_m = _km(stock, "incomeStatement", "netIncomeAvailableToCommonTrailing12Months")
    out["revenue_ttm"] = round(rev_m / 10, 2) if rev_m else None           # ₹ Cr
    out["pat_ttm"] = round(pat_m / 10, 2) if pat_m else None               # ₹ Cr

    out["revenue_growth_3y"] = _km(stock, "growth", "growthRatePercentRevenue3Year")
    out["eps_growth_3y"] = _km(stock, "growth", "growthRatePercentEPS3year")

    # Shareholding: latest promoter % + full trend
    promoter_trend = []
    for grp in stock.get("shareholding") or []:
        if "promoter" in (grp.get("categoryName") or "").lower():
            promoter_trend = sorted(
                [(c.get("holdingDate"), _num(c.get("percentage")))
                 for c in grp.get("categories") or []])
    out["promoter_trend"] = promoter_trend
    out["promoter_holding"] = promoter_trend[-1][1] if promoter_trend else None

    # Raw sections for deep use (names kept for fundamental_valuation.py compat)
    out["financials_raw"] = stock.get("financials")        # 8yr INC/BAL/CAS, ₹ Cr
    out["ratios_raw"] = stock.get("keyMetrics")
    out["shareholding_raw"] = stock.get("shareholding")
    out["analyst_view"] = stock.get("analystView")
    out["recent_news"] = [x for x in (stock.get("recentNews") or []) if x]
    return out


def test_connection() -> dict:
    """Cheap health check — at most ONE quota request (cached news)."""
    if not is_configured():
        return {"status": "not_configured", "message": "Set INDIANAPI_KEY env var"}
    news = get_news(limit=1)
    return {
        "status": "ok" if news else "failed",
        "base_url": INDIANAPI_BASE_URL,
        "usage_this_month": get_usage(),
        "quota": 500,
    }


if __name__ == "__main__":
    print("IndianAPI client — configured:", is_configured())
    print(test_connection())
    if len(sys.argv) > 1:
        f = get_fundamentals(sys.argv[1])
        print(json.dumps({k: v for k, v in f.items()
                          if not k.endswith("_raw") and k != "recent_news"},
                         indent=2, default=str))
        print("usage this month:", get_usage())
