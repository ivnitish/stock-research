"""
Reusable NSE bhav copy (EOD prices/volume) by stock ticker or stock details.
Official source: NSE archives. Use pre-downloaded files in data/bhav/ or try fetch from NSE.
Input: stock ticker (str) or stock details (dict); normalized via stock_input.
"""
import os
import zipfile
import io
from datetime import date
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import pandas as pd

from config import BHAV_COPY_DIR
from stock_input import to_symbol_series

# NSE bhav copy URL pattern (date like 07FEB2025)
_NSE_BHAV_URL = "https://www.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{day:02d}{month}{year}bhav.csv.zip"
_MONTHS = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()


def _month_str(d: date) -> str:
    return _MONTHS[d.month - 1]


def _path_for_date(d: date) -> str:
    """Preferred local path: data/bhav/YYYY-MM-DD.csv (standard) or cm{dd}{Mon}{yyyy}bhav.csv."""
    return os.path.join(BHAV_COPY_DIR, d.strftime("%Y-%m-%d") + ".csv")


def _legacy_path_for_date(d: date) -> str:
    """Legacy NSE filename: cm07FEB2025bhav.csv."""
    return os.path.join(BHAV_COPY_DIR, f"cm{d.day:02d}{_month_str(d)}{d.year}bhav.csv")


def load_bhav_for_date(d: date, path: str = None) -> pd.DataFrame | None:
    """
    Load bhav copy for a given date from a CSV path. If path is None, look in BHAV_COPY_DIR
    for YYYY-MM-DD.csv or cm{dd}{Mon}{yyyy}bhav.csv. Returns DataFrame with EQ rows only if
    SERIES column exists; otherwise returns all. Returns None if file missing.
    """
    if path is None:
        path = _path_for_date(d)
        if not os.path.isfile(path):
            path = _legacy_path_for_date(d)
    if not os.path.isfile(path):
        return None
    df = pd.read_csv(path)
    # Normalize column names (NSE uses uppercase)
    df.columns = [c.strip().upper() for c in df.columns]
    if "SERIES" in df.columns:
        df = df[df["SERIES"].astype(str).str.upper() == "EQ"].copy()
    return df


def fetch_bhav_from_nse(d: date) -> pd.DataFrame | None:
    """
    Try to download bhav copy for date from NSE. Returns DataFrame or None if fail.
    NSE may block without cookies; use local file if this fails.
    """
    url = _NSE_BHAV_URL.format(
        year=d.year,
        month=_month_str(d),
        day=d.day,
    )
    req = Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.nseindia.com/"})
    try:
        with urlopen(req, timeout=15) as resp:
            z = zipfile.ZipFile(io.BytesIO(resp.read()), "r")
            names = z.namelist()
            if not names:
                return None
            csv_content = z.read(names[0]).decode("utf-8", errors="replace")
            df = pd.read_csv(io.StringIO(csv_content))
            df.columns = [c.strip().upper() for c in df.columns]
            if "SERIES" in df.columns:
                df = df[df["SERIES"].astype(str).str.upper() == "EQ"].copy()
            return df
    except (HTTPError, URLError, zipfile.BadZipFile, Exception):
        return None


def get_bhav_for_date(d: date, try_nse: bool = True) -> pd.DataFrame | None:
    """
    Get bhav copy DataFrame for date: load from local BHAV_COPY_DIR first, then optionally
    try NSE download. try_nse=False to use only local files.
    """
    df = load_bhav_for_date(d)
    if df is not None:
        return df
    if try_nse:
        df = fetch_bhav_from_nse(d)
        if df is not None:
            os.makedirs(BHAV_COPY_DIR, exist_ok=True)
            df.to_csv(_path_for_date(d), index=False)
            return df
    return None


def get_eod(symbol_or_details, d: date, bhav_df: pd.DataFrame | None = None, try_nse: bool = True) -> dict | None:
    """
    Get EOD (end-of-day) for one stock: open, high, low, close, volume.
    symbol_or_details: stock ticker (e.g. RELIANCE, RELIANCE.NS) or dict {"symbol": "RELIANCE", "series": "EQ"}.
    d: date. bhav_df: optional pre-loaded bhav DataFrame; if None, load/fetch for d.
    try_nse: whether to try downloading from NSE if local file missing.
    Returns dict with keys like open, high, low, close, volume, symbol, timestamp, or None if not found.
    """
    symbol, series = to_symbol_series(symbol_or_details)
    if not symbol:
        return None
    if bhav_df is None:
        bhav_df = get_bhav_for_date(d, try_nse=try_nse)
    if bhav_df is None or bhav_df.empty:
        return None
    # Match row: SYMBOL (and SERIES if present)
    mask = bhav_df["SYMBOL"].astype(str).str.upper() == symbol
    if "SERIES" in bhav_df.columns:
        mask = mask & (bhav_df["SERIES"].astype(str).str.upper() == series)
    rows = bhav_df.loc[mask]
    if rows.empty:
        return None
    row = rows.iloc[0]
    out = {
        "symbol": symbol,
        "series": series,
        "open": _num(row.get("OPEN")),
        "high": _num(row.get("HIGH")),
        "low": _num(row.get("LOW")),
        "close": _num(row.get("CLOSE")),
        "volume": _num(row.get("TOTTRDQTY")),
    }
    if "TIMESTAMP" in row:
        out["timestamp"] = row["TIMESTAMP"]
    return out


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def get_eod_batch(symbols_or_details_list, d: date, bhav_df: pd.DataFrame | None = None, try_nse: bool = True) -> list[dict]:
    """
    Get EOD for multiple stocks. symbols_or_details_list: list of tickers or dicts.
    Returns list of dicts (same as get_eod); missing symbols are omitted.
    """
    if bhav_df is None:
        bhav_df = get_bhav_for_date(d, try_nse=try_nse)
    if bhav_df is None:
        return []
    out = []
    for s in symbols_or_details_list:
        row = get_eod(s, d, bhav_df=bhav_df, try_nse=False)
        if row:
            out.append(row)
    return out


if __name__ == "__main__":
    from datetime import date
    # Example: today or last weekday
    d = date.today()
    print(f"Bhav dir: {BHAV_COPY_DIR}")
    print("get_eod('RELIANCE', d) with try_nse=True then False:")
    eod = get_eod("RELIANCE", d, try_nse=True)
    if eod:
        print(eod)
    else:
        eod = get_eod("RELIANCE.NS", d, try_nse=False)
        print(eod or "(no local file; put CSV in data/bhav/YYYY-MM-DD.csv)")
    print("get_eod({'symbol': 'TCS', 'series': 'EQ'}, d):")
    print(get_eod({"symbol": "TCS", "series": "EQ"}, d, try_nse=False))
