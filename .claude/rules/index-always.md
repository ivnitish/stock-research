Every time a new research file is created (research/SYMBOL.md) or an HTML is generated (output/html/SYMBOL.html), you MUST immediately add an entry to output/html/index.html before ending the session.

## Where to add

**Table view (required):** Add a `<tr class="stock-row">` row in the appropriate section:
- Grade A (20-25/25) → `data-section="grade-a india"`
- Grade B (15-19/25) → `data-section="grade-b india"`
- Grade C (<15/25) → `data-section="grade-c india"`
- Watchlist / No buy yet → `data-section="watch"`
- Reference / Macro doc → `data-section="watch" data-grade="w"`

**Cards view (for watchlist stocks with completed thesis):** Add an `<a class="card">` in the appropriate grid section.

## Row template (table)

```html
<tr class="stock-row" data-section="watch" data-grade="b" onclick="go('SYMBOL.html')">
  <td><div class="td-ticker">SYMBOL<div class="td-company">Company Name <span class="val-tag val-under">Undervalued</span></div></div></td>
  <td class="col-hide-sm"><span class="grade grade-B">B · 17/25</span></td>
  <td class="col-hide-sm num-cell num-dim">—</td><td class="col-hide-sm num-cell num-dim">—</td><td class="col-hide-sm num-cell num-dim">—</td><td class="col-hide-sm num-cell num-dim">—</td><td class="col-hide-sm num-cell num-dim">—</td><td class="col-hide-sm num-cell num-dim">—</td><td class="col-hide-sm num-cell num-dim">—</td>
  <td class="num-cell pl-none">—</td>
  <td class="col-hide-sm"><span class="action-tag act-watch">Watch · Buy &lt;₹XXX</span></td>
  <td class="col-hide-sm num-cell" style="color:#166534;font-weight:600">₹TARGET</td>
  <td class="col-hide-sm num-cell num-dim">₹CMP</td>
  <td class="col-hide-sm num-cell num-dim">₹BUY_ZONE</td>
  <td class="col-hide-sm num-cell num-dim">~Xx</td>
  <td class="td-arrow">›</td>
</tr>
```

## val-tag classes
- `val-deep` = deep value (P/B < 0.5x or very undervalued)
- `val-under` = undervalued
- `val-fair` = fairly valued
- `val-rich` = expensive / overvalued

## action-tag classes
- `act-buy` = strong buy
- `act-add` = add / accumulate
- `act-hold` = hold
- `act-watch` = watchlist
- `act-exit` = exit / avoid
- `act-ref` = reference document

## grade classes
- `grade-A` = Grade A (green)
- `grade-B` = Grade B (yellow)
- `grade-C` = Grade C (red)
- `grade-W` = Watch/Reference (grey)

Never skip this step. The index is the homepage on GitHub Pages — if it's not in the index, it effectively doesn't exist.
