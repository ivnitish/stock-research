#!/usr/bin/env python3
"""
Rebuild the "Expected CAGR — Thesis-Based Estimates" section in
output/html/index.html from live data.

Source of truth:
  - portfolio.csv for what is held + qty/avg
  - index.html stock rows for CMP and combined Target·Upside cell
    (already reconciled by src/recompute_target_upside.py)
  - research/SYMBOL.md for an optional one-line thesis note

Computes per row:
  - PF weight = current value / total India current value
  - CAGR = (Target/CMP)^(1/horizon) - 1, default 3yr horizon
  - Weighted contribution = weight × CAGR

Sorted by current value desc to match the holdings table.

Idempotent — replaces the existing #expected-cagr section in place.
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "output" / "html" / "index.html"
CSV_PATH = ROOT / "data" / "portfolio.csv"
RESEARCH_DIR = ROOT / "research"

ROW_RE = re.compile(r"<tr class=\"stock-row\"[^>]*>.*?</tr>", re.DOTALL)
TD_RE = re.compile(r"<td[^>]*>.*?</td>", re.DOTALL)
SECTION_RE = re.compile(
    r'<section id="expected-cagr"[^>]*>.*?</section>',
    re.DOTALL,
)

DEFAULT_HORIZON_YEARS = 3


def parse_price(s: str) -> float | None:
    if not s or "—" in s:
        return None
    range_m = re.match(r"[₹$]?([\d,]+(?:\.\d+)?)\s*-\s*[₹$]?([\d,]+(?:\.\d+)?)", s)
    if range_m:
        a = float(range_m.group(1).replace(",", ""))
        b = float(range_m.group(2).replace(",", ""))
        return (a + b) / 2
    m = re.search(r"[₹$]?([\d,]+(?:\.\d+)?)", s)
    if not m:
        return None
    return float(m.group(1).replace(",", ""))


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def fmt_inr(v: float) -> str:
    if v >= 1_00_00_000:
        return f"₹{v/1_00_00_000:.2f}Cr"
    if v >= 1_00_000:
        return f"₹{v/1_00_000:.2f}L"
    if v >= 1_000:
        return f"₹{v/1_000:,.1f}K"
    return f"₹{v:,.0f}"


def load_holdings() -> dict[str, dict]:
    out = {}
    with open(CSV_PATH) as f:
        for r in csv.DictReader(f):
            sym = r["symbol"].replace(".NS", "").replace(".BO", "")
            out[sym] = {
                "qty": float(r["quantity"]),
                "avg": float(r["avg_buy_price"]),
            }
    return out


def parse_html_rows(html: str) -> dict[str, dict]:
    """Return ticker -> {grade, cmp, target_text, upside_pct, action, url}."""
    out = {}
    for m in ROW_RE.finditer(html):
        row = m.group(0)
        tds = TD_RE.findall(row)
        if len(tds) != 7:
            continue
        ticker_m = re.search(r'<div class="td-ticker">([^<]+)<', tds[0])
        if not ticker_m:
            continue
        ticker = ticker_m.group(1).strip()
        if ticker in out:
            continue  # take the first occurrence
        url_m = re.search(r"onclick=\"go\('([^']+)'\)\"", row)
        grade_text = strip_tags(tds[1])
        action_text = strip_tags(tds[2])
        cmp_text = strip_tags(tds[3])
        cmp_v = parse_price(cmp_text)
        combined = strip_tags(tds[5])
        target_text = combined.split("·")[0].strip()
        target_v = parse_price(target_text)
        up_m = re.search(r"([+-]?\d+)%", combined)
        upside = float(up_m.group(1)) if up_m else None
        out[ticker] = {
            "url": url_m.group(1) if url_m else None,
            "grade": grade_text,
            "action": action_text,
            "cmp_text": cmp_text,
            "cmp": cmp_v,
            "target_text": target_text,
            "target": target_v,
            "upside": upside,
        }
    return out


def parse_grade_letter_score(grade_text: str) -> tuple[str, int]:
    m = re.search(r"([A-C])[+\-–]?\s*[·\s]*(\d{1,2})", grade_text)
    if not m:
        return ("?", 0)
    return (m.group(1), int(m.group(2)))


def extract_thesis_note(symbol: str) -> str:
    """Look in research/SYMBOL.md for a one-line thesis hook."""
    path = RESEARCH_DIR / f"{symbol}.md"
    if not path.exists():
        return ""
    txt = path.read_text(errors="ignore")
    # Try in order:
    # 1. The bullet right after "Why this business?" header
    why_m = re.search(r"(?:^|\n)#+\s*Why this business\??\s*\n+(.{20,300}?)\n\n", txt, re.DOTALL)
    if why_m:
        first_sentence = re.split(r"(?<=[.!?])\s+", why_m.group(1).strip(), maxsplit=1)[0]
        first_sentence = re.sub(r"\s+", " ", first_sentence)
        return first_sentence[:180]
    # 2. First line after "## Why this is a monitor position" (stubs)
    mon_m = re.search(r"## Why this is a monitor position\s*\n+(.{20,300}?)\n\n", txt, re.DOTALL)
    if mon_m:
        first_sentence = re.split(r"(?<=[.!?])\s+", mon_m.group(1).strip(), maxsplit=1)[0]
        return first_sentence[:180]
    return ""


def extract_horizon(symbol: str) -> int:
    """Look for explicit horizon in research note. Default 3yr."""
    path = RESEARCH_DIR / f"{symbol}.md"
    if not path.exists():
        return DEFAULT_HORIZON_YEARS
    txt = path.read_text(errors="ignore")
    # Patterns: "3yr CAGR", "Horizon: 2 years", "over 5 years"
    m = re.search(r"\b(\d)\s*[-]?\s*(?:yr|year)s?\s*(?:CAGR|horizon|target)", txt, re.IGNORECASE)
    if m:
        n = int(m.group(1))
        if 1 <= n <= 7:
            return n
    return DEFAULT_HORIZON_YEARS


def render(rows: list[dict], total_current: float, weighted_cagr: float, coverage_pct: float) -> str:
    grade_styles = {
        "A": ("#d4edda", "#155724"),
        "B": ("#fff3cd", "#856404"),
        "C": ("#fee2e2", "#721c24"),
    }
    body_rows = []
    alt = False
    for r in rows:
        alt = not alt
        bg = "#fafafa" if alt else "white"
        gl, gscore = parse_grade_letter_score(r["grade"])
        gb, gf = grade_styles.get(gl, ("#eee", "#666"))
        cagr_str = "—"
        cagr_color = "#94a3b8"
        wcontrib_str = "—"
        if r["cagr"] is not None:
            sign = "+" if r["cagr"] >= 0 else ""
            cagr_str = f"{sign}{r['cagr']:.1f}%"
            if r["cagr"] >= 15:
                cagr_color = "#166534"
            elif r["cagr"] >= 5:
                cagr_color = "#0891b2"
            elif r["cagr"] >= 0:
                cagr_color = "#666"
            else:
                cagr_color = "#991b1b"
            wsign = "+" if r["wcontrib"] >= 0 else ""
            wcontrib_str = f"{wsign}{r['wcontrib']:.2f}%"

        click = f' onclick="window.location.href=\'{r["url"]}\'"' if r["url"] else ""
        cursor = "cursor:pointer" if r["url"] else ""

        body_rows.append(
            f'<tr style="border-bottom:1px solid #f1f5f9;background:{bg};{cursor}"{click}>'
            f'<td style="padding:8px 12px;font-weight:700;color:#0f172a">{r["ticker"]}</td>'
            f'<td style="padding:8px 12px"><span style="background:{gb};color:{gf};font-size:0.65rem;font-weight:700;padding:2px 7px;border-radius:10px">{r["grade"]}</span></td>'
            f'<td style="padding:8px 12px;text-align:right;font-size:0.78rem">{r["weight"]:.1f}%</td>'
            f'<td style="padding:8px 12px;text-align:right;font-size:0.78rem">{r["cmp_text"]}</td>'
            f'<td style="padding:8px 12px;text-align:right;font-size:0.78rem">{r["target_text"]}</td>'
            f'<td style="padding:8px 12px;text-align:right;font-size:0.78rem;color:#64748b">{r["horizon"]}yr</td>'
            f'<td style="padding:8px 12px;text-align:right;font-weight:700;color:{cagr_color}">{cagr_str}</td>'
            f'<td style="padding:8px 12px;text-align:right;color:{cagr_color}">{wcontrib_str}</td>'
            f'<td style="padding:8px 12px;color:#555;font-size:0.74rem">{r["note"]}</td>'
            f'</tr>'
        )

    cagr_color = "#16a34a" if weighted_cagr >= 12 else ("#0891b2" if weighted_cagr >= 0 else "#dc2626")

    section = f'''<section id="expected-cagr" style="max-width:1100px;margin:36px auto 0;padding:0 16px;font-family:-apple-system,sans-serif">

  <div style="border-top:2px solid #1a1a2e;padding-top:24px;margin-bottom:18px">
    <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#888;margin-bottom:6px">Portfolio Analytics · Auto-generated from portfolio.csv + research targets</div>
    <h2 style="font-size:1.3rem;font-weight:700;color:#1a1a2e;margin:0 0 6px">
      Expected CAGR — Thesis-Based Estimates
    </h2>
    <p style="font-size:0.82rem;color:#555;margin:0;line-height:1.6">
      Base-case price targets from research notes, mapped to annualised CAGR over the stated horizon (default 3yr).
      <strong>Not a prediction</strong> — these are the returns implied by the thesis <em>if it plays out</em>.
      Coverage: {coverage_pct:.0f}% of portfolio value has a base target. Rows without a target contribute 0% to the weighted CAGR.
    </p>
  </div>

  <div style="overflow-x:auto;margin-bottom:16px">
  <table style="width:100%;border-collapse:collapse;font-family:-apple-system,sans-serif;font-size:0.81rem;min-width:760px">
    <thead>
      <tr style="background:#1a1a2e;color:#fff">
        <th style="padding:9px 12px;text-align:left">Stock</th>
        <th style="padding:9px 12px;text-align:left">Grade</th>
        <th style="padding:9px 12px;text-align:right">PF Wt</th>
        <th style="padding:9px 12px;text-align:right">CMP</th>
        <th style="padding:9px 12px;text-align:right">Base Target</th>
        <th style="padding:9px 12px;text-align:right">Horizon</th>
        <th style="padding:9px 12px;text-align:right">Exp. CAGR</th>
        <th style="padding:9px 12px;text-align:right">Wtd Contrib.</th>
        <th style="padding:9px 12px;text-align:left">Thesis note</th>
      </tr>
    </thead>
    <tbody>
      {"".join(body_rows)}
      <tr style="background:#1a1a2e;color:white;font-weight:700">
        <td style="padding:10px 12px">Portfolio Weighted CAGR</td>
        <td colspan="2" style="padding:10px 12px;text-align:right;color:#e2e8f0">{len(rows)} holdings · {fmt_inr(total_current)} current</td>
        <td colspan="3" style="padding:10px 12px"></td>
        <td style="padding:10px 12px;text-align:right;color:{cagr_color};font-size:1.05rem">{weighted_cagr:+.1f}%</td>
        <td colspan="2" style="padding:10px 12px;color:#9090b0;font-size:0.78rem">Σ weighted contributions</td>
      </tr>
    </tbody>
  </table>
  </div>

  <div style="font-size:0.72rem;color:#999;text-align:right;margin-bottom:8px">
    CAGR = (Base Target / CMP)<sup>1/Horizon</sup> − 1 · Generated 2026-05-19 · Targets from research notes (rerun with <code>src/build_expected_cagr.py</code>)
  </div>

</section>'''

    return section


def main():
    html = HTML_PATH.read_text()
    holdings = load_holdings()
    row_data = parse_html_rows(html)

    # Compute current value per holding
    rows = []
    total_current = 0.0
    coverage_current = 0.0

    for sym, h in holdings.items():
        if sym not in row_data:
            continue
        rd = row_data[sym]
        cmp_v = rd["cmp"]
        if cmp_v is None or cmp_v == 0:
            continue
        current = h["qty"] * cmp_v
        total_current += current

    if total_current == 0:
        print("No current values — aborting.")
        return

    for sym, h in holdings.items():
        if sym not in row_data:
            print(f"  ⚠ {sym}: no row in index.html")
            continue
        rd = row_data[sym]
        if rd["cmp"] is None:
            continue
        current = h["qty"] * rd["cmp"]
        weight = current / total_current * 100

        target = rd["target"]
        cagr = None
        wcontrib = 0.0
        horizon = extract_horizon(sym)
        if target and rd["cmp"]:
            ratio = target / rd["cmp"]
            cagr = (ratio ** (1.0 / horizon) - 1.0) * 100
            wcontrib = (weight / 100) * cagr
            coverage_current += current

        note = extract_thesis_note(sym)
        rows.append({
            "ticker": sym,
            "url": rd["url"],
            "grade": rd["grade"],
            "weight": weight,
            "current": current,
            "cmp_text": rd["cmp_text"],
            "target_text": rd["target_text"] if target else "—",
            "horizon": horizon,
            "cagr": cagr,
            "wcontrib": wcontrib,
            "note": note,
        })

    rows.sort(key=lambda r: -r["current"])

    weighted_cagr = sum(r["wcontrib"] for r in rows)
    coverage_pct = (coverage_current / total_current) * 100 if total_current else 0

    print(f"Holdings rendered: {len(rows)}")
    print(f"Total current: {fmt_inr(total_current)}")
    print(f"Weighted CAGR: {weighted_cagr:+.2f}%")
    print(f"Coverage (rows with target): {coverage_pct:.0f}%")
    print()
    print(f"  {'Ticker':<14}{'Wt%':>6}  {'CMP':>10}  {'Target':>10}  {'Hzn':>4}  {'CAGR':>7}  {'Wtd':>6}")
    for r in rows:
        cagr = f"{r['cagr']:+.1f}%" if r['cagr'] is not None else "—"
        wc = f"{r['wcontrib']:+.2f}%"
        print(f"  {r['ticker']:<14}{r['weight']:>5.1f}%  {r['cmp_text']:>10}  {r['target_text']:>10}  {r['horizon']:>3}yr  {cagr:>7}  {wc:>6}")

    section = render(rows, total_current, weighted_cagr, coverage_pct)

    if SECTION_RE.search(html):
        new_html = SECTION_RE.sub(section, html, count=1)
        print("\n✓ Replaced existing #expected-cagr section.")
    else:
        # Insert before the closing </body> as fallback
        new_html = html.replace("</body>", section + "\n</body>", 1)
        print("\n⚠ #expected-cagr section not found — appended before </body>.")

    HTML_PATH.write_text(new_html)
    print(f"✓ Wrote {HTML_PATH}")


if __name__ == "__main__":
    main()
