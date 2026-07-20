"""Single-command portfolio refresh.

Single source of truth for portfolio state:
  - data/portfolio.csv       → quantity, avg buy price  (manual edits)
  - latest broker xlsx       → CMP (closing price)
  - output/html/index.html   → per-row Target + Action  (from research)
                                    ↓
  output/html/portfolio.html (canonical live view, sortable)
  output/html/index.html      snapshot block at top

Note on the per-stock "Upside %" column:
  Upside % = (target / CMP − 1) × 100. No horizon math — different research
  files use different horizons (1yr fair value vs 3-5yr multi-bagger base
  case), so a single "Expected 3yr CAGR" was misleading. Upside % is just
  honest distance to whatever target the research file currently lists.

Snapshot's "Avg upside (active holds)" is current-weighted across holdings
whose Action is BUY / ADD / HOLD only — EXIT / WATCH / TRIM positions are
excluded because their target is an exit trigger, not an upside target.

Usage:
    python3 src/refresh_portfolio.py            # dry run, print snapshot
    python3 src/refresh_portfolio.py --write    # apply changes
"""

import argparse
import csv
import re
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "portfolio.csv"
HTML_PATH = ROOT / "output" / "html" / "index.html"
PORTFOLIO_HTML_PATH = ROOT / "output" / "html" / "portfolio.html"
BROKER_DIR = ROOT / "data" / "broker-exports"
RESEARCH_DIR = ROOT / "research"

ISIN_TO_SYMBOL: dict[str, str] = {
    "INE242C01024": "ANANTRAJ",
    "INE025R01021": "ARTEMISMED",
    "INE0LEZ01016": "ATHERENERG",
    "INE213C01025": "BANCOINDIA",
    "INE257A01026": "BHEL",
    "INE506A01018": "DREDGECORP",
    "INE0MLS01022": "EPACKPEB",
    "INE758T01015": "ETERNAL",
    "INE382Z01011": "GRSE",
    "INE346A01027": "ICICIAMC",
    "INE202H01019": "KERNEX",
    "INE317F01035": "NESCO",
    "INE619B01017": "NEWGEN",
    "INE882B01037": "NWIL",
    "INE082C01024": "PATELSAI",
    "INE301A01014": "RAYMOND",
    "INE667G01023": "SAKSOFT",
    "INE024F01011": "SHILCTECH",
    "INE980Y01015": "SOUTHWEST",
    "INE1VXE01018": "STLNETWORK",
    "INE00H001014": "SWIGGY",
    "INE628D01014": "THRIVE",
    "INE251B01027": "ZENTEC",
}

# action-tag class → canonical action label. Active actions (counted in
# "avg upside on active holds") are BUY / ADD / HOLD; the rest are excluded.
ACTION_MAP = {
    "act-buy": "BUY",
    "act-add": "ADD",
    "act-hold": "HOLD",
    "act-watch": "WATCH",
    "act-exit": "EXIT",
    "act-ref": "REF",
}
ACTIVE_ACTIONS = {"BUY", "ADD", "HOLD"}

# Color per action label, for portfolio.html
ACTION_COLORS = {
    "BUY":   "#16a34a",
    "ADD":   "#0891b2",
    "HOLD":  "#6b7280",
    "WATCH": "#a16207",
    "EXIT":  "#dc2626",
    "REF":   "#94a3b8",
    "—":     "#94a3b8",
}

ROW_RE = re.compile(r'<tr class="stock-row"([^>]*?)>(.*?)</tr>', re.DOTALL)
TD_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL)
SYMBOL_RE = re.compile(r"onclick=\"go\('([A-Z0-9]+)\.html'\)\"")
ACTION_TAG_RE = re.compile(r'<span class="action-tag (act-[a-z]+)"[^>]*>([^<]*)</span>')
PRICE_RE = re.compile(r"₹\s*([\d,]+(?:\.\d+)?)")
SNAPSHOT_RE = re.compile(
    r"<!-- BEGIN_PORTFOLIO_SNAPSHOT -->.*?<!-- END_PORTFOLIO_SNAPSHOT -->",
    re.DOTALL,
)
STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+)$", re.MULTILINE)


def parse_price(text: str) -> float | None:
    m = PRICE_RE.search(text)
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except ValueError:
        return None


def find_latest_broker_export() -> Path:
    candidates = list(BROKER_DIR.rglob("*Holdings*.xlsx"))
    if not candidates:
        candidates = list(BROKER_DIR.rglob("*.xlsx"))
    if not candidates:
        raise FileNotFoundError(f"No broker xlsx found under {BROKER_DIR}")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def parse_broker_export(path: Path) -> tuple[dict[str, dict], str, dict]:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))

    snapshot_date = "unknown"
    totals = {"invested": 0.0, "current": 0.0, "pnl": 0.0}
    for row in rows:
        if not row:
            continue
        first = row[0]
        if isinstance(first, str):
            if first.startswith("Holdings statement for stocks as on"):
                snapshot_date = first.split("as on")[-1].strip()
            elif first == "Invested Value" and row[1] is not None:
                totals["invested"] = float(row[1])
            elif first == "Closing Value" and row[1] is not None:
                totals["current"] = float(row[1])
            elif first == "Unrealised P&L" and row[1] is not None:
                totals["pnl"] = float(row[1])

    header_idx = next((i for i, r in enumerate(rows) if r and r[0] == "Stock Name"), None)
    if header_idx is None:
        raise ValueError(f"No header row found in {path.name}")

    holdings: dict[str, dict] = {}
    unmapped: list[str] = []
    for row in rows[header_idx + 1:]:
        if not row or not row[1]:
            continue
        name, isin, qty, avg, invested, close, current, pnl = row[:8]
        sym = ISIN_TO_SYMBOL.get(str(isin).strip())
        if not sym:
            unmapped.append(f"{isin} ({name})")
            continue
        holdings[sym] = {
            "name": name,
            "qty": float(qty),
            "avg": float(avg),
            "close": float(close),
            "invested": float(invested),
            "current": float(current),
            "pnl": float(pnl),
        }
    if unmapped:
        print(f"⚠ Unmapped ISINs in broker export ({len(unmapped)}):")
        for u in unmapped:
            print(f"    {u}")
        print("  → Add to ISIN_TO_SYMBOL")

    return holdings, snapshot_date, totals


def extract_row_metadata(html: str) -> dict[str, dict]:
    """For every <tr class='stock-row'> in index.html, extract:
        symbol → {target_price, action_label, action_class, action_text}
    target_price comes from the LAST <td> with a ₹ value (which is the
    target+upside cell in the simplified 7-cell stock-row layout).
    action comes from the action-tag <span> class + text."""
    out: dict[str, dict] = {}
    for m in ROW_RE.finditer(html):
        attrs, body = m.group(1), m.group(2)
        sym_m = SYMBOL_RE.search(attrs)
        if not sym_m:
            continue
        sym = sym_m.group(1)
        if sym in out:
            continue  # only keep first occurrence per symbol

        action_label = "—"
        action_class = None
        action_text = ""
        at = ACTION_TAG_RE.search(body)
        if at:
            action_class = at.group(1)
            action_label = ACTION_MAP.get(action_class, "—")
            action_text = at.group(2).strip()

        # Target lives in the cell whose text starts with ₹ and is rightmost
        # (the "₹800 · +300%" cell). Scan all <td> texts and take the last
        # one with a ₹ that isn't the CMP cell. We identify CMP by ordering:
        # CMP comes before target in the row, and the cell with both ₹ and
        # text-align:right but no upside annotation is CMP.
        cells = [c.group(1) for c in TD_RE.finditer(body)]
        target = None
        cmp_in_row = None
        # In the 7-cell layout: cells[3]=CMP, cells[5]=target+upside
        # In legacy layouts: longer. Heuristic: rightmost ₹ in any cell is target.
        rupee_cells = [(i, c) for i, c in enumerate(cells) if PRICE_RE.search(c)]
        if rupee_cells:
            # CMP heuristic: lower-indexed ₹ cell without "%" in it
            for i, c in rupee_cells:
                if "%" not in c:
                    cmp_in_row = parse_price(c)
                    break
            # Target: rightmost ₹ cell; if it has multiple ₹ values, take the first
            target = parse_price(rupee_cells[-1][1])
            # If CMP and target are the same value (only one ₹ cell), target is unknown
            if cmp_in_row is not None and target == cmp_in_row and len(rupee_cells) == 1:
                target = None

        out[sym] = {
            "target": target,
            "action_label": action_label,
            "action_class": action_class,
            "action_text": action_text,
        }
    return out


def find_stale_research_files(held_symbols: set[str]) -> list[tuple[str, str]]:
    stale = []
    for sym in held_symbols:
        path = RESEARCH_DIR / f"{sym}.md"
        if not path.exists():
            continue
        text = path.read_text()
        m = STATUS_RE.search(text)
        if not m:
            continue
        status = m.group(1).strip()
        bad = any(t in status.upper() for t in ("EXITED", "SOLD"))
        ok = any(t in status.upper() for t in ("OWNED", "HOLD"))
        if bad and not ok:
            stale.append((sym, status[:120]))
    return stale


def render_snapshot_block(
    snapshot_date: str,
    invested: float,
    current: float,
    pnl: float,
    pnl_pct: float,
    avg_upside: float | None,
    upside_coverage_pct: float,
    num_holdings: int,
) -> str:
    pnl_color = "#166534" if pnl >= 0 else "#991b1b"
    pnl_sign = "+" if pnl >= 0 else ""
    if avg_upside is None:
        upside_html = '<span style="color:#94a3b8">—</span>'
    else:
        up_color = "#1e40af" if avg_upside >= 0 else "#991b1b"
        upside_html = (
            f'<b style="color:{up_color}">{avg_upside:+.1f}%</b> '
            f'<span style="color:#94a3b8;font-size:0.82rem">'
            f'({upside_coverage_pct:.0f}% of book · BUY/ADD/HOLD only)</span>'
        )
    return f"""<!-- BEGIN_PORTFOLIO_SNAPSHOT -->
<div id="portfolio-snapshot" style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:18px 22px;margin:14px auto 24px;max-width:1200px;font-family:-apple-system,BlinkMacSystemFont,sans-serif">
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px;flex-wrap:wrap;gap:8px">
    <h2 style="margin:0;font-size:1.05rem;font-weight:700;color:#1a1a2e">Portfolio Snapshot</h2>
    <span style="color:#64748b;font-size:0.82rem">as of {snapshot_date} · {num_holdings} holdings · <a href="portfolio.html" style="color:#1d4ed8;text-decoration:none">full view ↗</a></span>
  </div>
  <div style="display:flex;gap:28px;flex-wrap:wrap;font-size:0.93rem;line-height:1.6">
    <div><span style="color:#64748b">Invested:</span> <b>₹{invested/100000:.2f}L</b></div>
    <div><span style="color:#64748b">Current:</span> <b>₹{current/100000:.2f}L</b></div>
    <div><span style="color:#64748b">P&amp;L:</span> <b style="color:{pnl_color}">{pnl_sign}₹{pnl/1000:.2f}K ({pnl_pct:+.2f}%)</b></div>
    <div><span style="color:#64748b">Avg upside (active holds):</span> {upside_html}</div>
  </div>
</div>
<!-- END_PORTFOLIO_SNAPSHOT -->"""


def render_portfolio_html(
    snapshot_date: str,
    invested: float,
    current: float,
    pnl: float,
    pnl_pct: float,
    avg_upside: float | None,
    upside_coverage_pct: float,
    holdings: list[dict],
) -> str:
    holdings_sorted = sorted(holdings, key=lambda h: -h["current"])

    rows: list[str] = []
    for h in holdings_sorted:
        wt = (h["current"] / current * 100) if current else 0
        pl_color = "#166534" if h["pnl"] >= 0 else "#991b1b"
        pl_sign = "+" if h["pnl"] >= 0 else ""
        pnl_pct_s = (h["pnl"] / h["invested"] * 100) if h["invested"] else 0
        target_str = "—"
        target_sort = -1.0
        upside_str = "—"
        upside_color = "#94a3b8"
        upside_sort = -9999.0
        if h["target"] and h["target"] > 0 and h["cmp"] > 0:
            target_str = f"₹{h['target']:,.0f}"
            target_sort = h["target"]
            upside = (h["target"] / h["cmp"] - 1.0) * 100
            upside_sort = upside
            upside_str = f"{upside:+.1f}%"
            upside_color = "#1e40af" if upside >= 0 else "#991b1b"
        action = h.get("action_label") or "—"
        action_color = ACTION_COLORS.get(action, "#94a3b8")
        rows.append(f"""        <tr onclick="window.location.href='{h['symbol']}.html'" style="cursor:pointer">
          <td data-sort="{h['symbol']}"><b>{h['symbol']}</b></td>
          <td class="num" data-sort="{h['qty']}">{h['qty']:,.0f}</td>
          <td class="num" data-sort="{h['avg']}">₹{h['avg']:,.2f}</td>
          <td class="num" data-sort="{h['cmp']}" style="font-weight:600">₹{h['cmp']:,.2f}</td>
          <td class="num" data-sort="{h['invested']}">₹{h['invested']/1000:,.1f}K</td>
          <td class="num" data-sort="{h['current']}" style="font-weight:600">₹{h['current']/1000:,.1f}K</td>
          <td class="num" data-sort="{h['pnl']}" style="font-weight:600;color:{pl_color}">{pl_sign}₹{h['pnl']/1000:.1f}K</td>
          <td class="num" data-sort="{pnl_pct_s}" style="font-weight:600;color:{pl_color}">{pnl_pct_s:+.1f}%</td>
          <td class="num" data-sort="{wt}">{wt:.1f}%</td>
          <td class="num" data-sort="{target_sort}">{target_str}</td>
          <td class="num" data-sort="{upside_sort}" style="font-weight:600;color:{upside_color}">{upside_str}</td>
          <td data-sort="{action}" style="font-weight:700;color:{action_color}">{action}</td>
        </tr>""")
    rows_str = "\n".join(rows)

    pnl_color = "#166534" if pnl >= 0 else "#991b1b"
    pnl_sign = "+" if pnl >= 0 else ""
    if avg_upside is None:
        upside_display = "—"
        upside_color = "#94a3b8"
    else:
        upside_display = f"{avg_upside:+.1f}%"
        upside_color = "#1e40af" if avg_upside >= 0 else "#991b1b"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Portfolio · Stock Research</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #f8fafc; color: #1a1a2e; }}
  header {{ background: linear-gradient(135deg, #1a1a2e 0%, #2d3055 100%); color: #fff; padding: 18px 22px; }}
  header .top {{ display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 12px; max-width: 1320px; margin: 0 auto; }}
  header h1 {{ font-size: 1.4rem; font-weight: 700; }}
  header p {{ color: #94a3b8; font-size: 0.85rem; margin-top: 4px; }}
  .canonical-banner {{ background: #fef3c7; border-left: 4px solid #f59e0b; color: #78350f; padding: 9px 22px; font-size: 0.82rem; font-weight: 500; max-width: 1320px; margin: 0 auto; }}
  .canonical-banner code {{ background: rgba(0,0,0,0.06); padding: 1px 6px; border-radius: 3px; font-size: 0.92em; }}
  .nav-links a {{ color: #93c5fd; text-decoration: none; font-size: 0.88rem; margin-left: 8px; padding: 6px 12px; border: 1px solid rgba(147,197,253,0.3); border-radius: 6px; }}
  .nav-links a:hover {{ background: rgba(147,197,253,0.1); }}
  .container {{ max-width: 1320px; margin: 22px auto; padding: 0 22px; }}
  .snapshot {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 22px 26px; margin-bottom: 22px; }}
  .snapshot h2 {{ font-size: 1.05rem; font-weight: 700; margin-bottom: 14px; color: #1a1a2e; }}
  .snapshot-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; }}
  .stat-label {{ color: #64748b; font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px; }}
  .stat-value {{ font-size: 1.18rem; font-weight: 700; }}
  .stat-sub {{ display: block; font-size: 0.74rem; font-weight: 500; color: #94a3b8; margin-top: 2px; }}
  table {{ width: 100%; background: #fff; border-collapse: collapse; border-radius: 10px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}
  th {{ background: #f1f5f9; color: #475569; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; padding: 12px 10px; border-bottom: 2px solid #e2e8f0; text-align: left; cursor: pointer; user-select: none; position: relative; }}
  th:hover {{ background: #e2e8f0; color: #1a1a2e; }}
  th .sort-arrow {{ display: inline-block; margin-left: 4px; color: #94a3b8; font-size: 0.7rem; }}
  th.sort-active .sort-arrow {{ color: #1a1a2e; }}
  td {{ padding: 11px 10px; font-size: 0.88rem; border-bottom: 1px solid #f1f5f9; font-variant-numeric: tabular-nums; }}
  th.num, td.num {{ text-align: right; }}
  tr:last-child td {{ border-bottom: none; }}
  tbody tr:hover {{ background: #f8fafc; }}
  .totals-row td {{ background: #f1f5f9; font-weight: 700; border-top: 2px solid #cbd5e1; padding: 14px 10px; font-size: 0.92rem; }}
  .footer {{ color: #94a3b8; font-size: 0.76rem; text-align: center; margin: 28px 0 22px; line-height: 1.6; }}
  .footer code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 3px; font-size: 0.85em; }}
</style>
</head>
<body>

<header>
  <div class="top">
    <div>
      <h1>📊 Portfolio · Single Source of Truth</h1>
      <p>{len(holdings)} holdings · as of {snapshot_date} (broker close)</p>
    </div>
    <div class="nav-links">
      <a href="FOCUS.html" style="border-color:rgba(239,68,68,0.5);color:#fca5a5;font-weight:700">🎯 Focus</a>
      <a href="index.html">🔍 Research</a>
      <a href="INVESTING_PLAYBOOK.html">📖 Playbook</a>
      <a href="DECISION_LOG.html">📋 Decisions</a>
    </div>
  </div>
</header>
<div class="canonical-banner">
  Live portfolio state lives here. Generated from <code>data/portfolio.csv</code> (qty, avg) + latest broker xlsx (CMP) + <code>index.html</code> stock-rows (target, action) by <code>src/refresh_portfolio.py</code>. Do not hand-edit this file.
</div>

<div class="container">

  <div class="snapshot">
    <h2>Snapshot</h2>
    <div class="snapshot-grid">
      <div>
        <div class="stat-label">Invested</div>
        <div class="stat-value">₹{invested/100000:.2f}L</div>
      </div>
      <div>
        <div class="stat-label">Current</div>
        <div class="stat-value">₹{current/100000:.2f}L</div>
      </div>
      <div>
        <div class="stat-label">Unrealised P&amp;L</div>
        <div class="stat-value" style="color:{pnl_color}">{pnl_sign}₹{pnl/1000:.2f}K
          <span class="stat-sub">{pnl_pct:+.2f}%</span>
        </div>
      </div>
      <div>
        <div class="stat-label">Avg Upside · Active Holds</div>
        <div class="stat-value" style="color:{upside_color}">{upside_display}
          <span class="stat-sub">{upside_coverage_pct:.0f}% of book · BUY/ADD/HOLD only</span>
        </div>
      </div>
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th>Symbol<span class="sort-arrow"></span></th>
        <th class="num">Qty<span class="sort-arrow"></span></th>
        <th class="num">Avg<span class="sort-arrow"></span></th>
        <th class="num">CMP<span class="sort-arrow"></span></th>
        <th class="num">Invested<span class="sort-arrow"></span></th>
        <th class="num sort-active">Current<span class="sort-arrow">▼</span></th>
        <th class="num">P&amp;L<span class="sort-arrow"></span></th>
        <th class="num">P&amp;L %<span class="sort-arrow"></span></th>
        <th class="num" title="Position weight as % of total portfolio current value">% Portfolio<span class="sort-arrow"></span></th>
        <th class="num">Target<span class="sort-arrow"></span></th>
        <th class="num" title="(target / CMP − 1) × 100. Raw distance to target — no horizon implied.">Upside %<span class="sort-arrow"></span></th>
        <th title="From research file action tag in index.html">Action<span class="sort-arrow"></span></th>
      </tr>
    </thead>
    <tbody>
{rows_str}
      <tr class="totals-row">
        <td colspan="4">TOTAL · {len(holdings)} holdings</td>
        <td class="num">₹{invested/100000:.2f}L</td>
        <td class="num">₹{current/100000:.2f}L</td>
        <td class="num" style="color:{pnl_color}">{pnl_sign}₹{pnl/1000:.2f}K</td>
        <td class="num" style="color:{pnl_color}">{pnl_pct:+.2f}%</td>
        <td class="num">100.0%</td>
        <td class="num">—</td>
        <td class="num" style="color:{upside_color}">{upside_display}</td>
        <td>active</td>
      </tr>
    </tbody>
  </table>

  <p class="footer">
    Click any column header to sort · Click any row to open the research note · CMPs from broker close on {snapshot_date}<br>
    Upside % = (target / CMP − 1) × 100. <b>No horizon assumed</b> — targets in research files use different timeframes (1yr fair value vs 3-5yr multi-bagger base case). Treat upside as raw distance to whatever the latest research target says.<br>
    Refresh: drop new broker xlsx into <code>data/broker-exports/</code>, then <code>python3 src/refresh_portfolio.py --write</code>
  </p>

</div>

<script>
(function() {{
  const table = document.querySelector('table');
  const tbody = table.querySelector('tbody');
  const headers = table.querySelectorAll('thead th');
  let sortState = {{ col: 5, dir: -1 }};

  function getSortValue(td) {{
    const raw = td.dataset.sort;
    if (raw === undefined) return td.textContent.trim();
    const n = parseFloat(raw);
    return isNaN(n) ? raw : n;
  }}

  function sortBy(colIdx) {{
    if (sortState.col === colIdx) {{
      sortState.dir *= -1;
    }} else {{
      sortState.col = colIdx;
      sortState.dir = (colIdx === 0 || colIdx === 11) ? 1 : -1;
    }}
    const dataRows = Array.from(tbody.querySelectorAll('tr:not(.totals-row)'));
    const totalsRow = tbody.querySelector('.totals-row');
    dataRows.sort((a, b) => {{
      const av = getSortValue(a.cells[colIdx]);
      const bv = getSortValue(b.cells[colIdx]);
      if (typeof av === 'number' && typeof bv === 'number') return (av - bv) * sortState.dir;
      return String(av).localeCompare(String(bv)) * sortState.dir;
    }});
    dataRows.forEach(r => tbody.appendChild(r));
    if (totalsRow) tbody.appendChild(totalsRow);
    headers.forEach((th, i) => {{
      const arrow = th.querySelector('.sort-arrow');
      if (i === colIdx) {{
        th.classList.add('sort-active');
        arrow.textContent = sortState.dir === 1 ? '▲' : '▼';
      }} else {{
        th.classList.remove('sort-active');
        if (arrow) arrow.textContent = '';
      }}
    }});
  }}

  headers.forEach((th, i) => th.addEventListener('click', () => sortBy(i)));
}})();
</script>

</body>
</html>
"""


def insert_snapshot(html: str, block: str) -> str:
    if SNAPSHOT_RE.search(html):
        return SNAPSHOT_RE.sub(block, html)
    anchor = "<!-- ═══════════ TABLE VIEW ═══════════ -->"
    if anchor in html:
        return html.replace(anchor, block + "\n\n  " + anchor)
    return html.replace("</h1>", "</h1>\n" + block, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="apply changes to disk")
    args = ap.parse_args()

    broker_path = find_latest_broker_export()
    print(f"Broker export: {broker_path.relative_to(ROOT)}")
    holdings, snapshot_date, broker_totals = parse_broker_export(broker_path)
    print(f"Snapshot date: {snapshot_date}  |  {len(holdings)} holdings parsed")

    html = HTML_PATH.read_text()
    row_meta = extract_row_metadata(html)
    print(f"Read {len(row_meta)} stock-row entries from index.html")

    per_stock: list[dict] = []
    missing_meta: list[str] = []
    for sym, h in holdings.items():
        meta = row_meta.get(sym, {})
        if sym not in row_meta:
            missing_meta.append(sym)
        per_stock.append({
            "symbol": sym,
            "qty": h["qty"],
            "avg": h["avg"],
            "cmp": h["close"],
            "invested": h["invested"],
            "current": h["current"],
            "pnl": h["pnl"],
            "target": meta.get("target"),
            "action_label": meta.get("action_label", "—"),
            "action_text": meta.get("action_text", ""),
        })

    if missing_meta:
        print(f"⚠ Held but no stock-row in index.html: {sorted(missing_meta)}")

    invested_sum = sum(s["invested"] for s in per_stock)
    current_sum = sum(s["current"] for s in per_stock)
    pnl_sum = current_sum - invested_sum
    pnl_pct = (pnl_sum / invested_sum * 100) if invested_sum else 0.0

    # Avg upside, current-weighted, BUY/ADD/HOLD only
    upside_weighted_value = 0.0
    upside_covered = 0.0
    for s in per_stock:
        if s["action_label"] in ACTIVE_ACTIONS and s["target"] and s["cmp"]:
            up = (s["target"] / s["cmp"] - 1.0) * 100
            upside_weighted_value += up * s["current"]
            upside_covered += s["current"]
    avg_upside = (upside_weighted_value / upside_covered) if upside_covered else None
    upside_coverage_pct = (upside_covered / current_sum * 100) if current_sum else 0.0

    # Console snapshot
    print()
    print("─" * 78)
    print(f"PORTFOLIO SNAPSHOT  ·  as of {snapshot_date}  ·  {len(per_stock)} holdings")
    print("─" * 78)
    print(f"  Invested:  ₹{invested_sum/100000:,.2f}L")
    print(f"  Current:   ₹{current_sum/100000:,.2f}L")
    sign = "+" if pnl_sum >= 0 else ""
    print(f"  P&L:       {sign}₹{pnl_sum/1000:,.2f}K  ({pnl_pct:+.2f}%)")
    if avg_upside is None:
        print(f"  Avg upside (active holds):  — (no BUY/ADD/HOLD positions with targets)")
    else:
        print(f"  Avg upside (BUY/ADD/HOLD):  {avg_upside:+.1f}%  ({upside_coverage_pct:.0f}% of book)")
    print()
    print(f"  {'Symbol':<14}{'Wt%':>6}{'CMP':>10}{'Target':>10}{'Upside':>9}{'Action':>9}{'P&L%':>9}")
    for s in sorted(per_stock, key=lambda x: -x["current"]):
        wt = (s["current"] / current_sum * 100) if current_sum else 0
        target_s = f"₹{s['target']:,.0f}" if s["target"] else "—"
        upside_s = "—"
        if s["target"] and s["cmp"]:
            up = (s["target"] / s["cmp"] - 1.0) * 100
            upside_s = f"{up:+.1f}%"
        pnl_p = ((s["cmp"] - s["avg"]) / s["avg"] * 100) if s["avg"] else 0
        print(f"  {s['symbol']:<14}{wt:>5.1f}%{s['cmp']:>10,.2f}{target_s:>10}{upside_s:>9}{s['action_label']:>9}{pnl_p:>+8.1f}%")
    print("─" * 78)

    # Stale Status header detection
    held_symbols = {sym for sym, h in holdings.items() if h["qty"] > 1}
    stale = find_stale_research_files(held_symbols)
    if stale:
        print()
        print(f"⚠ Stale research files ({len(stale)}):")
        for sym, status in stale:
            print(f"    {sym}: {status}")

    # Render snapshot block + portfolio.html
    block = render_snapshot_block(
        snapshot_date=snapshot_date,
        invested=invested_sum,
        current=current_sum,
        pnl=pnl_sum,
        pnl_pct=pnl_pct,
        avg_upside=avg_upside,
        upside_coverage_pct=upside_coverage_pct,
        num_holdings=len(per_stock),
    )
    new_html = insert_snapshot(html, block)

    portfolio_html = render_portfolio_html(
        snapshot_date=snapshot_date,
        invested=invested_sum,
        current=current_sum,
        pnl=pnl_sum,
        pnl_pct=pnl_pct,
        avg_upside=avg_upside,
        upside_coverage_pct=upside_coverage_pct,
        holdings=per_stock,
    )

    # HTML generation retired 2026-07-20. index.html and portfolio.html are now
    # auto-generated from research/*.md and portfolio.csv with fresh bhavcopy
    # closes by scripts/build_site_index.py and scripts/build_portfolio_page.py
    # (wired into the daily cron). This script no longer writes either file — it
    # would overwrite them with stale broker-export prices. Kept as a read-only
    # broker-reconciliation reporter: the console snapshot above compares the
    # broker export to your positions. _ = (new_html, portfolio_html)
    _ = (new_html, portfolio_html)
    if args.write:
        print("\n⚠ --write is retired. The site pages are auto-generated now:")
        print("    venv/bin/python3 scripts/build_site_index.py      # research index")
        print("    venv/bin/python3 scripts/build_portfolio_page.py  # portfolio page")
        print("  This script is now a read-only broker-reconciliation reporter.")
    else:
        print("\n(read-only reporter; the site pages are built by the two scripts above)")


if __name__ == "__main__":
    main()
