Run the fintwitter-finds skill in FULL mode.

Read `.claude/skills/fintwitter-finds/SKILL.md` and `references/SCAN_PROMPT.md`.
Execute the full daily pipeline:
1. Scan Indian fintwitter / ValuePickr / ThreadReader (last 24h)
2. Update `data/fintwitter_finds_metrics.json` and `docs/FINTWITTER_FINDS.md`
3. Run `scripts/run_fintwitter_daily.sh` (Screener fetch → Telegram text + PDF)

Apply contrarian lens from `docs/FINTWITTER_WATCHLIST.md`. Never fabricate numbers.