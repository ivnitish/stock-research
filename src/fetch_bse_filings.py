#!/usr/bin/env python3
"""
fetch_bse_filings.py — On-demand BSE filing fetcher

Usage:
  python3 scripts/fetch_bse_filings.py KERNEX
  python3 scripts/fetch_bse_filings.py RAYMOND --days 180
  python3 scripts/fetch_bse_filings.py ALL           # fetch for all portfolio companies
  python3 scripts/fetch_bse_filings.py KERNEX --list # list only, no download

Downloads: Quarterly results, concall transcripts, annual reports, investor presentations
Saves to:  data/filings/{SYMBOL}/{DATE}_{CATEGORY}_{HEADLINE}.pdf
"""

import sys, os, re, json, time, requests
from datetime import datetime, timedelta
from pathlib import Path

# ── Portfolio companies: SYMBOL → BSE scrip code ──────────────────────────────
PORTFOLIO = {
    "ICICIAMC":   543235,
    "GROWW":      544046,
    "KERNEX":     532686,
    "NEWGEN":     540900,
    "KAYNES":     543664,
    "EPACKPEB":   544540,
    "ANANTRAJ":   500007,
    "SHAKTIPUMP": 531431,
    "BANCOINDIA": 500039,
    "SAKSOFT":    590051,
    "ARTEMISMED": 526779,
    "NAVA":       513023,
    "RAYMOND":    500330,
    "RSYSTEMS":   532735,
    "ETERNAL":    543321,
    "SHILCTECH":  543285,
    "PARADEEP":   543530,
    "STLNETWORK": 532517,
    "SWANDEF":    543399,
    "HDFCBANK":   500180,
    "GRSE":       542011,
    "NESCO":      505355,
    "DREDGECORP": 523618,
    "NILE":       530129,
    "DCMSIL":     544702,
    "KAYA":       539276,
    "PRIMAINNO":  544855,
    "PRIMAPLAS":  530589,
    # US stocks don't have BSE codes — skip them
}

# ── Categories to download ─────────────────────────────────────────────────────
RELEVANT_CATEGORIES = {
    "Result",
    "Results",
    "Annual Report",
    "Board Meeting",
    "Analyst / Investor Meet",
    "Company Update",
    "Investor Presentation",
}

RELEVANT_SUBCATS = {
    "Financial Results",
    "Quarterly Results",
    "Annual Report",
    "Analyst / Investor Meet - Con. Call Transcript",
    "Investor Presentation",
    "Outcome of Board Meeting",
}

BASE_DATA_DIR = Path(__file__).parent.parent / "data" / "filings"
BSE_API = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w"

# BSE moves attachments between directories as they age: recent filings sit in
# AttachLive, older ones (roughly 30+ days) are shifted to AttachHis, and a few
# land under CorpAttachment. The path is not in the API response, so try each in
# turn — hitting only AttachLive returns 404 on every historical filing.
BSE_PDF_DIRS = (
    "https://www.bseindia.com/xml-data/corpfiling/AttachLive/{filename}",
    "https://www.bseindia.com/xml-data/corpfiling/AttachHis/{filename}",
    "https://www.bseindia.com/xml-data/corpfiling/CorpAttachment/{filename}",
)
MIN_PDF_BYTES = 2000  # BSE serves a short HTML error body instead of a 404 sometimes
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.bseindia.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120",
}

def slugify(text, maxlen=60):
    """Clean text for use in filename."""
    text = re.sub(r'[^\w\s\-]', '', text)
    text = re.sub(r'\s+', '_', text.strip())
    return text[:maxlen]

def fetch_announcements(scrip_code, days=365):
    """Fetch announcements from BSE API for the past N days."""
    to_date   = datetime.now()
    from_date = to_date - timedelta(days=days)
    params = {
        "pageno":      1,
        "strCat":      -1,
        "strPrevDate": from_date.strftime("%Y%m%d"),
        "strScrip":    scrip_code,
        "strSearch":   "P",
        "strToDate":   to_date.strftime("%Y%m%d"),
        "strType":     "C",
        "subcategory": -1,
    }
    try:
        r = requests.get(BSE_API, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        return data.get("Table", [])
    except Exception as e:
        print(f"  ✗ API error: {e}")
        return []

def is_relevant(ann):
    """Return True if the announcement is a filing we care about."""
    cat    = ann.get("CATEGORYNAME", "")
    subcat = ann.get("SUBCATNAME", "")
    has_pdf = ann.get("PDFFLAG", 0) == 1
    if not has_pdf:
        return False
    if cat in RELEVANT_CATEGORIES:
        return True
    if subcat in RELEVANT_SUBCATS:
        return True
    # Catch concall transcripts by keyword
    headline = ann.get("HEADLINE", "").lower()
    if any(k in headline for k in ["conference call", "concall", "transcript", "investor meet", "annual report"]):
        return True
    return False

def download_pdf(ann, symbol, dry_run=False):
    """Download a single PDF filing and save it."""
    filename    = ann.get("ATTACHMENTNAME", "")
    date_str    = ann.get("DT_TM", "")[:10].replace("-", "")   # YYYYMMDD
    category    = slugify(ann.get("SUBCATNAME") or ann.get("CATEGORYNAME", "Filing"))
    headline    = slugify(ann.get("NEWSSUB") or ann.get("HEADLINE", ""), maxlen=50)
    out_name    = f"{date_str}_{category}_{headline}.pdf"

    out_dir = BASE_DATA_DIR / symbol
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / out_name

    if out_path.exists() and out_path.stat().st_size >= MIN_PDF_BYTES:
        print(f"  ↳ Already exists: {out_name}")
        return True

    if dry_run:
        print(f"  ↳ [LIST] {out_name}")
        return True

    if not filename:
        print(f"  ✗ No attachment on this announcement: {out_name}")
        return False

    errors = []
    for template in BSE_PDF_DIRS:
        url = template.format(filename=filename)
        subdir = template.rsplit("/", 2)[-2]
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code != 200:
                errors.append(f"{subdir}:{r.status_code}")
                continue
            if len(r.content) < MIN_PDF_BYTES:
                errors.append(f"{subdir}:short({len(r.content)}B)")
                continue
            out_path.write_bytes(r.content)
            size_kb = out_path.stat().st_size // 1024
            print(f"  ✓ {out_name} ({size_kb} KB) [{subdir}]")
            return True
        except Exception as e:
            errors.append(f"{subdir}:{type(e).__name__}")

    print(f"  ✗ Download failed: {out_name} — tried {', '.join(errors)}")
    return False

def process_symbol(symbol, scrip_code, days=365, dry_run=False):
    print(f"\n{'─'*60}")
    print(f"  {symbol} (BSE: {scrip_code}) — last {days} days")
    print(f"{'─'*60}")

    announcements = fetch_announcements(scrip_code, days)
    if not announcements:
        print("  No announcements found.")
        return

    relevant = [a for a in announcements if is_relevant(a)]
    print(f"  Found {len(announcements)} announcements → {len(relevant)} relevant filings\n")

    for ann in relevant:
        date  = ann.get("DT_TM", "")[:10]
        subcat = ann.get("SUBCATNAME") or ann.get("CATEGORYNAME", "")
        subj  = ann.get("NEWSSUB", ann.get("HEADLINE", ""))[:70]
        print(f"  [{date}] {subcat}: {subj}")
        download_pdf(ann, symbol, dry_run=dry_run)
        time.sleep(0.3)  # be polite to BSE servers

def main():
    args    = sys.argv[1:]
    dry_run = "--list" in args
    args    = [a for a in args if not a.startswith("--list")]

    days = 365
    for i, a in enumerate(args):
        if a == "--days" and i + 1 < len(args):
            days = int(args[i + 1])
    args = [a for a in args if a != "--days" and not a.isdigit() or a.isalpha()]

    if not args:
        print("Usage: python3 fetch_bse_filings.py SYMBOL [--days 180] [--list]")
        print(f"Known symbols: {', '.join(sorted(PORTFOLIO))}")
        sys.exit(1)

    target = args[0].upper()

    if target == "ALL":
        for sym, code in sorted(PORTFOLIO.items()):
            process_symbol(sym, code, days=days, dry_run=dry_run)
    elif target in PORTFOLIO:
        process_symbol(target, PORTFOLIO[target], days=days, dry_run=dry_run)
    else:
        # Try treating as a raw BSE code
        try:
            code = int(target)
            process_symbol(f"BSE_{code}", code, days=days, dry_run=dry_run)
        except ValueError:
            print(f"Unknown symbol: {target}")
            print(f"Known: {', '.join(sorted(PORTFOLIO))}")
            sys.exit(1)

    print(f"\n{'─'*60}")
    print(f"  Done. Files saved to: {BASE_DATA_DIR}")
    print(f"{'─'*60}\n")

if __name__ == "__main__":
    main()
