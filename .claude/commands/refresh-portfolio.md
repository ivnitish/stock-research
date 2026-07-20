# Refresh Portfolio — rebuild the site pages with fresh closes

**Changed 2026-07-20.** The portfolio page and research index are auto-generated
with fresh **bhavcopy** closes. This command just reruns the generators (the
daily cron already does this every morning). The old broker-xlsx →
`refresh_portfolio.py --write` flow is retired for HTML output.

## What it does

1. `scripts/build_site_index.py` → rewrites `output/html/index.html` from
   `research/*.md` with fresh bhavcopy CMP and auto verdict buckets.
2. `scripts/build_portfolio_page.py` → rewrites `output/html/portfolio.html`
   from `data/portfolio.csv` (qty, avg) + fresh bhavcopy CMP + each note's action.

Both are zero-token and idempotent. Prices are always the latest exchange close;
holdings are only as current as `data/portfolio.csv`.

## How to invoke

User says `/refresh-portfolio`.

## Steps

1. **Run both generators:**
   ```bash
   cd "/Users/nitish/stocks automation"
   venv/bin/python3 scripts/build_site_index.py
   venv/bin/python3 scripts/build_portfolio_page.py
   ```
   Report the printed stats (holdings count, invested/current/P&L, any unpriced names).

2. **If the user has traded recently**, remind them `data/portfolio.csv` is the
   holdings source and must be updated by hand (or reconciled against a broker
   export) for the P&L to be exact — that is the one step needing a broker pull.
   `src/refresh_portfolio.py` (no `--write`) still prints a broker-vs-CSV
   reconciliation report if a fresh xlsx is in `data/broker-exports/`.

3. **Commit + push** if there are changes:
   ```bash
   git add output/html/index.html output/html/portfolio.html
   git commit -m "Rebuild site pages with fresh bhavcopy closes <DATE>"
   git push origin main
   ```

## When to use it

- After writing/updating a research note (to surface it in the index immediately).
- At the start of a session where you want current P&L without waiting for cron.
- Before buy/sell decisions (fresh CMPs).

## Notes

- Do NOT hand-edit `index.html` / `portfolio.html` — changes are lost on rebuild.
- CMP is blank for names with no matched exchange ticker (US, some BSE-SME).
  That is correct — never fill it with a guessed number.
