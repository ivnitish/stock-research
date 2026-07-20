#!/usr/bin/env python3
"""Regenerate output/html/index.html from research/*.md — the research table only.

Kills the hand-maintained stock list (was ~1,950 lines, went stale). Every
research note gets a row automatically; a note can never silently vanish
(unparseable ones bucket as "Unclassified"). CMP is fetched FRESH from the
official bhavcopy at build time — never the stale price baked into the note's
header — so "auto-generated" doesn't quietly mean "auto-stale". Names without a
bhav match show a blank CMP rather than a guess (no fabricated data).

The satellite pages (Focus, Portfolio, Playbook, Library, Decisions) and the
site's visual design are preserved; only the main table body is generated.

Usage:
  venv/bin/python3 scripts/build_site_index.py           # write index.html
  venv/bin/python3 scripts/build_site_index.py --stdout  # print, don't write
"""

import csv
import glob
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from daily_portfolio_telegram import build_price_map, last_trading_bhav

REPO = Path(__file__).resolve().parent.parent
RESEARCH = REPO / "research"
OUT = REPO / "output" / "html" / "index.html"


def base_symbol(sym: str) -> str:
    return re.sub(r"\.(NS|BO)$", "", sym.strip())


def price_overrides() -> dict[str, str]:
    """research symbol -> bhav symbol (SYMBOL.NS/.BO), for names whose file
    stem isn't the ticker (BSE-SME renames, portfolio suffixes)."""
    ov: dict[str, str] = {}
    pf = REPO / "data" / "portfolio.csv"
    if pf.exists():
        with open(pf) as f:
            for row in csv.DictReader(f):
                ov[base_symbol(row["symbol"])] = row["symbol"].strip()
    ba = REPO / "data" / "buyat_alerts.csv"
    if ba.exists():
        with open(ba) as f:
            for row in csv.DictReader(f):
                ov[row["symbol"].strip()] = row["bhav_symbol"].strip()
    return ov


def owned_symbols() -> set[str]:
    pf = REPO / "data" / "portfolio.csv"
    if not pf.exists():
        return set()
    with open(pf) as f:
        return {base_symbol(r["symbol"]) for r in csv.DictReader(f)}


def classify(verdict: str) -> tuple[str, str]:
    """(bucket key, display label) from the raw verdict/status string.

    Explicit-state words (OWNED / WATCHLIST) are tested before action words so a
    stray "buy" inside a long status line can't mislabel a holding or a watch.
    OWNED headers are known-stale (portfolio positions are really HOLD/ADD/TRIM
    decisions) — labelled neutrally as "Holding"; read the note for the action.
    """
    v = verdict.upper()
    if not v.strip():
        return "note", "Note / analysis"
    if "AVOID" in v:
        return "avoid", "Avoid"
    if "OWNED" in v:
        return "owned", "Holding"
    if "WATCHLIST" in v or "PRE-IPO" in v or "UNLISTED" in v or "PRE IPO" in v:
        return "watch", "Watchlist"
    if "EXIT" in v:
        return "exit", "Exit"
    if "TRIM" in v or "REDUCE" in v or "BOOK PROFIT" in v:
        return "trim", "Trim"
    if "BUY AT" in v or "BUY BELOW" in v or "BUY @" in v or "STANDING PRICE ALERT" in v:
        return "buyat", "Buy at price"
    if "APPLY" in v:
        return "buy", "Apply / Buy"
    if "BUY" in v or "ACCUMULATE" in v or "INITIATE" in v or "STARTER" in v:
        return "buy", "Buy"
    if "ADD" in v:
        return "buy", "Add"
    if "HOLD" in v:
        return "hold", "Hold"
    if "TRACKING" in v or "LISTED" in v or "WATCH" in v:
        return "watch", "Watchlist"
    return "unclassified", "Unclassified"


HEADING = re.compile(r"^#\s+(.+)$", re.M)
VERDICT = re.compile(r"\*\*\s*(?:Verdict|Recommendation)\s*:\s*(.+?)\*\*", re.I | re.S)
STATUS = re.compile(r"\*\*\s*Status\s*:\s*\*\*\s*(.+)")
GRADE = re.compile(r"Grade\s*([A-D][+\-]?)", re.I)
SCORE = re.compile(r"(\b\d{1,2})\s*/\s*25\b")
DATE = re.compile(
    r"\*\*\s*(?:Date|Last\s*Updated)\s*:\s*\*?\*?\s*(\d{4}-\d{2}-\d{2}|\d{1,2}\s+\w+\s+\d{4})",
    re.I,
)


def parse_note(path: Path) -> dict:
    sym = path.stem
    text = path.read_text(encoding="utf-8", errors="replace")
    head = text[:2000]  # metadata always sits at the top

    m = HEADING.search(head)
    title = m.group(1).strip() if m else sym
    # "SYMBOL — Company Name" -> "Company Name"; else keep the H1 text.
    name = re.sub(rf"^{re.escape(sym)}\s*[—\-:]\s*", "", title).strip()
    name = re.sub(r"\s+—\s+.*(Note|Valuation|IPO).*$", "", name).strip() or title

    vm = VERDICT.search(head) or STATUS.search(head)
    verdict = ""
    if vm:
        verdict = re.sub(r"\s+", " ", vm.group(1)).strip(" *|—-")
        verdict = verdict.split("|")[0].strip()  # drop trailing Date/CMP cells
    bucket, label = classify(verdict) if verdict else ("unclassified", "Unclassified")

    gm = GRADE.search(head)
    sm = SCORE.search(head)
    dm = DATE.search(head)
    # A stock note without a header verdict (thesis-in-prose) stays visible as
    # "Unclassified" — never dropped. A pure doc (no verdict, no price, no grade)
    # is a note/analysis, not a stock, and goes to the Notes bucket.
    stock_ish = bool(gm or sm or re.search(r"\*\*\s*(CMP|P/E|PE|Mkt\s*Cap|Market\s*Cap|MCap)\s*:", head, re.I))
    if not verdict and stock_ish:
        bucket, label = "unclassified", "Unclassified"
    # Exchange tickers never contain "_"; underscore stems are multi-stock
    # analyses / themes / screens (MACRO_NOTES, GROWW_vs_ICICIAMC, ...) — route
    # them to Notes so they don't sit in the stock table with a blank verdict.
    if "_" in sym:
        bucket, label = "note", "Note / analysis"
    return {
        "symbol": sym,
        "name": html.unescape(name),
        "verdict": html.unescape(verdict),
        "bucket": bucket,
        "label": label,
        "grade": gm.group(1).upper() if gm else "",
        "score": int(sm.group(1)) if sm else None,
        "date": dm.group(1) if dm else "",
    }


def build_rows() -> tuple[list[dict], str, dict]:
    overrides = price_overrides()
    owned = owned_symbols()
    try:
        trade_date, nse, bse = last_trading_bhav()
        pm = build_price_map(nse, bse)
        cmp_note = f"CMP from official bhavcopy close, {trade_date}"
    except Exception as e:  # graceful — grade/verdict still render
        pm, cmp_note = {}, f"CMP unavailable (bhav fetch failed: {e})"

    rows = []
    for f in sorted(glob.glob(str(RESEARCH / "*.md"))):
        r = parse_note(Path(f))
        sym = r["symbol"]
        key = overrides.get(sym)
        if key not in pm:
            key = sym + ".NS" if sym + ".NS" in pm else (sym + ".BO" if sym + ".BO" in pm else None)
        r["cmp"] = round(pm[key][0], 1) if key in pm else None
        r["owned"] = base_symbol(sym) in owned
        rows.append(r)

    order = {"buy": 0, "buyat": 1, "hold": 2, "watch": 3, "owned": 4,
             "trim": 5, "exit": 6, "avoid": 7, "note": 8, "unclassified": 9}
    rows.sort(key=lambda r: (order.get(r["bucket"], 9), -(r["score"] or 0), r["symbol"]))
    stats = {
        "total": len(rows),
        "priced": sum(1 for r in rows if r["cmp"] is not None),
        "graded": sum(1 for r in rows if r["grade"]),
        "unclassified": sum(1 for r in rows if r["bucket"] == "unclassified"),
    }
    return rows, cmp_note, stats


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Stock Research — Nitish</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f7f8fa; color: #1a1a1a; }}
  header {{ background: #1a1a2e; color: white; padding: 18px 20px 14px; }}
  .header-top {{ display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 10px; }}
  header h1 {{ font-size: 1.3rem; font-weight: 700; letter-spacing: -0.5px; }}
  header .sub {{ color: #9090b0; font-size: 0.75rem; margin-top: 3px; }}
  .nav {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 12px; }}
  .nav a {{ font-size: 0.72rem; padding: 5px 11px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.22);
           color: #c4c4dd; text-decoration: none; transition: all .15s; }}
  .nav a:hover {{ background: rgba(255,255,255,0.12); color: #fff; }}
  .controls {{ max-width: 1200px; margin: 0 auto; padding: 16px 12px 6px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }}
  #search {{ flex: 1 1 240px; min-width: 200px; padding: 8px 12px; border: 1px solid #d5d8e0; border-radius: 8px; font-size: 0.85rem; }}
  .chips {{ display: flex; gap: 6px; flex-wrap: wrap; }}
  .chip {{ font-size: 0.72rem; font-weight: 600; padding: 5px 12px; border-radius: 20px; border: 1px solid #d5d8e0;
          background: #fff; color: #555; cursor: pointer; transition: all .15s; }}
  .chip:hover {{ border-color: #1a1a2e; }}
  .chip.active {{ background: #1a1a2e; color: #fff; border-color: #1a1a2e; }}
  .toggle {{ font-size: 0.72rem; font-weight: 600; color: #555; display: flex; align-items: center; gap: 5px; cursor: pointer; user-select: none; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 8px 12px 40px; }}
  .table-wrap {{ background: #fff; border-radius: 12px; border: 1px solid #e8e8e8; overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; min-width: 720px; }}
  thead tr {{ background: #f8f9fb; border-bottom: 2px solid #e8e8e8; }}
  th {{ padding: 10px 12px; text-align: left; font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
       letter-spacing: 0.6px; color: #667; white-space: nowrap; cursor: pointer; position: sticky; top: 0; background: #f8f9fb; }}
  th.num {{ text-align: right; }}
  th .arrow {{ color: #bbb; font-size: 0.7rem; }}
  tbody tr {{ border-bottom: 1px solid #f0f0f4; cursor: pointer; transition: background .1s; }}
  tbody tr:hover {{ background: #f6f8ff; }}
  td {{ padding: 9px 12px; font-size: 0.82rem; vertical-align: middle; }}
  td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  .sym {{ font-weight: 700; color: #1a1a2e; }}
  .nm {{ color: #667; font-size: 0.74rem; }}
  .owned {{ display: inline-block; margin-left: 6px; font-size: 0.6rem; font-weight: 700; color: #166534;
           background: #dcfce7; border-radius: 4px; padding: 1px 5px; vertical-align: middle; }}
  .verdict {{ font-size: 0.78rem; }}
  .badge {{ display: inline-block; font-size: 0.62rem; font-weight: 700; border-radius: 5px; padding: 2px 7px; white-space: nowrap; }}
  .b-buy {{ background: #dcfce7; color: #166534; }}
  .b-buyat {{ background: #cffafe; color: #155e75; }}
  .b-hold {{ background: #fef9c3; color: #854d0e; }}
  .b-watch {{ background: #e0e7ff; color: #3730a3; }}
  .b-owned {{ background: #ede9fe; color: #5b21b6; }}
  .b-trim {{ background: #ffedd5; color: #9a3412; }}
  .b-exit {{ background: #fee2e2; color: #991b1b; }}
  .b-avoid {{ background: #fee2e2; color: #991b1b; }}
  .b-note {{ background: #f1f5f9; color: #64748b; }}
  .b-unclassified {{ background: #f1f5f9; color: #64748b; }}
  .grade {{ font-weight: 700; font-size: 0.78rem; }}
  .empty {{ padding: 40px; text-align: center; color: #99a; font-size: 0.85rem; }}
  footer {{ max-width: 1200px; margin: 0 auto; padding: 0 12px 40px; color: #99a; font-size: 0.72rem; line-height: 1.5; }}
</style>
</head>
<body>
<header>
  <div class="header-top">
    <div>
      <h1>Stock Research</h1>
      <div class="sub">{count} research notes · {cmp_note} · built {built}</div>
    </div>
  </div>
  <div class="nav">
    <a href="FOCUS.html">🎯 Focus</a>
    <a href="portfolio.html">📊 Portfolio</a>
    <a href="INVESTING_PLAYBOOK.html">📖 Playbook</a>
    <a href="library.html">📚 Library</a>
    <a href="DECISION_LOG.html">📋 Decisions</a>
  </div>
</header>

<div class="controls">
  <input id="search" type="search" placeholder="Search symbol, company, or verdict…" autocomplete="off">
  <div class="chips" id="chips">
    <button class="chip active" data-b="all">All</button>
    <button class="chip" data-b="buy">Buy</button>
    <button class="chip" data-b="buyat">Buy at price</button>
    <button class="chip" data-b="hold">Hold</button>
    <button class="chip" data-b="watch">Watchlist</button>
    <button class="chip" data-b="owned">Holdings</button>
    <button class="chip" data-b="trim">Trim/Exit</button>
    <button class="chip" data-b="avoid">Avoid</button>
    <button class="chip" data-b="note">Notes</button>
  </div>
  <label class="toggle"><input type="checkbox" id="ownedOnly"> Owned only</label>
</div>

<div class="container">
  <div class="table-wrap">
    <table>
      <thead><tr>
        <th data-k="symbol">Stock <span class="arrow">↕</span></th>
        <th data-k="grade">Grade <span class="arrow">↕</span></th>
        <th data-k="label">Verdict <span class="arrow">↕</span></th>
        <th class="num" data-k="cmp">CMP ₹ <span class="arrow">↕</span></th>
        <th class="num" data-k="score">Score <span class="arrow">↕</span></th>
        <th data-k="date">Updated <span class="arrow">↕</span></th>
      </tr></thead>
      <tbody id="tb"></tbody>
    </table>
    <div class="empty" id="empty" style="display:none">No notes match.</div>
  </div>
</div>

<footer>
  Prices are the official exchange bhavcopy close, not live. CMP is blank where a
  note has no matched exchange ticker (US names, some BSE-SME scrips). Verdict
  buckets are auto-classified from each note's header — always read the note for
  the exact recommendation and price levels. Auto-generated by
  scripts/build_site_index.py.
</footer>

<script type="application/json" id="data">{data}</script>
<script>
const ROWS = JSON.parse(document.getElementById('data').textContent);
let bucket = 'all', ownedOnly = false, sortK = null, sortAsc = true;
const tb = document.getElementById('tb'), empty = document.getElementById('empty');
const gradeRank = {{ 'A+':9,'A':8,'A-':7,'B+':6,'B':5,'B-':4,'C+':3,'C':2,'C-':1,'D':0 }};

function render() {{
  const q = document.getElementById('search').value.trim().toLowerCase();
  let rows = ROWS.filter(r => {{
    if (bucket !== 'all' && !(bucket === 'trim' ? (r.bucket==='trim'||r.bucket==='exit') : r.bucket === bucket)) return false;
    if (ownedOnly && !r.owned) return false;
    if (q && !((r.symbol+' '+r.name+' '+r.verdict).toLowerCase().includes(q))) return false;
    return true;
  }});
  if (sortK) {{
    rows.sort((a,b) => {{
      let x = a[sortK], y = b[sortK];
      if (sortK === 'grade') {{ x = gradeRank[x] ?? -1; y = gradeRank[y] ?? -1; }}
      if (sortK === 'cmp' || sortK === 'score') {{ x = x ?? -1; y = y ?? -1; }}
      if (x < y) return sortAsc ? -1 : 1;
      if (x > y) return sortAsc ? 1 : -1;
      return 0;
    }});
  }}
  tb.innerHTML = rows.map(r => `
    <tr onclick="location.href='${{r.symbol}}.html'">
      <td><span class="sym">${{r.symbol}}</span>${{r.owned?'<span class="owned">OWNED</span>':''}}<div class="nm">${{r.name}}</div></td>
      <td><span class="grade">${{r.grade||'—'}}</span></td>
      <td><span class="badge b-${{r.bucket}}">${{r.label}}</span>${{r.verdict?`<div class="verdict">${{r.verdict}}</div>`:''}}</td>
      <td class="num">${{r.cmp!=null?r.cmp.toLocaleString('en-IN'):'—'}}</td>
      <td class="num">${{r.score!=null?r.score+'/25':'—'}}</td>
      <td>${{r.date||'—'}}</td>
    </tr>`).join('');
  empty.style.display = rows.length ? 'none' : 'block';
}}

document.getElementById('search').addEventListener('input', render);
document.getElementById('ownedOnly').addEventListener('change', e => {{ ownedOnly = e.target.checked; render(); }});
document.querySelectorAll('.chip').forEach(c => c.addEventListener('click', () => {{
  document.querySelectorAll('.chip').forEach(x => x.classList.remove('active'));
  c.classList.add('active'); bucket = c.dataset.b; render();
}}));
document.querySelectorAll('th').forEach(th => th.addEventListener('click', () => {{
  const k = th.dataset.k;
  if (sortK === k) sortAsc = !sortAsc; else {{ sortK = k; sortAsc = true; }}
  render();
}}));
render();
</script>
</body>
</html>
"""


def main() -> int:
    rows, cmp_note, stats = build_rows()
    data = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    page = PAGE.format(
        count=stats["total"],
        cmp_note=cmp_note,
        built=date.today().isoformat(),
        data=data,
    )
    if "--stdout" in sys.argv:
        sys.stdout.write(page)
    else:
        OUT.write_text(page, encoding="utf-8")
        print(f"wrote {OUT}")
    print(f"stats: {stats['total']} notes | {stats['priced']} priced | "
          f"{stats['graded']} graded | {stats['unclassified']} unclassified", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
