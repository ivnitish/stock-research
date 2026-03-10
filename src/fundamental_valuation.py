"""
Stock price analysis + fundamental valuation (reusable for any ticker or stock details).
Uses yfinance and Indian-Stock-Market-API. Output: price stats, key ratios, simple fair-value view.
For DCF/multiples you can pass optional assumptions; otherwise uses available data only.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

import pandas as pd
import yfinance as yf

from config import OUTPUT_DIR
from stock_input import StockInput, to_ticker, normalize_stock_input


@dataclass
class ValuationInput:
    """Optional assumptions for valuation. None = use only reported data."""
    revenue_growth_pct: float | None = None   # e.g. 25 for 25%
    terminal_growth_pct: float | None = None  # e.g. 5 for DCF
    discount_rate_pct: float | None = None    # e.g. 12 for WACC
    peer_pe: float | None = None              # for relative valuation
    years_projections: int = 5


def _num(x, default=None):
    try:
        return float(x) if x is not None else default
    except (TypeError, ValueError):
        return default


def get_fundamentals(ticker: str) -> dict:
    """Fetch fundamentals from yfinance (and optionally Indian-Stock-Market-API)."""
    t = yf.Ticker(ticker)
    info = t.info
    out = {
        "ticker": ticker,
        "name": info.get("longName") or info.get("shortName"),
        "currency": info.get("currency", "INR"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": _num(info.get("marketCap")),
        "pe_ratio": _num(info.get("trailingPE") or info.get("forwardPE")),
        "forward_pe": _num(info.get("forwardPE")),
        "pb_ratio": _num(info.get("priceToBook") or info.get("bookValue") and info.get("regularMarketPrice") and (info["regularMarketPrice"] / info["bookValue"])),
        "peg_ratio": _num(info.get("pegRatio")),
        "dividend_yield": _num(info.get("dividendYield"), 0.0),
        "roe": _num(info.get("returnOnEquity")),
        "roa": _num(info.get("returnOnAssets")),
        "debt_to_equity": _num(info.get("debtToEquity")),
        "revenue": _num(info.get("totalRevenue") or info.get("revenue")),
        "net_income": _num(info.get("netIncomeToCommon") or info.get("netIncome")),
        "eps": _num(info.get("trailingEps") or info.get("forwardEps")),
        "book_value": _num(info.get("bookValue")),
        "free_cash_flow": _num(info.get("freeCashflow") or info.get("operatingCashflow")),
        "current_price": _num(info.get("regularMarketPrice") or info.get("currentPrice") or info.get("previousClose")),
    }
    # Fallback: try Indian-Stock-Market-API for price/PE if yfinance sparse
    if (out.get("current_price") is None or out.get("pe_ratio") is None) and ticker.endswith((".NS", ".BO")):
        try:
            from indian_stock_api import get_stock
            api = get_stock(ticker, res="num")
            if api:
                if out.get("current_price") is None:
                    out["current_price"] = _num(api.get("last_price"))
                if out.get("pe_ratio") is None:
                    out["pe_ratio"] = _num(api.get("pe_ratio"))
                if out.get("name") is None:
                    out["name"] = api.get("company_name")
        except Exception:
            pass
    return out


def get_quarterly_results(ticker: str, num_quarters: int = 4) -> list[dict]:
    """
    Fetch recent quarterly income statement. Returns list of dicts, newest first.
    Each dict has: period_end, revenue, net_income, and other keys if available.
    """
    t = yf.Ticker(ticker)
    try:
        q = getattr(t, "quarterly_income_stmt", None)
        if q is None:
            q = t.get_income_stmt(freq="quarterly")
    except Exception:
        return []
    if q is None or (hasattr(q, "empty") and q.empty):
        return []
    if isinstance(q, pd.DataFrame):
        # Columns are period end dates (often newest first); rows are line items.
        cols = list(q.columns)[:num_quarters]
        out = []
        for col in cols:
            period_end = col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col)
            row = {"period_end": period_end}
            for label in q.index:
                if label is None:
                    continue
                try:
                    val = q.loc[label, col]
                except Exception:
                    continue
                if val is None or (isinstance(val, float) and pd.isna(val)):
                    continue
                try:
                    row[str(label).strip()] = float(val)
                except (TypeError, ValueError):
                    pass
            # Normalize common names for display
            for rev_key in ("Total Revenue", "Revenue", "Operating Revenue"):
                if rev_key in row:
                    row["revenue"] = row[rev_key]
                    break
            for ni_key in ("Net Income", "Net Income Common Stockholders", "Net Income Including Noncontrolling Interests"):
                if ni_key in row:
                    row["net_income"] = row[ni_key]
                    break
            out.append(row)
        return out[:num_quarters]
    return []


def price_analysis(ticker: str, period: str = "1y") -> dict:
    """Return price stats: return, high, low, volatility proxy."""
    t = yf.Ticker(ticker)
    hist = t.history(period=period)
    if hist is None or hist.empty or len(hist) < 2:
        return {}
    close = hist["Close"]
    start, end = close.iloc[0], close.iloc[-1]
    total_return_pct = (end / start - 1) * 100
    return {
        "period": period,
        "start_price": round(start, 2),
        "end_price": round(end, 2),
        "high": round(close.max(), 2),
        "low": round(close.min(), 2),
        "total_return_pct": round(total_return_pct, 2),
        "volatility_proxy": round(close.pct_change().std() * 100, 2) if len(close) > 1 else None,
    }


def run_valuation(
    symbol_or_details: StockInput,
    period: str = "1y",
    assumptions: ValuationInput | None = None,
    save_csv: bool = True,
) -> dict:
    """
    Run price analysis + fundamental snapshot + optional simple valuation.
    symbol_or_details: ticker (e.g. GROWW, GROWW.NS) or stock details dict.
    assumptions: optional; if None, only reported metrics are shown.
    Returns combined dict of price stats, fundamentals, and (if possible) simple fair value.
    """
    n = normalize_stock_input(symbol_or_details)
    ticker = n["ticker"]
    if not ticker:
        return {}

    price_stats = price_analysis(ticker, period=period)
    fund = get_fundamentals(ticker)
    quarterly = get_quarterly_results(ticker, num_quarters=4)

    # Simple fair value from P/E if we have EPS and a target P/E
    fair_value_pe = None
    if assumptions and assumptions.peer_pe is not None and fund.get("eps"):
        fair_value_pe = assumptions.peer_pe * fund["eps"]
    elif fund.get("pe_ratio") and fund.get("current_price") and fund.get("eps"):
        # Current implied: price = P/E * EPS; we just report
        pass

    out = {
        "symbol": n["symbol"],
        "ticker": ticker,
        "name": fund.get("name"),
        **price_stats,
        **{k: v for k, v in fund.items() if k not in ("ticker", "name")},
        "fair_value_pe_based": fair_value_pe,
        "quarterly": quarterly,
    }

    # Print summary
    print("\n--- Price analysis ---")
    for k, v in price_stats.items():
        print(f"  {k}: {v}")
    print("\n--- Fundamentals (snapshot) ---")
    for k in ("market_cap", "pe_ratio", "forward_pe", "pb_ratio", "roe", "revenue", "net_income", "eps", "current_price"):
        if out.get(k) is not None:
            print(f"  {k}: {out[k]}")
    if out.get("fair_value_pe_based") is not None:
        print(f"\n  fair_value (P/E peer-based): {out['fair_value_pe_based']:.2f}")
    if quarterly:
        print("\n--- Recent quarterly results ---")
        for qr in quarterly[:4]:
            period_end = qr.get("period_end", "")
            rev = qr.get("revenue") or qr.get("Total Revenue")
            ni = qr.get("net_income") or qr.get("Net Income")
            rev_f = f"  {rev/1e9:.2f}B" if rev is not None else "  —"
            ni_f = f"  {ni/1e9:.2f}B" if ni is not None else "  —"
            print(f"  {period_end}:  Revenue {rev_f}   Net income {ni_f}")

    if save_csv:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        row = {k: v for k, v in out.items() if v is not None and k != "quarterly"}
        pd.DataFrame([row]).to_csv(os.path.join(OUTPUT_DIR, f"valuation_{n['symbol']}.csv"), index=False)
        if quarterly:
            qdf = pd.DataFrame(quarterly)
            qdf.to_csv(os.path.join(OUTPUT_DIR, f"quarterly_{n['symbol']}.csv"), index=False)
            print(f"\nSaved: {OUTPUT_DIR}/valuation_{n['symbol']}.csv, {OUTPUT_DIR}/quarterly_{n['symbol']}.csv")
        else:
            print(f"\nSaved: {OUTPUT_DIR}/valuation_{n['symbol']}.csv")

    return out


if __name__ == "__main__":
    import sys
    stock: StockInput = sys.argv[1] if len(sys.argv) > 1 else "GROWW.NS"
    run_valuation(stock, period="1y")
