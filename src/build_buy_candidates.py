#!/usr/bin/env python3
"""
Build a ranked "Top Buy Candidates" section and inject it at the top of
output/html/index.html, right after the pf-strip.

Ranks every stock-row that has a buy-flavoured action tag, by:
  - Grade weight (A=100, B 18-19=80, B 15-17=60, C+=40, C=25)
  - Recommendation weight (BUY=50, BUY REDUCED=35, Add/Avg=25, Tracking=15, Watch=10, Spec=5)
  - Upside % from the combined Target cell (+0.5 per pct point above 10%)

Output: a 3-column grid card pinned at the top of the homepage. Top 12 names
shown.

Idempotent — if the section already exists it gets replaced, not duplicated.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "output" / "html" / "index.html"

ROW_RE = re.compile(r"<tr class=\"stock-row\"[^>]*>.*?</tr>", re.DOTALL)
TD_RE = re.compile(r"<td[^>]*>.*?</td>", re.DOTALL)
SECTION_MARKER = "<!-- BUY CANDIDATES BLOCK -->"


def parse_grade(grade_text: str) -> tuple[str, int]:
    """Return (letter, score). e.g. 'B · 17/25' -> ('B', 17)."""
    m = re.search(r"([A-C])[+\-–]?\s*[·\s]*(\d{1,2})", grade_text)
    if not m:
        return ("?", 0)
    return (m.group(1), int(m.group(2)))


def grade_weight(letter: str, score: int) -> int:
    if letter == "A":
        return 100
    if letter == "B":
        if score >= 18:
            return 80
        if score >= 15:
            return 60
        return 50
    if letter == "C":
        if score >= 13:
            return 40
        return 25
    return 10


def classify_action(action_text: str) -> tuple[str, int, str]:
    """Return (kind, weight, label) for ranking + display.
    kind in {"BUY", "ADD", "TRACK", "WATCH", "SPEC", "EXIT", "HOLD", "OTHER"}."""
    t = action_text.lower()
    if "exit" in t or "sold" in t or "avoid" in t:
        return ("EXIT", 0, "Exit")
    if "speculative" in t or "spec buy" in t:
        return ("SPEC", 15, "Speculative")
    if "buy reduced" in t or "buy red" in t:
        return ("BUY", 35, "Buy reduced")
    if t.startswith("buy") or "buy phased" in t or " buy " in t:
        return ("BUY", 50, "Buy")
    if "watch" in t and "buy" in t:
        # "Watch · Buy <₹X" — wait for price
        return ("WATCH", 30, "Watch — buy at price")
    if "add" in t or "avg" in t:
        return ("ADD", 25, "Add to holding")
    if "tracking" in t and ("add" in t or "build" in t):
        return ("TRACK", 20, "Tracking — build trigger")
    if "tracking" in t:
        return ("TRACK", 10, "Tracking")
    if "watch" in t:
        return ("WATCH", 8, "Watch")
    if "hold" in t:
        return ("HOLD", 0, "Hold")
    return ("OTHER", 0, action_text[:30])


def parse_upside(combined_cell_text: str) -> float | None:
    """Parse '+14%' from '₹530 · +14%'."""
    m = re.search(r"([+-]?\d+)%", combined_cell_text)
    if not m:
        return None
    return float(m.group(1))


def parse_target_price(combined_cell_text: str) -> str:
    parts = combined_cell_text.split("·")
    return parts[0].strip() if parts else "—"


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def scan_candidates(html: str) -> list[dict]:
    out = []
    for m in ROW_RE.finditer(html):
        row = m.group(0)
        tds = TD_RE.findall(row)
        if len(tds) != 7:
            continue

        onclick_m = re.search(r"onclick=\"go\('([^']+)'\)\"", row)
        if not onclick_m:
            continue
        target_url = onclick_m.group(1)

        ticker_m = re.search(r'<div class="td-ticker">([^<]+)<', tds[0])
        company_m = re.search(r'<div class="td-company">([^<]*)', tds[0])
        ticker = ticker_m.group(1).strip() if ticker_m else "?"
        company = strip_tags(company_m.group(1)) if company_m else ""
        # Strip val-tag remnants from company line
        company = re.sub(r"\s*(Undervalued|Deep Value|Fairly Valued|Fair|Expensive|Speculative)\s*$", "", company).strip()

        grade_text = strip_tags(tds[1])
        if not grade_text:
            continue
        letter, score = parse_grade(grade_text)
        gw = grade_weight(letter, score)

        action_text = strip_tags(tds[2])
        kind, aw, action_label = classify_action(action_text)
        if kind in ("EXIT", "HOLD", "OTHER"):
            continue

        cmp_text = strip_tags(tds[3])
        combined = strip_tags(tds[5])
        upside = parse_upside(combined)
        target_price = parse_target_price(combined)

        upside_bonus = 0.0
        if upside is not None:
            upside_bonus = max(0, (upside - 10)) * 0.5

        score_total = gw + aw + upside_bonus

        out.append({
            "ticker": ticker,
            "company": company,
            "url": target_url,
            "grade": grade_text,
            "grade_letter": letter,
            "kind": kind,
            "action_label": action_label,
            "action_raw": action_text,
            "cmp": cmp_text,
            "target": target_price,
            "upside": upside,
            "score": score_total,
        })
    out.sort(key=lambda x: (-x["score"], -(x["upside"] or 0), x["ticker"]))
    return out


def render_section(candidates: list[dict], n: int = 15) -> str:
    """Return the HTML block to inject."""
    top = candidates[:n]

    kind_colors = {
        "BUY":   ("#16a34a", "#dcfce7", "BUY"),
        "ADD":   ("#0891b2", "#cffafe", "ADD"),
        "TRACK": ("#7c3aed", "#ede9fe", "TRACK"),
        "WATCH": ("#ca8a04", "#fef3c7", "WATCH"),
        "SPEC":  ("#dc2626", "#fee2e2", "SPEC"),
    }

    rows_html = []
    for i, c in enumerate(top, 1):
        fg, bg, badge = kind_colors.get(c["kind"], ("#666", "#eee", c["kind"]))
        upside_str = f"+{c['upside']:.0f}%" if c["upside"] is not None and c["upside"] > 0 else (
            f"{c['upside']:.0f}%" if c["upside"] is not None else "—"
        )
        upside_color = "#166534" if c["upside"] and c["upside"] >= 10 else ("#991b1b" if c["upside"] and c["upside"] < 0 else "#666")
        grade_letter = c["grade_letter"]
        grade_bg = {"A": "#d4edda", "B": "#fff3cd", "C": "#fee2e2"}.get(grade_letter, "#eee")
        grade_fg = {"A": "#155724", "B": "#856404", "C": "#721c24"}.get(grade_letter, "#666")

        rows_html.append(
            f'<tr style="border-bottom:1px solid #f1f5f9;cursor:pointer" '
            f'onclick="window.location.href=\'{c["url"]}\'" '
            f'onmouseover="this.style.background=\'#f8fafc\'" '
            f'onmouseout="this.style.background=\'transparent\'">'
            f'<td style="padding:9px 8px 9px 14px;color:#94a3b8;font-size:0.78rem;font-weight:600">#{i}</td>'
            f'<td style="padding:9px 8px"><b style="font-size:0.92rem;color:#0f172a">{c["ticker"]}</b>'
            f'<div style="font-size:0.74rem;color:#64748b;margin-top:1px">{c["company"]}</div></td>'
            f'<td style="padding:9px 8px"><span style="background:{grade_bg};color:{grade_fg};font-size:0.7rem;font-weight:700;padding:2px 7px;border-radius:10px">{c["grade"]}</span></td>'
            f'<td style="padding:9px 8px"><span style="background:{bg};color:{fg};font-size:0.68rem;font-weight:700;padding:3px 8px;border-radius:4px">{badge}</span></td>'
            f'<td style="padding:9px 8px;font-size:0.78rem;color:#334155">{c["action_raw"]}</td>'
            f'<td style="padding:9px 8px;font-size:0.78rem;color:#64748b;text-align:right">{c["cmp"]}</td>'
            f'<td style="padding:9px 8px;font-size:0.78rem;text-align:right">{c["target"]}</td>'
            f'<td style="padding:9px 14px 9px 8px;text-align:right;font-weight:700;color:{upside_color};font-size:0.85rem">{upside_str}</td>'
            f'</tr>'
        )

    block = (
        f'\n  {SECTION_MARKER}\n'
        f'  <section style="max-width:1200px;margin:8px auto 18px;padding:0 16px">\n'
        f'    <div style="background:linear-gradient(135deg,#fef3c7 0%,#fef9c3 100%);border:1px solid #fde68a;border-radius:12px;padding:18px 22px 14px;font-family:-apple-system,sans-serif">\n'
        f'      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px">\n'
        f'        <div>\n'
        f'          <h2 style="margin:0;font-size:1.1rem;font-weight:700;color:#78350f">🎯 Top Buy Candidates — pick when you have time</h2>\n'
        f'          <p style="margin:3px 0 0;font-size:0.75rem;color:#92400e">Ranked by grade · recommendation strength · upside vs CMP. Click any row to open the research note.</p>\n'
        f'        </div>\n'
        f'        <span style="font-size:0.7rem;color:#92400e">Top {len(top)} of {len(candidates)} actionable</span>\n'
        f'      </div>\n'
        f'      <div style="background:white;border-radius:8px;overflow:hidden">\n'
        f'      <table style="width:100%;border-collapse:collapse;font-family:-apple-system,sans-serif">\n'
        f'        <thead>\n'
        f'          <tr style="background:#1a1a2e;color:#e2e8f0;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.05em">\n'
        f'            <th style="padding:8px 8px 8px 14px;text-align:left">#</th>\n'
        f'            <th style="padding:8px 8px;text-align:left">Stock</th>\n'
        f'            <th style="padding:8px 8px;text-align:left">Grade</th>\n'
        f'            <th style="padding:8px 8px;text-align:left">Type</th>\n'
        f'            <th style="padding:8px 8px;text-align:left">Action</th>\n'
        f'            <th style="padding:8px 8px;text-align:right">CMP</th>\n'
        f'            <th style="padding:8px 8px;text-align:right">Target</th>\n'
        f'            <th style="padding:8px 14px 8px 8px;text-align:right">Upside</th>\n'
        f'          </tr>\n'
        f'        </thead>\n'
        f'        <tbody>\n'
        + "\n          ".join(rows_html) +
        f'\n        </tbody>\n'
        f'      </table>\n'
        f'      </div>\n'
        f'    </div>\n'
        f'  </section>\n'
    )
    return block


def inject(html: str, block: str) -> str:
    """Insert (or replace) the buy-candidates block. Anchor: right after the pf-strip closing tag."""
    # Replace existing block if present
    existing_re = re.compile(
        rf"\n  {re.escape(SECTION_MARKER)}.*?</section>\n",
        re.DOTALL,
    )
    if existing_re.search(html):
        return existing_re.sub(block, html)
    # Otherwise insert after the pf-strip's parent header </div>... we'll anchor after </header>
    if "</header>" in html:
        return html.replace("</header>", "</header>\n" + block, 1)
    return html


def main():
    html = HTML_PATH.read_text()
    candidates = scan_candidates(html)
    print(f"Total actionable candidates: {len(candidates)}")
    if not candidates:
        print("No candidates found — nothing to inject.")
        return

    print("\nTop 12 by composite score:")
    for c in candidates[:12]:
        up = f"{c['upside']:+.0f}%" if c['upside'] is not None else "—"
        print(f"  {c['ticker']:<14} {c['grade']:<12} {c['kind']:<6} {c['action_raw']:<35} CMP={c['cmp']:<10} Tgt={c['target']:<10} Up={up:<6} score={c['score']:.1f}")

    block = render_section(candidates, n=12)
    new_html = inject(html, block)
    HTML_PATH.write_text(new_html)
    print(f"\n✓ Injected/refreshed buy-candidates block in {HTML_PATH}")


if __name__ == "__main__":
    main()
