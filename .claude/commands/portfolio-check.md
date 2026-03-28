# Portfolio Check — Holdings vs Research Theses

Review live portfolio against research theses. Flags divergences, stale research, and missing coverage.

## Steps

1. **Fetch live holdings:**
   - Use Kite MCP: `mcp__kite__get_holdings` to get current portfolio
   - Extract: symbol, quantity, average price, current value, P&L%

2. **Cross-reference each holding against research:**
   - For each symbol, check if `research/SYMBOL.md` exists
   - If it exists, extract from the research file:
     - Recommendation (BUY/HOLD/EXIT)
     - Action table price levels (buy zone, hold zone, exit trigger)
     - Last updated date (from Version History or Research Log)
     - Quality score (/25)
     - Key exit triggers

3. **Flag issues:**
   - **NO RESEARCH:** Holding exists but no `research/SYMBOL.md` → needs research
   - **STALE:** Research file last updated > 90 days ago → needs refresh
   - **EXIT TRIGGER:** Current price has crossed an exit trigger level
   - **BELOW BUY ZONE:** Price dropped below the action table's buy zone → potential add opportunity
   - **CONCENTRATION:** Any single holding > 10% of portfolio value

4. **Output summary table:**

```
## Portfolio Health Check — [DATE]

| Symbol | Qty | Avg | CMP | P&L% | Score | Recommendation | Status |
|--------|-----|-----|-----|------|-------|---------------|--------|
| ...    | ... | ... | ... | ...  | ../25 | BUY/HOLD/EXIT | OK/FLAG |

### Flags
- [SYMBOL]: [issue description and suggested action]

### Missing Research
- [list of holdings without research files]

### Summary
- Total holdings: X
- With research: X | Without: X | Stale: X
- Flags raised: X
```

5. **Optionally run red flag monitor:**
   - If `src/red_flag_monitor.py` exists, run it: `python3 src/red_flag_monitor.py`
   - Append any red flags to the output
