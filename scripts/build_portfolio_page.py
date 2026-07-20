#!/usr/bin/env python3
"""Regenerate output/html/portfolio.html from data/portfolio.csv + fresh closes.

Holdings (qty, avg buy) come from data/portfolio.csv — the documented source of
truth for what is held. CMP is the official bhavcopy close fetched at build
time (same source as the daily portfolio ping), NOT a stale broker export. Each
holding's action label is read from its research note via the same parser the
research index uses, so the two pages never disagree.

Two dates are stamped separately and honestly: holdings are only as current as
portfolio.csv; prices are the latest exchange close. If you have traded since
the CSV was last updated, refresh it (that is the one step needing a broker
pull) — the prices here are always fresh regardless.

Usage:
  venv/bin/python3 scripts/build_portfolio_page.py            # write file
  venv/bin/python3 scripts/build_portfolio_page.py --stdout   # print, don't write
"""

import csv
import html as html_mod
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from daily_portfolio_telegram import build_price_map, last_trading_bhav
from build_site_index import parse_note, base_symbol

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "data" / "portfolio.csv"
RESEARCH = REPO / "research"
OUT = REPO / "output" / "html" / "portfolio.html"

# research verdict bucket -> short portfolio action label + colour
ACTION = {
    "buy": ("Buy", "#166534"),
    "buyat": ("Buy at ₹", "#155e75"),
    "hold": ("Hold", "#854d0e"),
    "watch": ("Watch", "#3730a3"),
    "owned": ("Hold", "#854d0e"),
    "trim": ("Trim", "#9a3412"),
    "exit": ("Exit", "#991b1b"),
    "avoid": ("Avoid", "#991b1b"),
    "note": ("—", "#94a3b8"),
    "unclassified": ("—", "#94a3b8"),
}


def holdings() -> list[dict]:
    trade_date, nse, bse = last_trading_bhav()
    prices = build_price_map(nse, bse)
    rows = []
    with open(CSV_PATH) as f:
        for r in csv.DictReader(f):
            sym = r["symbol"].strip()
            base = base_symbol(sym)
            qty = float(r["quantity"])
            avg = float(r["avg_buy_price"])
            px = prices.get(sym) or prices.get(base + ".NS") or prices.get(base + ".BO")
            cmp_ = round(px[0], 2) if px else None
            note = RESEARCH / f"{base}.md"
            if note.exists():
                bucket = parse_note(note)["bucket"]
            else:
                bucket = None
            action, acolor = ACTION.get(bucket, ("—", "#94a3b8"))
            invested = qty * avg
            current = qty * cmp_ if cmp_ is not None else None
            rows.append({
                "symbol": base, "qty": qty, "avg": avg, "cmp": cmp_,
                "invested": invested, "current": current,
                "pnl": (current - invested) if current is not None else None,
                "action": action, "acolor": acolor,
                "has_note": note.exists(),
            })
    return rows, trade_date


def csv_stamp() -> str:
    ts = datetime.fromtimestamp(CSV_PATH.stat().st_mtime)
    return ts.strftime("%d %b %Y")


def fmt_k(v: float) -> str:
    return f"₹{v/1000:,.1f}K"


def build() -> str:
    rows, trade_date = holdings()
    priced = [h for h in rows if h["current"] is not None]
    invested = sum(h["invested"] for h in priced)
    current = sum(h["current"] for h in priced)
    pnl = current - invested
    pnl_pct = (pnl / invested * 100) if invested else 0.0
    unpriced = [h["symbol"] for h in rows if h["current"] is None]

    pl_col = "#16a34a" if pnl >= 0 else "#dc2626"
    rows_sorted = sorted(rows, key=lambda h: -(h["current"] or -1))

    tr = []
    for h in rows_sorted:
        wt = (h["current"] / current * 100) if (h["current"] and current) else 0
        cmp_s = f"₹{h['cmp']:,.2f}" if h["cmp"] is not None else "—"
        cur_s = fmt_k(h["current"]) if h["current"] is not None else "—"
        pnl_s = (("+" if h["pnl"] >= 0 else "") + fmt_k(h["pnl"])) if h["pnl"] is not None else "—"
        pnlp = (h["pnl"] / h["invested"] * 100) if (h["pnl"] is not None and h["invested"]) else None
        pnlp_s = f"{pnlp:+.1f}%" if pnlp is not None else "—"
        pcol = "#16a34a" if (h["pnl"] or 0) >= 0 else "#dc2626"
        name = html_mod.escape(h["symbol"])
        tr.append(f"""      <tr onclick="location.href='{name}.html'">
        <td data-s="{name}"><b>{name}</b></td>
        <td class="num" data-label="Qty" data-s="{h['qty']}">{h['qty']:,.0f}</td>
        <td class="num" data-label="Avg" data-s="{h['avg']}">₹{h['avg']:,.2f}</td>
        <td class="num" data-label="CMP" data-s="{h['cmp'] or -1}" style="font-weight:600">{cmp_s}</td>
        <td class="num" data-label="Invested" data-s="{h['invested']}">{fmt_k(h['invested'])}</td>
        <td class="num" data-label="Current" data-s="{h['current'] or -1}" style="font-weight:600">{cur_s}</td>
        <td class="num" data-label="P&amp;L" data-s="{h['pnl'] if h['pnl'] is not None else -1e12}" style="font-weight:600;color:{pcol}">{pnl_s}</td>
        <td class="num" data-label="P&amp;L %" data-s="{pnlp if pnlp is not None else -1e9}" style="font-weight:600;color:{pcol}">{pnlp_s}</td>
        <td class="num" data-label="Weight" data-s="{wt}">{wt:.1f}%</td>
        <td data-label="Action" data-s="{h['action']}" style="font-weight:700;color:{h['acolor']}">{h['action']}</td>
      </tr>""")
    rows_html = "\n".join(tr)

    unpriced_note = ""
    if unpriced:
        unpriced_note = ("<div class='warn'>No live close for: " + ", ".join(unpriced)
                         + " — excluded from totals (US names / unlisted / SME not in the bhavcopy feed).</div>")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>Portfolio · Stock Research</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #f8fafc; color: #1a1a2e; }}
  header {{ background: linear-gradient(135deg, #1a1a2e 0%, #2d3055 100%); color: #fff; padding: 18px 22px; }}
  .top {{ display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 12px; max-width: 1320px; margin: 0 auto; }}
  header h1 {{ font-size: 1.4rem; font-weight: 700; }}
  header p {{ color: #94a3b8; font-size: 0.82rem; margin-top: 4px; }}
  .nav a {{ color: #93c5fd; text-decoration: none; font-size: 0.85rem; margin-left: 8px; padding: 6px 12px; border: 1px solid rgba(147,197,253,0.3); border-radius: 6px; }}
  .nav a:hover {{ background: rgba(147,197,253,0.1); }}
  .container {{ max-width: 1320px; margin: 22px auto; padding: 0 22px; }}
  .snapshot {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px 24px; margin-bottom: 18px; }}
  .snap-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 20px; }}
  .stat-label {{ color: #64748b; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px; }}
  .stat-value {{ font-size: 1.2rem; font-weight: 700; }}
  .warn {{ background: #fef3c7; border-left: 4px solid #f59e0b; color: #78350f; padding: 9px 14px; font-size: 0.8rem; border-radius: 6px; margin-bottom: 16px; }}
  table {{ width: 100%; background: #fff; border-collapse: collapse; border-radius: 10px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}
  th {{ background: #f1f5f9; color: #475569; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; padding: 12px 10px; border-bottom: 2px solid #e2e8f0; text-align: left; cursor: pointer; user-select: none; white-space: nowrap; }}
  th:hover {{ background: #e2e8f0; }}
  th.num, td.num {{ text-align: right; }}
  td {{ padding: 11px 10px; font-size: 0.86rem; border-bottom: 1px solid #f1f5f9; font-variant-numeric: tabular-nums; }}
  tbody tr {{ cursor: pointer; }}
  tbody tr:hover {{ background: #f8fafc; }}
  .table-wrap {{ overflow-x: auto; }}
  .footer {{ color: #94a3b8; font-size: 0.74rem; margin: 22px 0; line-height: 1.6; }}
  @media (max-width: 640px) {{
    header {{ padding: 14px 16px; }}
    header h1 {{ font-size: 1.2rem; }}
    .container {{ margin: 16px auto; padding: 0 12px; }}
    .snapshot {{ padding: 16px; }}
    .snap-grid {{ grid-template-columns: 1fr 1fr; gap: 14px; }}
    .table-wrap {{ overflow: visible; }}
    table {{ box-shadow: none; border-radius: 0; }}
    thead {{ display: none; }}
    table, tbody, tr, td {{ display: block; width: 100%; }}
    tbody tr {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
                margin-bottom: 10px; padding: 12px 14px; }}
    tbody tr:hover {{ background: #fff; }}
    td {{ display: flex; justify-content: space-between; align-items: baseline; gap: 12px;
          padding: 5px 0; border: none; text-align: right; }}
    td::before {{ content: attr(data-label); font-weight: 600; color: #64748b; font-size: 0.68rem;
                 text-transform: uppercase; letter-spacing: 0.4px; text-align: left; white-space: nowrap; }}
    td:first-child {{ display: flex; justify-content: space-between; align-items: baseline;
                     padding-bottom: 8px; margin-bottom: 6px; border-bottom: 1px solid #f1f5f9; font-size: 1rem; }}
    td:first-child::before {{ content: none; }}
  }}
</style>
</head>
<body>
<header>
  <div class="top">
    <div>
      <h1>📊 Portfolio</h1>
      <p>{len(rows)} holdings · holdings as of {csv_stamp()} (portfolio.csv) · prices {trade_date} (bhavcopy close)</p>
    </div>
    <div class="nav">
      <a href="index.html">🔍 Research</a>
      <a href="FOCUS.html">🎯 Focus</a>
      <a href="INVESTING_PLAYBOOK.html">📖 Playbook</a>
      <a href="DECISION_LOG.html">📋 Decisions</a>
    </div>
  </div>
</header>

<div class="container">
  <div class="snapshot">
    <div class="snap-grid">
      <div><div class="stat-label">Invested</div><div class="stat-value">₹{invested/100000:,.2f}L</div></div>
      <div><div class="stat-label">Current</div><div class="stat-value">₹{current/100000:,.2f}L</div></div>
      <div><div class="stat-label">P&amp;L</div><div class="stat-value" style="color:{pl_col}">{'+' if pnl>=0 else ''}₹{pnl/1000:,.1f}K</div></div>
      <div><div class="stat-label">Return</div><div class="stat-value" style="color:{pl_col}">{pnl_pct:+.2f}%</div></div>
    </div>
  </div>
  {unpriced_note}
  <div class="table-wrap">
  <table id="pf">
    <thead><tr>
      <th data-k="0">Symbol</th>
      <th class="num" data-k="1">Qty</th>
      <th class="num" data-k="2">Avg</th>
      <th class="num" data-k="3">CMP</th>
      <th class="num" data-k="4">Invested</th>
      <th class="num" data-k="5">Current</th>
      <th class="num" data-k="6">P&amp;L</th>
      <th class="num" data-k="7">P&amp;L %</th>
      <th class="num" data-k="8">Weight</th>
      <th data-k="9">Action</th>
    </tr></thead>
    <tbody>
{rows_html}
    </tbody>
  </table>
  </div>
  <div class="footer">
    Prices are the official exchange bhavcopy close ({trade_date}), not live. Holdings
    (qty, avg) come from data/portfolio.csv, last updated {csv_stamp()} — refresh it after any
    trade for the P&amp;L to be exact. Action is read from each stock's research note.
    Auto-generated by scripts/build_portfolio_page.py.
  </div>
</div>

<script>
const tbody = document.querySelector('#pf tbody');
let sortCol = null, asc = true;
document.querySelectorAll('#pf th').forEach(th => th.addEventListener('click', () => {{
  const k = +th.dataset.k;
  if (sortCol === k) asc = !asc; else {{ sortCol = k; asc = true; }}
  const rows = [...tbody.querySelectorAll('tr')];
  rows.sort((a, b) => {{
    let x = a.children[k].dataset.s, y = b.children[k].dataset.s;
    const nx = parseFloat(x), ny = parseFloat(y);
    if (!isNaN(nx) && !isNaN(ny)) {{ x = nx; y = ny; }}
    return (x < y ? -1 : x > y ? 1 : 0) * (asc ? 1 : -1);
  }});
  rows.forEach(r => tbody.appendChild(r));
}}));
</script>
</body>
</html>
"""


def main() -> int:
    page = build()
    if "--stdout" in sys.argv:
        sys.stdout.write(page)
    else:
        OUT.write_text(page, encoding="utf-8")
        print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
