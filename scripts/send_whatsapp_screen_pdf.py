#!/usr/bin/env python3
"""Render the WhatsApp idea-thread screen (5 names, last ~30 days) to a one-page
PDF and DM it to Telegram.

Every number here is sourced this session from Screener.in (2026-07-24) or, for
VOGL, from the 03-Jul-2026 same-day fact-check; nothing is fabricated. Full
theses live in research/{CPPLUS,SHEMAROO,VOGL,AURUM,GUJAPOLLO}.md.

Usage:
  venv/bin/python3 scripts/send_whatsapp_screen_pdf.py            # build + send
  venv/bin/python3 scripts/send_whatsapp_screen_pdf.py --dry-run  # build only
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv
import os

REPO = Path(__file__).resolve().parent.parent
load_dotenv(REPO / ".env")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HTML_PATH = REPO / "output" / "html" / "WHATSAPP_SCREEN.html"
PDF_PATH = REPO / "output" / "pdf" / "WHATSAPP_SCREEN_2026-07-24.pdf"

# (name, ticker, verdict, badge_class, one_liner, facts, action)
ROWS = [
    (
        "Aditya Infotech", "CPPLUS", "BUY AT ₹1,900–2,000", "buyat",
        "India's #1 CCTV/surveillance brand (CP Plus, ~45% share) — the clearest listed winner of the April-2026 ban on non-certified Chinese cameras.",
        "Real business, real trigger: FY26 revenue ₹4,221 Cr (+36%), PAT ₹368 Cr (+166%), ROCE 28%. But priced for perfection at 113x P/E, 22x book — and FY26 operating cash flow was ₹13 Cr against ₹368 Cr of profit (3.5% conversion), a working-capital build that must prove it reverses.",
        "CMP ₹3,534 — no position. Buy zone ₹1,900–2,000, gated on two quarters of OCF/PAT recovering above 0.5. Grade B (16/25). The one real business in the batch.",
    ),
    (
        "Shemaroo Entertainment", "SHEMAROO", "AVOID", "avoid",
        "Hindi film / devotional content library monetized across TV syndication, its ShemarooMe OTT app, and YouTube.",
        "Loss-making and shrinking: FY26 revenue ₹583 Cr (−15% YoY), net loss ₹218 Cr (worse than FY25's −₹84 Cr), 3-yr ROCE −9%, ROE −24%, ₹302 Cr debt. Cheap at 1.3x book — but book is eroding every quarter.",
        "CMP ₹123. AVOID — capital-destroying media business; no price fixes it. Grade D.",
    ),
    (
        "Vedanta Oil & Gas", "VOGL", "AVOID (trade only)", "avoid",
        "The oil & gas arm spun out of Vedanta (June-2026 five-way demerger, listed 15 Jun, 1:1). The Rajasthan ex-Cairn block.",
        "The WhatsApp pitch (\"₹8,900 Cr EBITDA vs ₹17,500 Cr mcap, ~2x EV/EBITDA\") is on a target, not trailing: FY26 revenue was ₹9,582 Cr with declining production. Genuine cheapness is a forced-seller spin-off dislocation (MSCI dropped Vedanta 22 Jun). Fails the framework on management (Agarwal cash-extraction history) and runway (capex fights depletion).",
        "~₹45. AVOID as a compounder — tradeable special situation only, size as a trade if at all. Grade D.",
    ),
    (
        "Aurum PropTech", "AURUM", "AVOID (watch)", "watch",
        "Real-estate-technology roll-up (leasing, rental payments, sales enablement, brokerage tech), assembled largely by acquisition.",
        "Just turned profitable: FY26 revenue ₹381 Cr (+44%), net profit ₹1 Cr (vs −₹41 Cr). TTM profit ₹30 Cr — but the quarterly path (Jun −10, Sep −8, Dec +3, Mar +45) shows it's essentially one quarter, ~53x TTM. 3-yr ROCE 1.84%, ROE −12% — capital hasn't earned yet, acquisition-led. A \"prove it,\" not a broken one.",
        "CMP ₹222. AVOID for now — revisit after 2–3 yrs of ROCE clearing the mid-teens on organic leverage. Grade C.",
    ),
    (
        "Gujarat Apollo Industries", "GUJAPOLLO", "AVOID (value trap)", "avoid",
        "Maker of crushing & screening equipment for the aggregates/construction industry.",
        "Cash-rich (₹118 Cr vs ₹456 Cr mcap) and below book (0.90x) — but the operating business loses money (FY26 OPM −20%), revenue has gone nowhere for 5 years (−1% CAGR), operating cash flow was −₹38.8 Cr, and the promoter has cut its stake 8.4 pts to 47.3%. The ₹6 Cr \"profit\" is other income on the cash pile, not the business.",
        "CMP ₹352. AVOID — cheap on assets, no operating engine, no catalyst to unlock the cash. Grade D.",
    ),
]

BADGE = {
    "buyat": ("#1e5f3a", "#d6f5e3"),
    "avoid": ("#7a1f1f", "#f6dede"),
    "watch": ("#7a5a13", "#f7eccf"),
}


def render_html() -> str:
    cards = []
    for name, tk, verdict, cls, one, facts, action in ROWS:
        fg, bg = BADGE[cls]
        cards.append(f"""
        <div class="card">
          <div class="chead">
            <div><span class="name">{name}</span> <span class="tk">{tk}</span></div>
            <span class="badge" style="color:{fg};background:{bg};">{verdict}</span>
          </div>
          <div class="one">{one}</div>
          <div class="facts">{facts}</div>
          <div class="action"><b>Action:</b> {action}</div>
        </div>""")
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>
  @page {{ size: A4; margin: 14mm 12mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif; color:#1a1a1a; font-size:11px; line-height:1.5; margin:0; }}
  h1 {{ font-size:18px; margin:0 0 2px; }}
  .sub {{ color:#666; font-size:10.5px; margin-bottom:14px; }}
  .card {{ border:1px solid #e2e2e2; border-radius:8px; padding:11px 13px; margin-bottom:10px; page-break-inside:avoid; }}
  .chead {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:5px; }}
  .name {{ font-weight:700; font-size:13px; }}
  .tk {{ color:#888; font-size:10px; font-weight:600; letter-spacing:.3px; }}
  .badge {{ font-weight:700; font-size:10px; padding:3px 9px; border-radius:20px; white-space:nowrap; }}
  .one {{ color:#333; margin-bottom:5px; }}
  .facts {{ color:#333; margin-bottom:6px; }}
  .action {{ background:#f6f7f9; border-radius:6px; padding:6px 9px; font-size:10.5px; }}
  .foot {{ color:#999; font-size:9.5px; margin-top:8px; border-top:1px solid #eee; padding-top:8px; }}
</style></head><body>
  <h1>WhatsApp Idea-Thread Screen — 5 Names</h1>
  <div class="sub">Screened from the idea thread, last ~30 days · 2026-07-24 · sorted best-to-worst · full theses in research/{{TICKER}}.md</div>
  {''.join(cards)}
  <div class="foot">One real business (Aditya Infotech, gated on price + cash conversion); four AVOIDs for a compounding book. Data: Screener.in (2026-07-24); VOGL from the 03-Jul same-day fact-check. Nothing fabricated — figures dated and sourced. Not investment advice.</div>
</body></html>"""


def main() -> int:
    HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    HTML_PATH.write_text(render_html(), encoding="utf-8")
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={PDF_PATH}", f"file://{HTML_PATH.resolve()}"],
        check=True, timeout=60,
    )
    print(f"PDF: {PDF_PATH} ({PDF_PATH.stat().st_size // 1024} KB)")
    if "--dry-run" in sys.argv:
        return 0

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat = os.environ.get("TELEGRAM_ALLOWED_CHAT_ID", "").strip()
    if not token or not chat:
        print("TELEGRAM_BOT_TOKEN / TELEGRAM_ALLOWED_CHAT_ID missing — skip send", file=sys.stderr)
        return 0

    intro = (
        "Screen of the 5 names from the idea thread (last ~30 days). Verdict:\n\n"
        "• Aditya Infotech (CPPLUS) — BUY AT ₹1,900–2,000 (the one real business; gated on cash conversion; AVOID at ₹3,534)\n"
        "• Shemaroo — AVOID (loss-making, shrinking)\n"
        "• Vedanta Oil & Gas (VOGL) — AVOID as a compounder, trade-only special situation\n"
        "• Aurum PropTech — AVOID/watch (just turned profitable, returns unproven)\n"
        "• Gujarat Apollo — AVOID (cash-rich value trap)\n\n"
        "PDF one-pager attached; full theses on the research site."
    )
    r = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": int(chat), "text": intro}, timeout=30,
    )
    r.raise_for_status()
    with PDF_PATH.open("rb") as fh:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendDocument",
            data={"chat_id": int(chat),
                  "caption": "5-name WhatsApp screen · 2026-07-24 · 1 buy-at, 4 avoids"},
            files={"document": (PDF_PATH.name, fh, "application/pdf")},
            timeout=60,
        )
    r.raise_for_status()
    print("sent intro + PDF to Telegram")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
