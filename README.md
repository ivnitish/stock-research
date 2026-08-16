# Stock Research System

Personal fundamental research system for identifying multi-bagger opportunities in Indian equities (NSE/BSE) with selective US positions.

**Philosophy:** Charles Munger — read a lot, analyze deeply, hold long. Target: 25% IRR.

---

## What's Here

### Research Files (`research/`)
Per-company investment theses using a structured multi-bagger framework:
- Kill Filter → Compounding Engine → Management Quality → Competitive Landscape → Valuation
- Quality Score: 5 dimensions × 5 points = 25 max (A/B/C/D grade)
- DCF: Bear / Base / Bull with capacity-anchored growth rates

### Site pages (auto-generated 2026-07-20)
- **`output/html/index.html`** — research index across all coverage. Auto-generated from `research/*.md` by `scripts/build_site_index.py`: every note appears with its auto-classified verdict bucket (Buy / Buy-at / Hold / Watchlist / Trim / Exit / Avoid / Notes), grade, and **fresh bhavcopy CMP**. Filter chips + search + sortable columns. Never hand-edited.
- **`output/html/portfolio.html`** — live portfolio state. Auto-generated from `data/portfolio.csv` (qty, avg) + fresh bhavcopy CMP by `scripts/build_portfolio_page.py`. Sortable table, per-stock action read from its research note.
- Both rebuild every morning via the daily cron; run the two scripts manually (`/refresh-portfolio`) to rebuild on demand.
- `PORTFOLIO_OVERVIEW.html` is a legacy redirect; old markdown archived under `research/archive/`.

Hosted at: [ivnitish.github.io/stock-research](https://ivnitish.github.io/stock-research)

### Source-of-truth chain
```
research/*.md  ──(header verdict/grade/date)──┐
data/portfolio.csv (qty, avg) ────────────────┤   fresh bhavcopy close (CMP)
                                              ↓ scripts/build_site_index.py
                                              ↓ scripts/build_portfolio_page.py
                          output/html/index.html + portfolio.html
```
Notes:
- Prices are the official exchange **bhavcopy close** (end-of-day), not live. CMP is blank for names with no matched exchange ticker (US, some BSE-SME) — correct, never guessed.
- Holdings (qty/avg) are only as current as `data/portfolio.csv`; refresh it after trades. `src/refresh_portfolio.py` (no `--write`) still prints a broker-xlsx-vs-CSV reconciliation report; its HTML output is retired.

### Automation (`scripts/`, `src/`)
- `scripts/build_site_index.py` — regenerate the research index (fresh bhavcopy CMP)
- `scripts/build_portfolio_page.py` — regenerate the portfolio page (fresh bhavcopy CMP)
- `src/refresh_portfolio.py` — broker-xlsx-vs-CSV reconciliation reporter (HTML output retired)
- Daily portfolio price update (7pm)
- Weekly red flag monitor (promoter pledging, ROCE decline)
- Obsolete scripts archived under `src/archive/`: `portfolio_overview.py`, `portfolio_update.py`, `portfolio_review.py`

### Scheduled Jobs

The daily brief runs in **GitHub Actions** (primary, since Aug 2026); everything
else is still a macOS launchd agent on one Mac.

#### GitHub Actions — daily brief (primary)
`.github/workflows/daily-telegram.yml` — weekdays 03:12 UTC / 08:42 IST, with a
fallback slot at 09:12 UTC / 14:42 IST that no-ops once the day's `Morning News
YYYY-MM-DD` issue exists. Runs `collect_daily_inputs.py`, then the `morning-news`
skill via `anthropics/claude-code-action`, commits `docs/MACRO_THREAD.md` +
`docs/MORNING_BRIEF.md` back to `main`, then delivers the digest with
`send_macro_digest.py --require-today --strict`.

Required repo secrets (**Settings → Secrets and variables → Actions**):

| Secret | Purpose |
|---|---|
| `TELEGRAM_BOT_TOKEN` | digest delivery — value is in the local `.env` |
| `TELEGRAM_ALLOWED_CHAT_ID` | digest delivery — value is in the local `.env` |
| `CLAUDE_CODE_OAUTH_TOKEN` *or* `ANTHROPIC_API_KEY` | runs the brief. The OAuth token bills the Claude subscription; the API key bills API credits. |

Failure is loud by design — a run that delivers nothing turns red **and** pings
Telegram, because the previous setup made a dead job and a quiet market look
identical (the brief silently stopped on 2026-07-24 and went unnoticed for
weeks). Manual run / dry-run: **Actions → Daily Telegram Brief → Run workflow**.

`TELEGRAM_BOT_TOKEN` is deliberately withheld from the Claude step so the skill's
own Step 8b send stays a no-op and the digest is delivered exactly once, by
`send_macro_digest.py`.

#### launchd (local Mac, added Jul 2026)
macOS launchd agents (plists in `~/Library/LaunchAgents/`, scripts in `scripts/`). launchd runs missed jobs on wake, unlike cron.
- `com.nitish.stocks.nightly-filings` → `scripts/nightly_filings_cron.sh` — weekdays 21:12 IST, fetches BSE filings for all portfolio companies (zero Claude tokens). Log: `data/logs/nightly_filings.log`
- `com.nitish.stocks.daily-news` → `scripts/daily_news_cron.sh` — weekdays 08:42 IST with retry slots at 11:42/14:42/17:42/20:42 (each run no-ops once the day's brief succeeds — stamp file `data/logs/daily_news_last_success`; lock dir prevents overlap). Headless Claude run: morning news brief for holdings + buy-at alert check (web-sourced CMPs, no broker MCPs) → GitHub issue with the full brief, plus ONE short Telegram theme digest (3-6 lines: general themes, in-zone alerts, issue link — the only daily Telegram touchpoint, consolidated 2026-07-18). Log: `data/logs/daily_news.log`. **Now the fallback, not the primary** — the Actions workflow above runs first, and each local slot checks GitHub for today's `Morning News YYYY-MM-DD` issue and stands down if it already exists. Safe to leave enabled or bootout entirely.
- `com.nitish.stocks.fintwitter-finds` → `scripts/weekly_fintwitter_cron.sh` — **Saturdays** 10:00 IST, retry 18:15 (converted from daily 2026-07-18; stamp `data/logs/fintwitter_finds_last_success`). Headless Claude run: scans Indian fintwitter / ValuePickr / ThreadReader over the last 7 days (contrarian lens in `docs/FINTWITTER_WATCHLIST.md`), writes `docs/FINTWITTER_FINDS.md`, posts it as a GitHub issue (`Fintwitter Weekly YYYY-MM-DD`), then sends one short Telegram ping — pick count, new adds, Tier-1 names, issue link. No PDF, no chunked digest. Log: `data/logs/fintwitter_finds.log`. On-demand: `scripts/run_fintwitter_weekly.sh` (`FINTWITTER_DRY_RUN=1` for dry-run).
- ~~**Cloud routine (planned primary for the news brief)**~~ — superseded Aug 2026 by the GitHub Actions workflow above, which covers the same laptop-independence without a separate claude.ai environment to maintain.
- (removed 2026-07-06, user preference: news over price movements) `scripts/daily_portfolio_telegram.py` still works on demand — `venv/bin/python3 scripts/daily_portfolio_telegram.py` sends a portfolio EOD digest to Telegram from official NSE/BSE bhavcopy closes, zero Claude tokens

Manage: `launchctl list | grep nitish.stocks` · trigger now: `launchctl kickstart gui/$(id -u)/<label>` · disable: `launchctl bootout gui/$(id -u)/~/Library/LaunchAgents/<label>.plist`

### BSE Filing Fetcher (`scripts/fetch_bse_filings.py`)
On-demand downloader for quarterly results, concall transcripts, annual reports, investor presentations from BSE.
```bash
python3 scripts/fetch_bse_filings.py KERNEX           # last 365 days
python3 scripts/fetch_bse_filings.py RAYMOND --days 180
python3 scripts/fetch_bse_filings.py ALL              # all portfolio stocks
```
Downloads to: `data/financial statemnt and concals/{SYMBOL}/`

---

## Portfolio Companies

20 Indian stocks across defence, EMS, aerospace, fintech, BFSI, capital goods, and pharma.

---

## Key Docs

| Doc | Purpose |
|-----|---------|
| `research/_TEMPLATE.md` | Master research template |
| `docs/RESEARCH_APPROACH.md` | Data sources + research workflow |
| `docs/VALUATION_FRAMEWORK.md` | DCF + P/B-ROE methodology |
| `docs/TODO.md` | Active decisions + research backlog |
| `docs/SUPPLIER_CUSTOMER_DATA.md` | Customer/supplier analysis for all portfolio stocks |
