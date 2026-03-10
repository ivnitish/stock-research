"""
Import Groww broker Excel exports into the project's data format.
Parses Holdings, Orders, and P&L Excel files from data/groww/.

Usage:
  python src/groww_importer.py                    # parse all, export portfolio + decisions
  python src/groww_importer.py --holdings-only    # just portfolio.csv
"""
from __future__ import annotations

import os
import sys

import pandas as pd

# Ensure project root is on path for config/stock_input imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import GROWW_DATA_DIR, PORTFOLIO_PATH, JOURNAL_DIR


# ---------------------------------------------------------------------------
# Holdings parser
# ---------------------------------------------------------------------------

def parse_holdings(filepath: str | None = None) -> pd.DataFrame:
    """
    Parse Groww Holdings Statement Excel into a clean DataFrame.
    Returns columns: stock_name, symbol, isin, quantity, avg_buy_price,
                     buy_value, closing_price, closing_value, unrealised_pnl
    """
    if filepath is None:
        filepath = _find_file(GROWW_DATA_DIR, "Holdings")
    raw = pd.read_excel(filepath, header=None)

    # Find the header row (contains "Stock Name" or "ISIN")
    header_idx = None
    for i, row in raw.iterrows():
        vals = [str(v).strip().lower() for v in row.values if pd.notna(v)]
        if "isin" in vals or "stock name" in vals:
            header_idx = i
            break
    if header_idx is None:
        raise ValueError(f"Could not find header row in {filepath}")

    # Re-read with correct header
    df = raw.iloc[header_idx + 1:].copy()
    df.columns = raw.iloc[header_idx].values
    df = df.dropna(subset=[df.columns[0]])  # drop empty rows
    df = df.reset_index(drop=True)

    # Normalize column names
    col_map = {}
    for c in df.columns:
        cl = str(c).strip().lower()
        if "stock name" in cl or cl == "name":
            col_map[c] = "stock_name"
        elif cl == "isin":
            col_map[c] = "isin"
        elif cl == "quantity":
            col_map[c] = "quantity"
        elif "average" in cl or "avg" in cl:
            col_map[c] = "avg_buy_price"
        elif "buy value" in cl:
            col_map[c] = "buy_value"
        elif "closing price" in cl:
            col_map[c] = "closing_price"
        elif "closing value" in cl:
            col_map[c] = "closing_value"
        elif "unrealised" in cl or "p&l" in cl:
            col_map[c] = "unrealised_pnl"
    df = df.rename(columns=col_map)

    # Keep only known columns
    keep = ["stock_name", "isin", "quantity", "avg_buy_price", "buy_value",
            "closing_price", "closing_value", "unrealised_pnl"]
    df = df[[c for c in keep if c in df.columns]]

    # Convert numeric columns
    for c in ["quantity", "avg_buy_price", "buy_value", "closing_price",
              "closing_value", "unrealised_pnl"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["quantity"] = df["quantity"].astype(int)

    # Add NSE ticker symbol from the order-history style symbol (via ISIN lookup)
    # Also try name-based fuzzy match as fallback for ISIN mismatches
    def _resolve_symbol(row):
        sym = ISIN_TO_SYMBOL.get(row.get("isin", ""), "")
        if sym:
            return sym
        # Fallback: try matching stock_name prefix against order history names
        name = str(row.get("stock_name", "")).strip().upper()
        for isin, s in ISIN_TO_SYMBOL.items():
            if s.upper() in name or name[:8] in s.upper():
                return s
        return ""
    df["symbol"] = df.apply(_resolve_symbol, axis=1)

    return df


# ---------------------------------------------------------------------------
# Orders parser
# ---------------------------------------------------------------------------

def parse_orders(filepath: str | None = None) -> pd.DataFrame:
    """
    Parse Groww Order History Excel into a clean DataFrame.
    Returns columns: date, stock_name, symbol, isin, action, quantity, value,
                     exchange, order_status
    """
    if filepath is None:
        filepath = _find_file(GROWW_DATA_DIR, "Orders")
    raw = pd.read_excel(filepath, header=None)

    # Find header row
    header_idx = None
    for i, row in raw.iterrows():
        vals = [str(v).strip().lower() for v in row.values if pd.notna(v)]
        if "isin" in vals and ("stock name" in vals or "type" in vals):
            header_idx = i
            break
    if header_idx is None:
        raise ValueError(f"Could not find header row in {filepath}")

    df = raw.iloc[header_idx + 1:].copy()
    df.columns = raw.iloc[header_idx].values
    df = df.dropna(subset=[df.columns[0]])
    df = df.reset_index(drop=True)

    # Normalize column names
    col_map = {}
    for c in df.columns:
        cl = str(c).strip().lower()
        if "stock name" in cl:
            col_map[c] = "stock_name"
        elif cl == "symbol":
            col_map[c] = "symbol"
        elif cl == "isin":
            col_map[c] = "isin"
        elif cl == "type":
            col_map[c] = "action"
        elif cl == "quantity":
            col_map[c] = "quantity"
        elif cl == "value":
            col_map[c] = "value"
        elif cl == "exchange":
            col_map[c] = "exchange"
        elif "execution" in cl or "date" in cl:
            col_map[c] = "exec_datetime"
        elif "order status" in cl or "status" in cl:
            col_map[c] = "order_status"
    df = df.rename(columns=col_map)

    # Filter executed orders only
    if "order_status" in df.columns:
        df = df[df["order_status"].str.strip().str.lower() == "executed"]

    # Parse datetime
    if "exec_datetime" in df.columns:
        df["date"] = pd.to_datetime(df["exec_datetime"], format="mixed", dayfirst=True).dt.date

    # Numeric columns
    for c in ["quantity", "value"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Normalize action
    if "action" in df.columns:
        df["action"] = df["action"].str.strip().str.upper()

    # Add .NS ticker
    if "symbol" in df.columns:
        df["ticker"] = df["symbol"].str.strip().str.upper() + ".NS"

    keep = ["date", "stock_name", "symbol", "isin", "action", "quantity",
            "value", "exchange", "ticker"]
    df = df[[c for c in keep if c in df.columns]]
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# ISIN → NSE Symbol mapping (built from the Orders Excel which has both)
# ---------------------------------------------------------------------------

# This gets populated by build_isin_map() from orders data
ISIN_TO_SYMBOL: dict[str, str] = {}


def build_isin_map(orders_path: str | None = None) -> dict[str, str]:
    """Build ISIN → NSE symbol map from order history (which has both columns)."""
    global ISIN_TO_SYMBOL
    if orders_path is None:
        orders_path = _find_file(GROWW_DATA_DIR, "Orders")
    raw = pd.read_excel(orders_path, header=None)

    header_idx = None
    for i, row in raw.iterrows():
        vals = [str(v).strip().lower() for v in row.values if pd.notna(v)]
        if "isin" in vals and "symbol" in vals:
            header_idx = i
            break
    if header_idx is None:
        return {}

    df = raw.iloc[header_idx + 1:].copy()
    df.columns = raw.iloc[header_idx].values

    # Find ISIN and Symbol columns
    isin_col = symbol_col = None
    for c in df.columns:
        cl = str(c).strip().lower()
        if cl == "isin":
            isin_col = c
        elif cl == "symbol":
            symbol_col = c
    if isin_col is None or symbol_col is None:
        return {}

    for _, row in df.iterrows():
        isin = str(row[isin_col]).strip()
        sym = str(row[symbol_col]).strip().upper()
        if isin.startswith("INE") and sym and sym != "NAN":
            ISIN_TO_SYMBOL[isin] = sym

    return ISIN_TO_SYMBOL


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------

def export_portfolio(holdings_path: str | None = None,
                     output_path: str | None = None) -> str:
    """Export clean portfolio CSV from holdings Excel."""
    if output_path is None:
        output_path = PORTFOLIO_PATH

    # Build ISIN map first
    build_isin_map()

    df = parse_holdings(holdings_path)

    # Build portfolio rows
    rows = []
    for _, r in df.iterrows():
        sym = r.get("symbol", "")
        if not sym:
            # Try ISIN lookup
            sym = ISIN_TO_SYMBOL.get(r.get("isin", ""), "")
        if not sym:
            print(f"  WARNING: No symbol for {r.get('stock_name', '?')} (ISIN: {r.get('isin', '?')})")
            continue
        rows.append({
            "symbol": f"{sym}.NS",
            "quantity": int(r["quantity"]),
            "avg_buy_price": round(float(r["avg_buy_price"]), 2),
            "exchange": "NSE",
        })

    out = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    out.to_csv(output_path, index=False)
    print(f"Portfolio: {len(out)} stocks → {output_path}")
    return output_path


def export_decisions(orders_path: str | None = None,
                     output_path: str | None = None) -> str:
    """Export decision log CSV from order history."""
    if output_path is None:
        output_path = os.path.join(JOURNAL_DIR, "decisions.csv")

    df = parse_orders(orders_path)

    rows = []
    for _, r in df.iterrows():
        sym = r.get("symbol", r.get("ticker", ""))
        qty = int(r["quantity"]) if pd.notna(r.get("quantity")) else 0
        price = round(float(r["value"]) / qty, 2) if qty > 0 and pd.notna(r.get("value")) else 0
        rows.append({
            "date": r.get("date", ""),
            "stock": f"{sym}.NS" if not sym.endswith(".NS") else sym,
            "action": r.get("action", ""),
            "quantity": qty,
            "price": price,
            "value": round(float(r.get("value", 0)), 2),
            "reasoning": "",  # To be filled manually
            "review_date": "",
        })

    out = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    out.to_csv(output_path, index=False)
    print(f"Decisions: {len(out)} orders → {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _find_file(directory: str, keyword: str) -> str:
    """Find first file in directory matching keyword."""
    for f in os.listdir(directory):
        if keyword.lower() in f.lower() and f.endswith((".xlsx", ".xls")):
            return os.path.join(directory, f)
    raise FileNotFoundError(f"No file matching '{keyword}' in {directory}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== Groww Importer ===\n")

    # Build ISIN → Symbol map from orders
    isin_map = build_isin_map()
    print(f"ISIN map: {len(isin_map)} symbols loaded from order history\n")

    # Export portfolio
    export_portfolio()
    print()

    # Export decisions
    if "--holdings-only" not in sys.argv:
        export_decisions()
        print()

    # Print summary
    if os.path.exists(PORTFOLIO_PATH):
        df = pd.read_csv(PORTFOLIO_PATH)
        total = (df["quantity"] * df["avg_buy_price"]).sum()
        print(f"Summary: {len(df)} stocks, ₹{total:,.0f} invested")


if __name__ == "__main__":
    main()
