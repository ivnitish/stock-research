#!/usr/bin/env python3
"""Build PDF report for fintwitter finds with thesis + Screener metrics."""

from __future__ import annotations

import json
import subprocess
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JSON_PATH = REPO / "data" / "fintwitter_finds_metrics.json"
HTML_PATH = REPO / "output" / "html" / "FINTWITTER_FINDS.html"
PDF_DIR = REPO / "output" / "pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Screener.in screen + ratios page (7 Jul 2026) where full ratios fetch failed
FALLBACK: dict[str, dict[str, str]] = {
    "Pasupati Acrylon": {
        "mcap_cr": "544", "cmp": "61.0", "pe": "7.7", "bv": "49.8", "pb": "1.23",
        "roce": "21.2", "roe": "16.5", "sales_growth_ttm": "45", "profit_growth_ttm": "133",
        "opm_latest": "12", "promoter": "58", "pledge": "0", "npm": "8.5",
        "sales_cr": "980", "np_cr": "83", "symbol": "PASUPTAC",
    },
    "Shri Techtex": {
        "mcap_cr": "159", "cmp": "63.7", "pe": "8.2", "bv": "47.1", "pb": "1.35",
        "roce": "22.8", "roe": "18.2", "sales_growth_ttm": "10", "profit_growth_ttm": "88",
        "opm_latest": "14", "promoter": "62", "pledge": "0", "npm": "11.2",
        "symbol": "SHRITECH",
    },
    "TGV Sraac": {
        "mcap_cr": "1,110", "cmp": "103.7", "pe": "8.4", "bv": "122", "pb": "0.85",
        "roce": "12.7", "roe": "11.4", "sales_growth_ttm": "5", "profit_growth_ttm": "29",
        "opm_latest": "11", "promoter": "55", "pledge": "0", "npm": "9.8",
        "sales_cr": "2,044", "np_cr": "112", "symbol": "507753",
    },
    "Jay Bee Laminations": {
        "mcap_cr": "640", "cmp": "312", "pe": "18.5", "bv": "98", "pb": "3.2",
        "roce": "24.1", "roe": "19.8", "sales_growth_3y": "59", "sales_growth_ttm": "42",
        "profit_growth_ttm": "38", "opm_latest": "18", "promoter": "72", "pledge": "0",
        "npm": "14.2", "sales_cr": "485", "np_cr": "35", "fcf_cr": "15.8",
        "symbol": "530039", "data_note": "Screener ratios + cash-cow thread (Mar 2026)",
    },
    "Shivalic Power": {
        "mcap_cr": "312", "cmp": "69.0", "pe": "19.2", "bv": "42", "pb": "1.64",
        "roce": "14.0", "roe": "12.5", "sales_growth_ttm": "30", "profit_growth_ttm": "22",
        "opm_latest": "14", "promoter": "68", "pledge": "0", "npm": "7.5",
        "sales_cr": "352", "np_cr": "26", "symbol": "SPCL",
        "data_note": "Equitymaster switchgear list + Screener (Mar 2026)",
    },
    "JM Financial": {
        "mcap_cr": "8,420", "cmp": "142", "pe": "12.8", "bv": "138", "pb": "1.03",
        "roce": "11.2", "roe": "9.8", "sales_growth_ttm": "8", "profit_growth_ttm": "12",
        "opm_latest": "28", "promoter": "25", "pledge": "0", "npm": "22.5",
        "sales_cr": "4,850", "np_cr": "1,095", "debt_cr": "42,100",
        "earnings_yield": "7.8", "symbol": "JMFINACIL",
        "data_note": "Consolidated Screener ratios (7 Jul 2026)",
    },
}

SOURCES: dict[str, str] = {
    "B.R. Goyal Infra": "Ashish Chugh-style Screener screen · IPO 2025",
    "Pasupati Acrylon": "Ashish Chugh hidden gems screen",
    "Canarys Automation": "Ashish Chugh hidden gems screen",
    "Shri Techtex": "Ashish Chugh hidden gems screen",
    "Eleganz Interior": "Ashish Chugh hidden gems screen",
    "TGV Sraac": "Ashish Chugh hidden gems screen",
    "Jay Bee Laminations": "@raghavwadhwa cash-cow thread (Mar 2026)",
    "The Anup Engineering": "@raghavwadhwa cash-cow thread",
    "HPL Electric": "Grid supply chain screen · OB >₹30B",
    "Shivalic Power": "Equitymaster switchgear watchlist 2026",
    "Veto Switchgears": "Grid/switchgear peer screen",
    "Transrail Lighting": "ValuePickr Capt_Cool portfolio · grid T&D threads",
    "JM Financial": "TIA 20-20 summit (@jaganmsna)",
    "Windlas Biotech": "TIA 20-20 summit (@jaganmsna)",
    "Ultramarine Pigments": "iThought PMS thesis",
    "Timken India": "TIA / industrial capex thesis",
    "Carborundum Universal": "@selvaprathee MF flow thread",
}

METRIC_ROWS = [
    ("Market Cap", "mcap_cr", "₹ {} Cr"),
    ("Share Price (CMP)", "cmp", "₹ {}"),
    ("52W High / Low", "high_low", "{}"),
    ("Stock P/E", "pe", "{}"),
    ("Price / Book", "pb", "{}"),
    ("Book Value", "bv", "₹ {}"),
    ("ROCE", "roce", "{}%"),
    ("ROE", "roe", "{}%"),
    ("ROIC", "roic", "{}%"),
    ("Return on Assets", "roa", "{}%"),
    ("Sales (TTM)", "sales_cr", "₹ {} Cr"),
    ("Sales growth (3Y CAGR)", "sales_growth_3y", "{}%"),
    ("Sales growth (Qtr YoY)", "sales_growth_ttm", "{}%"),
    ("EBIT", "ebit_cr", "₹ {} Cr"),
    ("Net Profit", "np_cr", "₹ {} Cr"),
    ("Profit growth (3Y CAGR)", "profit_growth_3y", "{}%"),
    ("Profit growth (Qtr YoY)", "profit_growth_ttm", "{}%"),
    ("OPM (latest Q)", "opm_latest", "{}%"),
    ("NPM (last year)", "npm", "{}%"),
    ("EPS", "eps", "₹ {}"),
    ("Earnings Yield", "earnings_yield", "{}%"),
    ("Debt", "debt_cr", "₹ {} Cr"),
    ("Cash Equivalents", "cash_cr", "₹ {} Cr"),
    ("Free Cash Flow", "fcf_cr", "₹ {} Cr"),
    ("Enterprise Value", "ev_cr", "₹ {} Cr"),
    ("Promoter Holding", "promoter", "{}%"),
    ("Pledged %", "pledge", "{}%"),
    ("Dividend Yield", "div_yield", "{}%"),
    ("Inventory Days", "inv_days", "{}"),
    ("Up from 52W Low", "up_52w", "{}%"),
    ("Down from 52W High", "down_52w", "{}%"),
]


def derive_metrics(d: dict) -> dict:
    """Fill computed ratios when raw fields exist."""
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


def load_data() -> dict:
    raw = json.loads(JSON_PATH.read_text())
    for name, fb in FALLBACK.items():
        if name in raw:
            for k, v in fb.items():
                raw[name].setdefault(k, v)
    for name, d in raw.items():
        d.setdefault("source", SOURCES.get(name, ""))
        derive_metrics(d)
    return raw


def fmt_metric(d: dict, key: str, template: str) -> str | None:
    if key == "high_low":
        if d.get("high_52w") and d.get("low_52w"):
            return f"₹ {d['high_52w']} / ₹ {d['low_52w']}"
        return None
    val = d.get(key)
    if val is None or val == "":
        return None
    return template.format(val)


def render_stock(name: str, d: dict) -> str:
    rows = []
    for label, key, tmpl in METRIC_ROWS:
        v = fmt_metric(d, key, tmpl)
        if v:
            rows.append(f"<tr><td class='k'>{label}</td><td class='v'>{v}</td></tr>")

    note = d.get("data_note", "")
    note_html = f"<p class='note'><em>Data: {note}</em></p>" if note else ""
    symbol = d.get("symbol", "—")
    verdict = d.get("verdict", "")
    bucket = d.get("bucket", "")
    thesis = d.get("thesis", "")
    source = d.get("source", "")

    return f"""
    <section class="stock">
      <div class="hdr">
        <h2>{name}</h2>
        <span class="sym">{symbol}</span>
        <span class="bucket">{bucket}</span>
        <span class="verdict">{verdict}</span>
      </div>
      <div class="thesis"><strong>Why it's here</strong><p>{thesis}</p></div>
      <div class="source"><strong>Source</strong><p>{source}</p></div>
      <table class="metrics">{''.join(rows)}</table>
      {note_html}
    </section>
    """


def render_html(data: dict) -> str:
    order = [
        "A — Value / Manufacturing",
        "B — Grid Supply Chain",
        "C — TIA / Serious Investors",
    ]
    by_bucket: dict[str, list[tuple[str, dict]]] = {b: [] for b in order}
    for name, d in data.items():
        b = d.get("bucket", "Other")
        by_bucket.setdefault(b, []).append((name, d))

    body = []
    for bucket in order:
        items = by_bucket.get(bucket, [])
        if not items:
            continue
        body.append(f"<h1 class='bucket-title'>{bucket}</h1>")
        for name, d in items:
            body.append(render_stock(name, d))

    today = date.today().strftime("%d %B %Y")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Fintwitter Finds — {today}</title>
<style>
  @page {{ margin: 18mm 14mm; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
          font-size: 10.5pt; color: #1a1a1a; line-height: 1.45; max-width: 210mm; margin: 0 auto; }}
  .cover {{ padding: 24px 0 32px; border-bottom: 3px solid #1e3a5f; margin-bottom: 28px; }}
  .cover h1 {{ font-size: 22pt; margin: 0 0 8px; color: #1e3a5f; }}
  .cover p {{ margin: 4px 0; color: #444; }}
  .bucket-title {{ font-size: 14pt; color: #1e3a5f; margin: 28px 0 12px; padding-bottom: 6px;
                   border-bottom: 1px solid #ccc; page-break-after: avoid; }}
  .stock {{ margin-bottom: 22px; page-break-inside: avoid; border: 1px solid #e0e0e0;
            border-radius: 6px; padding: 14px 16px; background: #fafbfc; }}
  .hdr {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 8px 14px; margin-bottom: 10px; }}
  .hdr h2 {{ margin: 0; font-size: 13pt; flex: 1 1 100%; }}
  .sym {{ font-size: 9pt; color: #666; background: #eee; padding: 2px 8px; border-radius: 4px; }}
  .bucket {{ font-size: 8.5pt; color: #555; }}
  .verdict {{ font-size: 9pt; font-weight: 600; color: #0d5c2e; background: #e8f5e9; padding: 2px 8px; border-radius: 4px; }}
  .thesis, .source {{ margin: 10px 0 8px; }}
  .thesis strong, .source strong {{ display: block; font-size: 9pt; text-transform: uppercase; letter-spacing: 0.04em;
                    color: #555; margin-bottom: 4px; }}
  .thesis p, .source p {{ margin: 0; }}
  .source p {{ font-size: 9.5pt; color: #444; }}
  table.metrics {{ width: 100%; border-collapse: collapse; font-size: 9.5pt; }}
  table.metrics td {{ padding: 4px 8px; border-bottom: 1px solid #ececec; vertical-align: top; }}
  table.metrics td.k {{ width: 42%; color: #555; }}
  table.metrics td.v {{ font-weight: 500; }}
  .note {{ font-size: 8.5pt; color: #777; margin: 8px 0 0; }}
  .footer {{ margin-top: 32px; padding-top: 12px; border-top: 1px solid #ddd; font-size: 8.5pt; color: #888; }}
</style>
</head>
<body>
  <div class="cover">
    <h1>Fintwitter Finds — Less Discovered, Thesis-Backed</h1>
    <p>Prepared {today} · Data: Screener.in (consolidated where available)</p>
    <p>Contrarian lens: prefer grid supply chain &amp; value manufacturing over crowded defence/EMS rerates.</p>
    <p>Not investment advice. Verify numbers before acting.</p>
  </div>
  {''.join(body)}
  <div class="footer">
    Sources: Indian fintwitter / ValuePickr / ThreadReader threads (Jul 2026) cross-checked on Screener.in.
    Crowded skips: INDOTECH, KAYNES, ZENTEC, MTAR, APOLLO, PARAS.
  </div>
</body>
</html>"""


def main() -> int:
    data = load_data()
    HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    html = render_html(data)
    HTML_PATH.write_text(html, encoding="utf-8")

    pdf_name = f"FINTWITTER_FINDS_{date.today().isoformat()}.pdf"
    pdf_path = PDF_DIR / pdf_name
    for old in PDF_DIR.glob("FINTWITTER_FINDS_*.pdf"):
        old.unlink()

    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}", f"file://{HTML_PATH.resolve()}",
    ]
    subprocess.run(cmd, check=True, timeout=60)
    print(f"HTML: {HTML_PATH}")
    print(f"PDF:  {pdf_path} ({pdf_path.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())