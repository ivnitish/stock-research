# Refresh Portfolio — One-Command Snapshot

Refreshes the portfolio snapshot in `output/html/index.html` (and `output/html/portfolio.html` once that exists) from the latest broker holdings export.

## What it does

1. Reads the most-recent xlsx file under `data/broker-exports/` (broker holdings statement from Groww/Kite).
2. Joins it with `data/portfolio.csv` (qty, avg buy price).
3. Updates each held row in `index.html`:
   - CMP cell from broker close
   - Δ/share, current value, P&L abs, P&L %
4. Computes weighted expected 3-yr CAGR from each row's base-case target cell.
5. Inserts/updates the **Portfolio Snapshot** block at the top of index.html (invested · current · P&L · expected CAGR · holdings count · snapshot date).
6. Flags stale `research/SYMBOL.md` `Status:` headers — held positions where the file still says EXITED/WATCHLIST.

Idempotent. Re-running with no new data is a no-op.

## How to invoke

User says `/refresh-portfolio` (optionally followed by an integer for the CAGR horizon, default 3 years).

## Steps

1. **Run the script (dry-run first to show diff):**
   ```bash
   cd "/Users/nitish/stocks automation"
   python3 src/refresh_portfolio.py
   ```
   Show the user the snapshot table + per-stock CAGR breakdown + any stale-research warnings.

2. **If the user confirms (or says they want it pushed), apply:**
   ```bash
   python3 src/refresh_portfolio.py --write
   ```
   Optionally with `--horizon N` if they passed an integer arg (e.g. `/refresh-portfolio 5` → `--horizon 5`).

3. **Re-render any affected research HTML if research file headers changed** (rare on a refresh, but check git status).

4. **Commit + push** if there are changes:
   ```bash
   git add output/html/index.html data/broker-exports/ src/refresh_portfolio.py
   git commit -m "Refresh portfolio snapshot from broker export <DATE>"
   git push origin main
   ```
   Use a message that names the broker export date and key deltas (e.g., "P&L moved from +₹X to +₹Y").

## When to use it

- After dropping a new broker xlsx into `data/broker-exports/`
- At the start of any session where you want current P&L
- Before making buy/sell decisions (you want fresh CMPs)
- Weekly cadence as a session-end ritual

## When NOT to use

- If `data/broker-exports/` has no new file since last run, the dry-run will show "0 rows would change" — no point pushing a no-op commit.
- If the broker export's ISIN isn't in the script's `ISIN_TO_SYMBOL` map, the script will print a warning. Add the ISIN to the map in `src/refresh_portfolio.py` before re-running.

## Output to user

Always print:
- Snapshot date + holdings count
- Invested / Current / P&L (₹ + %)
- Weighted expected CAGR + coverage %
- Top-3 contributors and bottom-3 by CAGR
- Any stale research files flagged

Skip the per-row diff dump unless they ask for it.
