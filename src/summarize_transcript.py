#!/usr/bin/env python3
"""
summarize_transcript.py — Generate structured investment summary from a YouTube transcript

Usage:
  python3 src/summarize_transcript.py data/transcripts/CHANNEL/FILE.md
  python3 src/summarize_transcript.py data/transcripts/CHANNEL/FILE.md --no-synthesis  # skip synthesis update

Requires: ANTHROPIC_API_KEY env var
Saves:
  - data/transcripts/CHANNEL/FILE_summary.md   (per-video summary)
  - data/transcripts/SYNTHESIS.md              (rolling combined doc, updated)
"""

import sys, os, re
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("Run: pip install anthropic")
    sys.exit(1)

TRANSCRIPTS_DIR = Path(__file__).parent.parent / "data" / "transcripts"
SYNTHESIS_FILE  = TRANSCRIPTS_DIR / "SYNTHESIS.md"

SUMMARY_PROMPT = """You are an investment analyst assistant working for a Munger-style long-term equity investor focused on Indian and US small/mid-cap stocks.

Below is a YouTube transcript from a financial podcast or interview. Generate a structured investment summary with these exact sections:

## Guest & Context
One line: who is the guest, their firm, what they manage.

## Macro View
3-5 bullet points covering their view on: markets, economy, geopolitics, rates, oil — whatever they covered. Include specific numbers where mentioned.

## Sector Bets (3-5 year horizon)
Bulleted list of sectors they are positive/negative on, with brief reasoning. Flag any that overlap with our portfolio themes: defence, energy/renewables, banking/NBFCs, manufacturing/EMS, IT services.

## Stocks & Companies Mentioned
Table with: Company | Sentiment (Bullish/Bearish/Neutral/Mentioned) | What was said (one line)
Only include if they gave a substantive view, not just name-dropping.

## Key Numbers & Data Points
Bullet list of specific numbers, thresholds, or statistics that are useful for investing context. Examples: "FII outflows $45B since Sep 2024 = GFC-equivalent", "IT sector: AI could displace 1-1.5M jobs in 3-5 years".

## Portfolio Relevance
2-4 sentences: what does this mean specifically for our portfolio? Our holdings include: defence (DCMSIL, GRSE, SWANDEF), banking (HDFCBANK), renewables (NAVA), manufacturing (KAYNES, EPACKPEB), IT (RSYSTEMS, SAKSOFT, NEWGEN), pharma (ARTEMISMED).

## Contrarian / Interesting Takes
1-3 things the guest said that are non-consensus, surprising, or worth flagging.

## One-Line Verdict
One sentence: the single most important investing takeaway from this episode.

---
Keep each section tight. No filler. Use specific numbers from the transcript wherever possible.

TRANSCRIPT:
{transcript}"""

SYNTHESIS_ENTRY_PROMPT = """You are maintaining a rolling investment intelligence document. A new video has been summarized.

Add a new dated entry to the synthesis document by extracting only what is ADDITIVE — new data points, updated views, changed probabilities, new sector calls — compared to what a typical investor would already know.

Do NOT repeat generic advice. Focus on: specific numbers, thesis changes, emerging themes, portfolio-relevant signals.

Format the new entry as:

---
### {date} — {title} (Guest: {guest})
**Key adds:**
- [bullet 1]
- [bullet 2]
- [bullet 3]

**Portfolio signal:** [one line on what to do or watch]

---

SUMMARY TO DISTILL:
{summary}"""


def get_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        print("ERROR: Set ANTHROPIC_API_KEY environment variable.")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)
    return key


def read_transcript(path: Path) -> tuple[str, str, str]:
    """Returns (raw_text, title, date)."""
    content = path.read_text(encoding="utf-8")
    title = ""
    date  = "NA"
    for line in content.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
        if line.startswith("**Date:**"):
            date = line.replace("**Date:**", "").strip()
    # Extract transcript body
    if "## Transcript" in content:
        transcript = content.split("## Transcript", 1)[1].strip()
    else:
        transcript = content
    return transcript, title, date


def generate_summary(transcript: str, title: str, client) -> str:
    prompt = SUMMARY_PROMPT.format(transcript=transcript[:40000])  # ~10k tokens max
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def update_synthesis(summary: str, title: str, date: str, guest: str, client):
    """Append new entry to SYNTHESIS.md."""
    # Extract guest from summary if not provided
    if not guest:
        match = re.search(r'## Guest & Context\n(.+)', summary)
        guest = match.group(1).strip() if match else "Unknown"

    entry_prompt = SYNTHESIS_ENTRY_PROMPT.format(
        date=date, title=title[:60], guest=guest, summary=summary
    )
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": entry_prompt}]
    )
    new_entry = response.content[0].text.strip()

    # Read or create synthesis doc
    if SYNTHESIS_FILE.exists():
        existing = SYNTHESIS_FILE.read_text(encoding="utf-8")
    else:
        existing = """# Investment Intelligence Synthesis

Rolling document — key insights extracted from investor podcasts, interviews, and commentary.
Newest entries at top. Each entry captures only additive, non-obvious information.

---
"""

    # Insert new entry after the header block (after first ---)
    parts = existing.split("---", 1)
    if len(parts) == 2:
        updated = parts[0] + "---\n\n" + new_entry + "\n\n" + parts[1].lstrip()
    else:
        updated = existing + "\n\n" + new_entry

    SYNTHESIS_FILE.write_text(updated, encoding="utf-8")
    print(f"  ✓ Synthesis updated: {SYNTHESIS_FILE}")


def summarize_file(transcript_path: Path, update_synth=True):
    client = anthropic.Anthropic(api_key=get_api_key())

    transcript, title, date = read_transcript(transcript_path)
    if not transcript.strip():
        print(f"  ✗ Empty transcript: {transcript_path}")
        return

    print(f"  Summarizing: {title or transcript_path.name}")
    summary = generate_summary(transcript, title, client)

    # Save summary alongside transcript
    summary_path = transcript_path.with_name(
        transcript_path.stem + "_summary.md"
    )
    summary_content = f"""# Summary: {title}

**Source:** {transcript_path.name}
**Date:** {date}
**Summarized:** {datetime.now().strftime('%Y-%m-%d')}

---

{summary}
"""
    summary_path.write_text(summary_content, encoding="utf-8")
    print(f"  ✓ Summary saved: {summary_path.name}")

    if update_synth:
        update_synthesis(summary, title, date, guest="", client=client)

    return summary_path


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    no_synthesis = "--no-synthesis" in args
    paths = [a for a in args if not a.startswith("--")]

    for p in paths:
        path = Path(p)
        if not path.exists():
            print(f"  ✗ File not found: {p}")
            continue
        # Skip already-summarized files
        if path.stem.endswith("_summary"):
            print(f"  ↳ Skipping summary file: {path.name}")
            continue
        summarize_file(path, update_synth=not no_synthesis)


if __name__ == "__main__":
    main()
