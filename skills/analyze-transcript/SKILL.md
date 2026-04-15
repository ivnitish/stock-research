# Skill: analyze-transcript

Analyze a YouTube transcript or URL from first principles and link findings to the user's portfolio.

## Trigger
User says: `/analyze-transcript [URL or file path]`
Or: "analyze this transcript", "summarize this podcast", "what does X say about markets"

## Workflow

### Step 1 — Get the transcript
- If a YouTube URL is provided: run `python3 src/fetch_yt_channel.py URL --id VIDEO_ID` to fetch and save the transcript to `data/transcripts/CHANNEL/`
- If a file path is provided: read the file directly
- If transcript is already in context (user pasted it): use that

### Step 2 — Analyze from first principles using the prompt below

### Step 3 — Save outputs (always maintain the three-layer chain)

**Transcript file** (`data/transcripts/CHANNEL/DATE_TITLE.md`):
- Add header line: `**Summary:** [DATE_TITLE_summary.md](DATE_TITLE_summary.md) · [Synthesis](../SYNTHESIS.md)`

**Summary file** (`data/transcripts/CHANNEL/DATE_TITLE_summary.md`):
- Header line: `**Source:** [Raw Transcript](DATE_TITLE.md) · [Synthesis entry](../SYNTHESIS.md)`
- Full analysis using the framework below

**Synthesis** (`data/transcripts/SYNTHESIS.md`):
- Add new entry at top (after the header)
- Format: `### DATE — TITLE | GUEST, FIRM` with links to summary and transcript
- 4-5 bullet points — only non-obvious, specific, numbered facts
- One-line portfolio signal

Open summary in Chrome: `python3 src/render_plan.py PATH_TO_SUMMARY`

---

## Analysis Prompt (First Principles Framework)

Use this structure exactly. Be specific with numbers. No filler.

---

### Guest & Context
One line: who, what firm, what they manage, when recorded.

### Their Mental Model
What is the core framework this person uses to think about markets and investing?
Not what they said — what lens they see the world through. 2-3 sentences.

### Macro View
3-5 bullet points. Include specific numbers, thresholds, timeframes from the transcript.
Flag if this updates or contradicts our existing Iran war / geopolitical research in `research/geopolitical/IRAN_WAR_V2.md`.

### Sector Bets (3-5 year view)
| Sector | View | Reasoning | Overlap with our portfolio? |
|--------|------|-----------|----------------------------|

### Stocks & Companies Named
| Company | Sentiment | What they said (one line) |
|---------|-----------|--------------------------|
Only include if substantive view given.

### Key Numbers & Thresholds
Bullet list of specific, quotable data points. These are the facts worth remembering.

### First Principles Stress Test
Ask: does their thesis hold on first principles?
- What assumptions are they making?
- What would have to be true for them to be wrong?
- What is Munger's likely reaction to this view?

### Portfolio Impact Assessment
Go through our active positions and state what this changes (if anything):

**Strengthens thesis:**
- [Position] — [why]

**Weakens thesis or adds risk:**
- [Position] — [why]

**No change:**
- [List positions unaffected]

Our current holdings for reference:
- Defence: DCMSIL (watch), GRSE, SWANDEF
- Banking: HDFCBANK
- Renewables/Commodities: NAVA
- Manufacturing/EMS: KAYNES, EPACKPEB
- IT/SaaS: RSYSTEMS, SAKSOFT, NEWGEN
- Pharma: ARTEMISMED
- Others: ANANTRAJ, SHAKTIPUMP, BANCOINDIA, NILE, PARADEEP, STLNETWORK, ICICIAMC

### Contrarian / Non-Consensus Views
1-3 things the guest said that are genuinely non-obvious or worth flagging.

### What to Do (if anything)
Specific, actionable. Not "monitor" or "stay cautious" — either:
- "No action needed" (if nothing changed)
- "Revisit [position] because [specific reason from transcript]"
- "Add [company] to watchlist because [specific data point]"

### One-Line Verdict
Single sentence: the one thing worth remembering from this episode 6 months from now.

---

## Synthesis Entry Format
After analysis, add this compact entry to `data/transcripts/SYNTHESIS.md` (newest first):

```
---
### [DATE] — [TITLE] | [GUEST, FIRM]

**Key adds** (non-obvious, specific):
- [bullet]
- [bullet]
- [bullet]

**Portfolio signal:** [one actionable line]
---
```
