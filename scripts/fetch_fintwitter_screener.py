#!/usr/bin/env python3
"""Fetch Screener.in metrics and merge into fintwitter JSON.

Tries multiple symbol aliases and consolidated/standalone paths.
Falls back to direct Screener HTML when jina reader returns empty ratios.
"""

from __future__ import annotations

import json
import re
import time
import urllib.request
from html import unescape
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JSON_PATH = REPO / "data" / "fintwitter_finds_metrics.json"

# name -> list of (symbol, use_consolidated)
SYMBOL_ALIASES: dict[str, list[tuple[str, bool]]] = {
    "B.R. Goyal Infra": [("544335", True)],
    "Pasupati Acrylon": [("PASUPTAC", True), ("PASUPTAC", False)],
    "Canarys Automation": [("CANARYS", True)],
    "Shri Techtex": [("SHRITECH", True), ("SHRITECH", False)],
    "Eleganz Interior": [("ELGNZ", True)],
    "TGV Sraac": [("507753", False), ("507753", True), ("TGVSLA", True)],
    "Jay Bee Laminations": [("JAYBEE", False), ("530039", False)],
    "The Anup Engineering": [("ANUP", True)],
    "HPL Electric": [("HPL", True)],
    "Shivalic Power": [("SPCL", False)],  # SME — standalone only
    "Veto Switchgears": [("VETO", True)],
    "Transrail Lighting": [("TRANSRAILL", True)],
    "JM Financial": [("JMFINANCIL", True), ("JMFINANCIL", False)],
    "Windlas Biotech": [("WINDLAS", True)],
    "Ultramarine Pigments": [("ULTRAMAR", True)],
    "Timken India": [("TIMKEN", True)],
    "Carborundum Universal": [("CARBORUNIV", True)],
}

JINA = "https://r.jina.ai/https://www.screener.in/company/{sym}/{path}"
SCREENER = "https://www.screener.in/company/{sym}/{path}"


def fetch_url(url: str, timeout: int = 45) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def num(s: str) -> str | None:
    s = s.replace(",", "").replace("₹", "").strip()
    if not s or s in ("-", "—"):
        return None
    return s


def parse_bullets_md(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    patterns = {
        "mcap_cr": r"Market Cap\s*₹\s*([\d,.]+)\s*Cr",
        "cmp": r"Current Price\s*₹\s*([\d,.]+)",
        "high_52w": r"High / Low\s*₹\s*([\d,.]+)\s*/\s*₹\s*([\d,.]+)",
        "pe": r"Stock P/E\s*([\d,.]+)",
        "bv": r"Book Value\s*₹\s*([\d,.]+)",
        "div_yield": r"Dividend Yield\s*([\d,.]+)\s*%",
        "roce": r"ROCE\s*([\d,.]+)\s*%",
        "roe": r"ROE\s*([\d,.]+)\s*%",
    }
    for key, pat in patterns.items():
        m = re.search(pat, text)
        if not m:
            continue
        if key == "high_52w":
            out["high_52w"] = num(m.group(1)) or ""
            out["low_52w"] = num(m.group(2)) or ""
        else:
            out[key] = num(m.group(1)) or ""
    return out


def parse_bullets_html(html: str) -> dict[str, str]:
    out: dict[str, str] = {}
    m = re.search(r'<ul id="top-ratios".*?</ul>', html, re.DOTALL)
    if not m:
        return out
    block = m.group(0)
    for li in re.finditer(
        r'<li class="flex flex-space-between".*?</li>', block, re.DOTALL
    ):
        item = li.group(0)
        name_m = re.search(r'<span class="name">(.*?)</span>', item, re.DOTALL)
        if not name_m:
            continue
        label = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", name_m.group(1))).strip()
        nums = re.findall(r'<span class="number">([^<]+)</span>', item)
        if not nums:
            continue
        val = unescape(nums[0].strip())
        mapping = {
            "Market Cap": "mcap_cr",
            "Current Price": "cmp",
            "Stock P/E": "pe",
            "Book Value": "bv",
            "Dividend Yield": "div_yield",
            "ROCE": "roce",
            "ROE": "roe",
        }
        if label == "High / Low" and len(nums) >= 2:
            out["high_52w"] = num(nums[0]) or ""
            out["low_52w"] = num(nums[1]) or ""
        elif label in mapping:
            out[mapping[label]] = num(val) or ""
    return out


def parse_compounded(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    m = re.search(
        r"Compounded Sales Growth\s*\n*\|[^\n]+\n\|[^\n]+\n\|[^\n]+\n\|[^\n]+\n\|[^\n]+\n\|[^\n]+\n\|[^\n]+\n\|([^\n|]+)",
        text,
    )
    if m:
        out["sales_growth_3y"] = num(m.group(1).strip()) or ""
    m = re.search(
        r"Compounded Profit Growth\s*\n*\n*\|[^\n]+\n\|[^\n]+\n\|[^\n]+\n\|[^\n]+\n\|[^\n]+\n\|[^\n]+\n\|([^\n|]+)",
        text,
    )
    if m:
        out["profit_growth_3y"] = num(m.group(1).strip()) or ""
    # TTM from peer table style
    sg = re.search(r"Qtr Sales Var %\s*\|[^\n]+\n(?:\|[^\n]+\n)*\|[^\n]*\|\s*([\d.\-]+)", text)
    if not sg:
        sg = re.search(r"Sales growth \(Qtr YoY\)", text)
    return out


def parse_quarterly(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    m = re.search(r"\| OPM % \|(.*?)\|\n", text)
    if m:
        cells = [c.strip() for c in m.group(1).split("|") if c.strip()]
        for c in reversed(cells):
            pct = re.search(r"(\d+)%", c)
            if pct:
                out["opm_latest"] = pct.group(1)
                break
    m = re.search(r"\| EPS in Rs \|(.*?)\|\n", text)
    if m:
        cells = [c.strip() for c in m.group(1).split("|") if c.strip()]
        for c in reversed(cells):
            v = num(c)
            if v:
                out["eps"] = v
                break
    # Peer table Qtr growth
    m = re.search(
        r"\| Qtr Sales Var % \|.*?\n\|.*?\n.*?\|.*?\n.*?\|.*?\n.*?\|.*?\|.*?([\d.\-]+)\s*\|",
        text,
    )
    if m:
        out["sales_growth_ttm"] = num(m.group(1)) or ""
    m = re.search(
        r"\| Qtr Profit Var % \|.*?\n\|.*?\n.*?\|.*?\n.*?\|.*?\|.*?([\d.\-]+)\s*\|",
        text,
    )
    if m:
        out["profit_growth_ttm"] = num(m.group(1)) or ""
    return out


def parse_annual(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    block_m = re.search(
        r"\| Mar 20\d\d \|.*?\n(.*?)(?:\n\n|\| Raw PDF|\| Compounded)", text, re.DOTALL
    )
    if not block_m:
        return out
    block = block_m.group(0)
    for label, key in [
        ("Sales", "sales_cr"),
        ("Net Profit", "np_cr"),
        ("EBIT", "ebit_cr"),
        ("OPM %", "npm"),
        ("Debt", "debt_cr"),
        ("Cash Equivalents", "cash_cr"),
    ]:
        row = re.search(rf"\| {re.escape(label)} \|(.*?)\|\n", block)
        if not row:
            continue
        cells = [c.strip() for c in row.group(1).split("|") if c.strip()]
        for c in reversed(cells):
            if label == "OPM %":
                pct = re.search(r"(\d+)%", c)
                if pct:
                    out["npm"] = pct.group(1)
                    break
            else:
                v = num(re.sub(r"[^\d.\-]", "", c) if re.search(r"[\d,]", c) else "")
                if v:
                    out[key] = v
                    break
    return out


def parse_working_capital(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    row = re.search(r"\| Inventory Days \|(.*?)\|\n", text)
    if row:
        cells = [c.strip() for c in row.group(1).split("|") if c.strip()]
        for c in reversed(cells):
            v = num(re.sub(r"[^\d.]", "", c))
            if v:
                out["inv_days"] = v
                break
    row = re.search(r"\| Free Cash Flow \|(.*?)\|\n", text)
    if row:
        cells = [c.strip() for c in row.group(1).split("|") if c.strip()]
        for c in reversed(cells):
            raw = re.search(r"-?[\d,]+", c)
            if raw:
                out["fcf_cr"] = raw.group(0).replace(",", "")
                break
    return out


def derive(d: dict[str, str]) -> dict[str, str]:
    try:
        if d.get("cmp") and d.get("bv") and not d.get("pb"):
            d["pb"] = f"{float(str(d['cmp']).replace(',', '')) / float(str(d['bv']).replace(',', '')):.2f}"
    except (ValueError, ZeroDivisionError):
        pass
    try:
        if d.get("np_cr") and d.get("mcap_cr") and not d.get("earnings_yield"):
            np_v = float(str(d["np_cr"]).replace(",", ""))
            mc = float(str(d["mcap_cr"]).replace(",", ""))
            d["earnings_yield"] = f"{np_v / mc * 100:.2f}"
    except (ValueError, ZeroDivisionError):
        pass
    try:
        cmp_f = float(str(d["cmp"]).replace(",", ""))
        if d.get("low_52w") and not d.get("up_52w"):
            low = float(str(d["low_52w"]).replace(",", ""))
            d["up_52w"] = f"{(cmp_f - low) / low * 100:.1f}"
        if d.get("high_52w") and not d.get("down_52w"):
            high = float(str(d["high_52w"]).replace(",", ""))
            d["down_52w"] = f"{(high - cmp_f) / high * 100:.1f}"
    except (ValueError, ZeroDivisionError, KeyError):
        pass
    return d


def parse_all(text: str, symbol: str, consolidated: bool) -> dict[str, str]:
    data: dict[str, str] = {
        "symbol": symbol,
        "data_note": f"Screener.in {'consolidated' if consolidated else 'standalone'} (auto-fetch)",
    }
    bullets = parse_bullets_md(text)
    if not bullets.get("cmp"):
        bullets = parse_bullets_html(text)
    data.update({k: v for k, v in bullets.items() if v})
    for part in (parse_compounded, parse_quarterly, parse_annual, parse_working_capital):
        data.update({k: v for k, v in part(text).items() if v})
    return derive(data)


def is_valid(d: dict[str, str]) -> bool:
    return bool(d.get("cmp") and d.get("pe"))


def fetch_one(symbol: str, consolidated: bool = True) -> dict[str, str]:
    path = "consolidated/" if consolidated else ""
    # jina markdown
    try:
        md = fetch_url(JINA.format(sym=symbol, path=path))
        data = parse_all(md, symbol, consolidated)
        if is_valid(data):
            return data
    except Exception:
        pass
    # direct HTML
    try:
        html = fetch_url(SCREENER.format(sym=symbol, path=path))
        data = parse_all(html, symbol, consolidated)
        if is_valid(data):
            return data
    except Exception:
        pass
    return {}


def main() -> int:
    existing = json.loads(JSON_PATH.read_text())
    for name, aliases in SYMBOL_ALIASES.items():
        print(f"fetching {name}...")
        fetched: dict[str, str] = {}
        for symbol, consolidated in aliases:
            try:
                fetched = fetch_one(symbol, consolidated)
            except Exception as exc:
                print(f"  FAIL {symbol}: {exc}")
                continue
            if is_valid(fetched):
                print(f"  OK via {symbol} ({'cons' if consolidated else 'std'})")
                break
            time.sleep(0.4)
        if not is_valid(fetched):
            print(f"  SKIP — no valid data (keeping existing)")
            continue
        row = existing.setdefault(name, {})
        for k, v in fetched.items():
            if k not in row or not row[k]:
                row[k] = v
            elif k in ("cmp", "mcap_cr", "pe", "symbol") and v:
                row[k] = v
        time.sleep(0.6)
    JSON_PATH.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n")
    print(f"updated {JSON_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())