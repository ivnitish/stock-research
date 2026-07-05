#!/usr/bin/env python3
"""Daily portfolio EOD digest -> Telegram. Zero Claude tokens.

Prices from official NSE/BSE udiff bhavcopies (end-of-day close; the legacy
endpoints in src/nse_bhavcopy.py are deprecated upstream and 404 now).
Reads data/portfolio.csv, sends one compact message to the Telegram bot
configured in .env (same creds as telegram_bridge.py).

Usage:
  python3 scripts/daily_portfolio_telegram.py            # fetch + send
  python3 scripts/daily_portfolio_telegram.py --dry-run  # print, don't send
"""

import csv
import io
import sys
import zipfile
from datetime import date, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv
import os

REPO = Path(__file__).resolve().parent.parent
load_dotenv(REPO / ".env")

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
NSE_URL = "https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{d}_F_0000.csv.zip"
BSE_URL = "https://www.bseindia.com/download/BhavCopy/Equity/BhavCopy_BSE_CM_0_0_0_{d}_F_0000.CSV"
NSE_SERIES = {"EQ", "BE", "BZ", "SM", "ST"}


def fetch_bhav(url: str, unzip: bool) -> list[dict] | None:
    r = requests.get(url, headers=UA, timeout=30)
    if r.status_code != 200:
        return None
    raw = r.content
    if unzip:
        zf = zipfile.ZipFile(io.BytesIO(raw))
        raw = zf.read(zf.namelist()[0])
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8", "replace"))))


def last_trading_bhav() -> tuple[date, list[dict], list[dict]]:
    """Walk back from today to find the most recent day with an NSE bhavcopy."""
    d = date.today()
    for _ in range(7):
        ds = d.strftime("%Y%m%d")
        nse = fetch_bhav(NSE_URL.format(d=ds), unzip=True)
        if nse:
            bse = fetch_bhav(BSE_URL.format(d=ds), unzip=False) or []
            return d, nse, bse
        d -= timedelta(days=1)
    raise RuntimeError("no bhavcopy found in the last 7 days")


def build_price_map(nse: list[dict], bse: list[dict]) -> dict[str, tuple[float, float]]:
    """symbol (with .NS/.BO suffix) -> (close, prev_close)"""
    prices = {}
    for row in nse:
        if row.get("SctySrs") in NSE_SERIES:
            try:
                prices[row["TckrSymb"] + ".NS"] = (float(row["ClsPric"]), float(row["PrvsClsgPric"]))
            except (ValueError, KeyError):
                pass
    for row in bse:
        if row.get("FinInstrmTp") == "STK":
            try:
                prices.setdefault(row["TckrSymb"] + ".BO", (float(row["ClsPric"]), float(row["PrvsClsgPric"])))
            except (ValueError, KeyError):
                pass
    return prices


def main() -> None:
    dry_run = "--dry-run" in sys.argv

    holdings = []
    with open(REPO / "data" / "portfolio.csv") as f:
        for row in csv.DictReader(f):
            holdings.append((row["symbol"].strip(), float(row["quantity"]), float(row["avg_buy_price"])))

    trade_date, nse, bse = last_trading_bhav()
    if trade_date != date.today() and not dry_run:
        # Evening weekday run with no fresh bhavcopy = market holiday; skip.
        # (Weekend runs never happen — launchd schedule is Mon-Fri.)
        print(f"no bhavcopy for today; latest is {trade_date} — market holiday, not sending")
        return

    prices = build_price_map(nse, bse)

    lines, missing = [], []
    tot_val = tot_cost = tot_prev = 0.0
    for sym, qty, avg in holdings:
        if sym not in prices:
            missing.append(sym)
            continue
        close, prev = prices[sym]
        day = (close - prev) / prev * 100 if prev else 0.0
        pnl = (close - avg) / avg * 100 if avg else 0.0
        tot_val += qty * close
        tot_cost += qty * avg
        tot_prev += qty * prev
        lines.append((qty * close, f"{sym.split('.')[0]:<12} {close:>9,.1f}  {day:+5.1f}%  P&L {pnl:+6.1f}%"))

    lines.sort(reverse=True)
    day_pct = (tot_val - tot_prev) / tot_prev * 100 if tot_prev else 0.0
    pnl_pct = (tot_val - tot_cost) / tot_cost * 100 if tot_cost else 0.0

    msg = (
        f"Portfolio EOD — {trade_date.strftime('%d %b %Y')}\n"
        f"Value: Rs {tot_val:,.0f}  |  Day {day_pct:+.2f}%  |  P&L {pnl_pct:+.1f}%\n"
        f"{'-' * 34}\n"
        + "\n".join(f"`{text}`" for _, text in lines)
    )
    if missing:
        msg += f"\n{'-' * 34}\nno EOD data: {', '.join(missing)}"

    if dry_run:
        print(msg)
        return

    resp = requests.post(
        f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage",
        json={"chat_id": int(os.environ["TELEGRAM_ALLOWED_CHAT_ID"]), "text": msg, "parse_mode": "Markdown"},
        timeout=30,
    )
    resp.raise_for_status()
    print(f"sent {len(lines)} holdings for {trade_date}")


if __name__ == "__main__":
    main()
