#!/usr/bin/env python3
"""
Single entry point: run any stock workflow with a ticker or stock details.
Keeps the repo reusable: same input shape (ticker or details) for every command.

Usage:
  python run_stock.py <ticker_or_details> <command> [command_args...]
  python run_stock.py RELIANCE company-name
  python run_stock.py '{"symbol":"TCS","series":"EQ"}' company-name
  python run_stock.py RELIANCE.NS eod 2025-02-07
  python run_stock.py RELIANCE analysis --period 6mo

Commands:
  company-name     Print company name (Indian-Stock-Market-API / yfinance).
  eod [YYYY-MM-DD] Get EOD for date (NSE bhav copy); default today.
  stock-info       Full stock info (price, PE, sector) from Indian-Stock-Market-API.
  valuation        Price analysis + fundamentals + simple valuation (optional assumptions).
"""
import json
import sys
from datetime import date, datetime

import config  # noqa: F401 — triggers sys.path setup for src/
from stock_input import StockInput


def _parse_stock_arg(s: str) -> StockInput:
    s = s.strip()
    if s.startswith("{") and s.endswith("}"):
        return json.loads(s)
    return s


def cmd_company_name(stock: StockInput) -> int:
    from src.get_company_name import get_company_name
    name = get_company_name(stock)
    if name:
        print(name)
        return 0
    print("Not found", file=sys.stderr)
    return 1


def cmd_eod(stock: StockInput, d: date) -> int:
    from src.nse_bhavcopy import get_eod
    eod = get_eod(stock, d, try_nse=True)
    if eod:
        for k, v in eod.items():
            print(f"  {k}: {v}")
        return 0
    print("No EOD data (missing bhav copy or symbol not found).", file=sys.stderr)
    return 1


def cmd_stock_info(stock: StockInput) -> int:
    from src.indian_stock_api import get_stock
    from stock_input import to_ticker
    data = get_stock(stock, res="num")
    if not data:
        print("Not found", file=sys.stderr)
        return 1
    for k, v in data.items():
        print(f"  {k}: {v}")
    return 0


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__.strip(), file=sys.stderr)
        return 1
    stock_arg = sys.argv[1]
    command = (sys.argv[2] or "").strip().lower()
    stock: StockInput = _parse_stock_arg(stock_arg)

    if command == "company-name":
        return cmd_company_name(stock)
    if command == "eod":
        d = date.today()
        if len(sys.argv) >= 4:
            try:
                d = datetime.strptime(sys.argv[3], "%Y-%m-%d").date()
            except ValueError:
                print("Date must be YYYY-MM-DD", file=sys.stderr)
                return 1
        return cmd_eod(stock, d)
    if command == "stock-info":
        return cmd_stock_info(stock)
    if command == "valuation":
        period = "1y"
        args = sys.argv[3:]
        if "--period" in args and args.index("--period") + 1 < len(args):
            period = args[args.index("--period") + 1]
        from src.fundamental_valuation import run_valuation
        run_valuation(stock, period=period)
        return 0
    if command == "analysis":
        period = "1y"
        args = sys.argv[3:]
        if "--period" in args:
            idx = args.index("--period")
            if idx + 1 < len(args):
                period = args[idx + 1]
        from src.stock_analysis import run_analysis
        run_analysis(symbols=[stock], period=period)
        return 0

    print(f"Unknown command: {command}", file=sys.stderr)
    print("Commands: company-name, eod [YYYY-MM-DD], stock-info, valuation [--period 1y], analysis [--period 6mo]", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
