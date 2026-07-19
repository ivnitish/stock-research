#!/usr/bin/env python3
"""Collect deterministic inputs for the morning news brief. Zero Claude tokens.

Gathers everything mechanical so the headless Claude run only analyzes and
writes (decided with user 2026-07-18):
  - last-24h headlines per holding (Google News RSS; 3-day window on Mondays)
  - India + US macro headlines
  - buy-at alerts precomputed from bhavcopy closes vs data/buyat_alerts.csv
  - last 3 entries of docs/MACRO_THREAD.md for narrative continuity

Writes data/daily_inputs/YYYY-MM-DD.md and prints the path. Non-fatal on any
single feed failure — failures are noted inside the output file so the Claude
step knows to use its escape hatch (max 3 targeted fetches) for those names.

Usage:
  venv/bin/python3 scripts/collect_daily_inputs.py            # write file
  venv/bin/python3 scripts/collect_daily_inputs.py --stdout   # print, don't write
"""

import csv
import html
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from daily_portfolio_telegram import build_price_map, last_trading_bhav

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "data" / "daily_inputs"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
GN_URL = "https://news.google.com/rss/search?q={q}%20when:{d}d&hl=en-IN&gl=IN&ceid=IN:en"

MACRO_QUERIES = [
    ("India macro", 'India economy OR RBI OR rupee OR "inflation India"', 8),
    ("India markets", "Nifty OR Sensex OR FII OR smallcap", 6),
    ("US macro", '"Federal Reserve" OR "US inflation" OR "US markets"', 6),
]


def strip_tags(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", text or "")).strip()


def rss_items(query: str, days: int, limit: int) -> list[dict]:
    url = GN_URL.format(q=quote(query), d=days)
    r = requests.get(url, headers=UA, timeout=20)
    r.raise_for_status()
    root = ET.fromstring(r.content)
    items = []
    for it in root.iter("item"):
        title = strip_tags(it.findtext("title", ""))
        source = (it.find("{https://news.google.com/rss}source") is not None
                  and it.find("{https://news.google.com/rss}source").text) or ""
        if not source:
            src_el = it.find("source")
            source = src_el.text if src_el is not None else ""
        pub = it.findtext("pubDate", "")[:16]  # "Sat, 18 Jul 2026"
        link = it.findtext("link", "")
        items.append({"title": title, "source": source, "date": pub, "link": link})
        if len(items) >= limit:
            break
    return items


def holdings_by_cost_basis() -> list[tuple[str, float]]:
    rows = []
    with open(REPO / "data" / "portfolio.csv") as f:
        for row in csv.DictReader(f):
            rows.append((row["symbol"].strip(),
                         float(row["quantity"]) * float(row["avg_buy_price"])))
    rows.sort(key=lambda r: -r[1])
    return rows


def company_queries() -> dict[str, tuple[str, str]]:
    """symbol -> (display name, RSS query)"""
    out = {}
    with open(REPO / "data" / "company_names.csv") as f:
        for row in csv.DictReader(f):
            q = row["query"].strip() or f'"{row["name"]}"'
            out[row["symbol"].strip()] = (row["name"].strip(), q)
    return out


def macro_thread_tail(n_entries: int = 3) -> str:
    path = REPO / "docs" / "MACRO_THREAD.md"
    if not path.exists():
        return "(docs/MACRO_THREAD.md missing)"
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## ", text)
    entries = ["## " + p.rstrip() for p in parts[1:1 + n_entries]]
    return "\n\n".join(entries) if entries else "(no entries yet)"


def buyat_alerts() -> tuple[str, list[str]]:
    """Returns (bhavcopy date line, alert lines) computed from closes."""
    with open(REPO / "data" / "buyat_alerts.csv") as f:
        alerts = list(csv.DictReader(f))
    trade_date, nse, bse = last_trading_bhav()
    prices = build_price_map(nse, bse)
    lines = []
    for a in alerts:
        sym, bhav, trig = a["symbol"], a["bhav_symbol"], float(a["trigger"])
        if bhav not in prices:
            lines.append(f"- {sym}: NO PRICE DATA (bhav symbol {bhav} not found) — {a['note']}")
            continue
        close, _ = prices[bhav]
        gap = (close - trig) / trig * 100
        state = "INSIDE zone" if close < trig else f"outside ({gap:+.1f}% above trigger)"
        lines.append(f"- {sym}: close Rs {close:,.1f} vs trigger <Rs {trig:,.0f} — {state}. {a['note']}")
    return f"Closes from bhavcopy of {trade_date}", lines


def main() -> int:
    to_stdout = "--stdout" in sys.argv
    today = date.today()
    days = 3 if today.weekday() == 0 else 1  # Monday covers the weekend

    queries = company_queries()
    failures = []

    sections = [f"# Daily inputs — {today}",
                f"Generated {datetime.now():%Y-%m-%d %H:%M} by collect_daily_inputs.py. "
                f"News window: last {days} day(s). All headlines are from Google News RSS — "
                f"headline-depth only; use the escape hatch (max 3 targeted WebFetch/WebSearch) "
                f"for items that are material but unclear from the headline."]

    bhav_line, alert_lines = buyat_alerts()
    sections.append("## Buy-at alerts (precomputed — copy into the brief as-is)\n"
                    + bhav_line + "\n" + "\n".join(alert_lines))

    sections.append("## Macro thread context (last entries of docs/MACRO_THREAD.md)\n"
                    + macro_thread_tail())

    hold_parts = ["## Holdings headlines (cost-basis order; silent = no items found)"]
    for sym, _basis in holdings_by_cost_basis():
        name, q = queries.get(sym, (sym.split(".")[0], f'"{sym.split(".")[0]}"'))
        try:
            items = rss_items(q + " stock", days, limit=5)
        except Exception as e:
            failures.append(f"{sym}: {e}")
            continue
        if not items:
            continue
        block = [f"### {sym.split('.')[0]} ({name})"]
        block += [f"- {i['title']} — {i['source']} ({i['date']}) {i['link']}" for i in items]
        hold_parts.append("\n".join(block))
    sections.append("\n\n".join(hold_parts))

    for label, q, limit in MACRO_QUERIES:
        try:
            items = rss_items(q, days, limit)
            body = "\n".join(f"- {i['title']} — {i['source']} ({i['date']}) {i['link']}"
                             for i in items) or "(nothing found)"
        except Exception as e:
            failures.append(f"{label}: {e}")
            body = f"(feed failed: {e})"
        sections.append(f"## {label} headlines\n{body}")

    if failures:
        sections.append("## Collector failures (use escape hatch / fallback for these)\n"
                        + "\n".join(f"- {f}" for f in failures))

    doc = "\n\n".join(sections) + "\n"
    if to_stdout:
        print(doc)
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{today}.md"
    out.write_text(doc, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
