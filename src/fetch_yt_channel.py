#!/usr/bin/env python3
"""
fetch_yt_channel.py — Pull transcripts from a YouTube channel

Usage:
  python3 src/fetch_yt_channel.py URL                        # list recent 20 videos
  python3 src/fetch_yt_channel.py URL --n 50                 # list recent 50
  python3 src/fetch_yt_channel.py URL --filter "HDFC"        # filter by keyword in title
  python3 src/fetch_yt_channel.py URL --id VIDEO_ID          # fetch specific video
  python3 src/fetch_yt_channel.py URL --latest               # fetch most recent video transcript
  python3 src/fetch_yt_channel.py URL --filter "Kenneth" --fetch  # fetch all matching

Saves to: data/transcripts/CHANNEL_NAME/DATE_TITLE.md
"""

import sys, re, subprocess, json
from pathlib import Path
from datetime import datetime

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
except ImportError:
    print("Run: pip install youtube-transcript-api")
    sys.exit(1)

TRANSCRIPTS_DIR = Path(__file__).parent.parent / "data" / "transcripts"


def slugify(text, maxlen=80):
    text = re.sub(r'[^\w\s\-]', '', text)
    text = re.sub(r'\s+', '_', text.strip())
    return text[:maxlen]


def get_channel_videos(channel_url, n=20):
    """Use yt-dlp to list videos from a channel."""
    cmd = [
        "yt-dlp",
        "--flat-playlist",
        "--print", "%(id)s\t%(title)s\t%(upload_date)s",
        "--playlist-end", str(n),
        channel_url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    videos = []
    for line in result.stdout.strip().splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            vid_id   = parts[0].strip()
            title    = parts[1].strip() if len(parts) > 1 else ""
            date_raw = parts[2].strip() if len(parts) > 2 else "NA"
            # Format date
            if date_raw and date_raw != "NA" and len(date_raw) == 8:
                date = f"{date_raw[:4]}-{date_raw[4:6]}-{date_raw[6:]}"
            else:
                date = date_raw
            videos.append({"id": vid_id, "title": title, "date": date})
    return videos


def fetch_transcript(video_id, title="", date="NA", channel_slug="channel"):
    """Fetch transcript for a video and save as markdown."""
    print(f"\n  Fetching: {title or video_id}")

    api = YouTubeTranscriptApi()
    try:
        transcript_list = api.list(video_id)
        transcripts = list(transcript_list)

        # Prefer English (manual or auto); skip if English not available
        en_transcripts = [t for t in transcripts if t.language_code.startswith('en')]
        if not en_transcripts:
            langs = [t.language_code for t in transcripts]
            print(f"  ⚠ No English transcript — available: {langs}. Skipping.")
            return None

        chosen = en_transcripts[0]
        source = f"{'manual' if not chosen.is_generated else 'auto-generated'} ({chosen.language_code})"
        entries = chosen.fetch()

    except TranscriptsDisabled:
        print(f"  ✗ Transcripts disabled for {video_id}")
        return None
    except NoTranscriptFound:
        print(f"  ✗ No transcript found for {video_id}")
        return None
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None

    # Clean and join text (v1.x uses .text attribute on snippet objects)
    lines = []
    for entry in entries:
        text = entry.text.strip() if hasattr(entry, 'text') else str(entry).strip()
        text = text.replace("\n", " ").replace("[Music]", "").replace("[Applause]", "")
        text = re.sub(r'\s+', ' ', text)
        if text:
            lines.append(text)

    full_text = " ".join(lines)

    # Save
    out_dir = TRANSCRIPTS_DIR / channel_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    safe_title = slugify(title or video_id)
    filename = f"{date}_{safe_title}.md"
    out_path = out_dir / filename

    content = f"""# {title}

**Video ID:** {video_id}
**Date:** {date}
**Source:** YouTube transcript ({source})
**URL:** https://www.youtube.com/watch?v={video_id}
**Fetched:** {datetime.now().strftime('%Y-%m-%d')}

---

## Transcript

{full_text}
"""

    out_path.write_text(content, encoding="utf-8")
    word_count = len(full_text.split())
    print(f"  ✓ Saved: {filename} ({word_count:,} words, {source})")
    return out_path


def channel_slug_from_url(url):
    match = re.search(r'@([\w\-]+)', url)
    return match.group(1).lower() if match else "channel"


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    channel_url = args[0]
    slug = channel_slug_from_url(channel_url)

    # Parse flags
    n         = 20
    keyword   = None
    video_id  = None
    do_fetch  = False
    latest    = False

    i = 1
    while i < len(args):
        if args[i] == "--n" and i + 1 < len(args):
            n = int(args[i + 1]); i += 2
        elif args[i] == "--filter" and i + 1 < len(args):
            keyword = args[i + 1].lower(); i += 2
        elif args[i] == "--id" and i + 1 < len(args):
            video_id = args[i + 1]; i += 2
        elif args[i] == "--fetch":
            do_fetch = True; i += 1
        elif args[i] == "--latest":
            latest = True; i += 1
        else:
            i += 1

    # Single video by ID
    if video_id:
        fetch_transcript(video_id, channel_slug=slug)
        return

    # List videos from channel
    print(f"  Listing videos from {channel_url} (n={n}) ...")
    videos = get_channel_videos(channel_url, n=n)

    if not videos:
        print("  No videos found. Check the channel URL.")
        return

    # Apply keyword filter
    if keyword:
        videos = [v for v in videos if keyword in v["title"].lower()]
        print(f"  Filtered to {len(videos)} videos matching '{keyword}'")

    # Print list
    print(f"\n  {'#':<4} {'Date':<12} {'Title':<70} ID")
    print(f"  {'─'*4} {'─'*12} {'─'*70} {'─'*12}")
    for i, v in enumerate(videos, 1):
        print(f"  {i:<4} {v['date']:<12} {v['title'][:70]:<70} {v['id']}")

    # Fetch
    if latest:
        v = videos[0]
        fetch_transcript(v["id"], v["title"], v["date"], slug)
    elif do_fetch:
        print(f"\n  Fetching transcripts for {len(videos)} video(s)...")
        for v in videos:
            fetch_transcript(v["id"], v["title"], v["date"], slug)

    print(f"\n  Transcripts saved to: {TRANSCRIPTS_DIR / slug}/")


if __name__ == "__main__":
    main()
