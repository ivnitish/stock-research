# Full Stock Research — Deep Analysis

Run the complete multi-bagger research framework on `$ARGUMENTS`.

## Steps

1. **Resolve the ticker and detect market:**
   - Indian: no suffix, or ends in .NS/.BO/.BSE → use India workflow
   - US: standard US tickers (NVDA, GOOGL, etc.) → use US workflow
   - If ambiguous, ask the user

2. **Archive existing research (if any):**
   - Check if `research/$ARGUMENTS.md` (or `research/us/$ARGUMENTS.md` for US) exists
   - If yes, determine next version number from `research/archive/`
   - Copy to `research/archive/${ARGUMENTS}_v${N}.md`
   - Log: "Archived previous version as v{N}"

3. **Run the full research framework using a subagent:**
   - Use a subagent to keep the main context clean
   - The subagent should read `.claude/skills/stock-research/SKILL.md` for the full methodology
   - For India: fetch from Screener.in, BSE filings (`python3 src/fetch_bse_filings.py $ARGUMENTS`), WebSearch
   - For US: fetch from Alpha Vantage MCP, SEC filings via WebSearch, WebFetch
   - Follow the template at `research/_TEMPLATE.md` for output structure
   - Apply writing quality rules: narrative over formula, show math, be skeptical

4. **Save the research:**
   - India: `research/$ARGUMENTS.md`
   - US: `research/us/$ARGUMENTS.md`

5. **Render and open for review:**
   - Render the markdown to HTML using the standard renderer
   - Open in Chrome for the user to review

6. **Update index if needed:**
   - If this is a new stock (not an update), add it to `output/html/index.html` stock list

## Quality gates (do not skip)
- Every number must have a source — no fabricated data
- CMP must come from Tickertape or Google Finance (NOT Screener.in, NOT Yahoo Finance)
- Bull/bear/compounding sections must read as narratives, not formula-filling
- Research log must have dated entries with source references
