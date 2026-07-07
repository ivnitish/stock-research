#!/usr/bin/env python3
"""Build rich Telegram summary from fintwitter_finds_metrics.json into FINTWITTER_FINDS.md."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JSON_PATH = REPO / "data" / "fintwitter_finds_metrics.json"
MD_PATH = REPO / "docs" / "FINTWITTER_FINDS.md"

# Fallback attribution when JSON entry lacks source
try:
    import importlib.util

    _spec = importlib.util.spec_from_file_location(
        "pdf_build", REPO / "scripts" / "build_fintwitter_finds_pdf.py"
    )
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)  # type: ignore[union-attr]
    SOURCE_FALLBACK: dict[str, str] = getattr(_mod, "SOURCES", {})
except Exception:
    SOURCE_FALLBACK = {}

BUCKET_ORDER = [
    "B — Grid Supply Chain",
    "A — Value / Manufacturing",
    "C — TIA / Serious Investors",
]

TIER1_KEYWORDS = ("TIER 1", "actionable")


def fmt_pct(val: str | None, suffix: str = "%") -> str | None:
    if not val:
        return None
    v = str(val).strip()
    if v.startswith("-") or v.startswith("+"):
        return f"{v}{suffix}"
    try:
        float(v.replace(",", ""))
        return f"+{v}{suffix}" if not v.startswith("+") else f"{v}{suffix}"
    except ValueError:
        return v


def fmt_metrics(d: dict) -> str:
    parts: list[str] = []
    if d.get("mcap_cr"):
        parts.append(f"MCap {d['mcap_cr']} Cr")
    if d.get("cmp"):
        parts.append(f"CMP {d['cmp']}")
    if d.get("pe"):
        parts.append(f"P/E {d['pe']}")
    if d.get("pb"):
        parts.append(f"P/B {d['pb']}")
    if d.get("roe"):
        parts.append(f"ROE {d['roe']}%")
    sg = d.get("sales_growth_ttm") or d.get("sales_growth_3y")
    if sg:
        parts.append(f"sales {fmt_pct(sg)}")
    if d.get("npm"):
        parts.append(f"NPM {d['npm']}%")
    if d.get("roce"):
        parts.append(f"ROCE {d['roce']}%")
    return " / ".join(parts) if parts else "metrics pending — check PDF"


def short_name(name: str, d: dict) -> str:
    sym = (d.get("symbol") or "").strip()
    if sym and sym.isalpha() and len(sym) <= 12:
        return sym.upper()
    # BSE numeric codes — use readable short name
    compact = name.replace(".", "").replace(",", "")
    words = [w for w in compact.split() if w.lower() not in ("ltd", "limited", "india", "infra")]
    if len(words) >= 2:
        return "".join(w[0] for w in words[:3]).upper()
    return (words[0][:10] if words else name[:12]).upper()


def is_tier1(d: dict) -> bool:
    v = d.get("verdict", "").upper()
    return any(k in v for k in TIER1_KEYWORDS)


def build_blocks(data: dict) -> str:
    today = date.today().strftime("%d %b %Y")
    lines = [f"Fintwitter Finds — {today}", ""]

    tier1: list[tuple[str, dict]] = []
    by_bucket: dict[str, list[tuple[str, dict]]] = {b: [] for b in BUCKET_ORDER}
    other: list[tuple[str, dict]] = []

    for name, d in data.items():
        if is_tier1(d):
            tier1.append((name, d))
        else:
            b = d.get("bucket", "")
            if b in by_bucket:
                by_bucket[b].append((name, d))
            else:
                other.append((name, d))

    if tier1:
        lines.append("TIER 1 / ACTIONABLE")
        for name, d in tier1:
            lines.extend(pick_block(name, d))
        lines.append("")

    for bucket in BUCKET_ORDER:
        items = [x for x in by_bucket.get(bucket, []) if not is_tier1(x[1])]
        if not items:
            continue
        short_bucket = bucket.split("—")[-1].strip() if "—" in bucket else bucket
        lines.append(short_bucket.upper())
        for name, d in items:
            lines.extend(pick_block(name, d))
        lines.append("")

    if other:
        lines.append("OTHER")
        for name, d in other:
            lines.extend(pick_block(name, d))
        lines.append("")

    lines.append("CROWDED SKIP")
    lines.append("INDOTECH KAYNES ZENTEC MTAR APOLLO PARAS — do not chase")
    lines.append("")
    lines.append("PDF attached — full thesis + Screener metrics per pick.")

    return "\n".join(lines).strip()


def pick_block(name: str, d: dict) -> list[str]:
    ticker = short_name(name, d)
    verdict = d.get("verdict", "DIG DEEPER")
    thesis = d.get("thesis", "").split(".")[0].strip()  # first sentence for Telegram
    if len(thesis) > 120:
        thesis = thesis[:117] + "..."
    source = d.get("source") or SOURCE_FALLBACK.get(name, "")
    return [
        f"{ticker} — {verdict}",
        f"Thesis: {thesis}",
        f"Metrics: {fmt_metrics(d)}",
        f"Source: {source}" if source else "",
        "",
    ]


def inject_into_markdown(summary: str) -> None:
    if MD_PATH.exists():
        text = MD_PATH.read_text(encoding="utf-8")
    else:
        text = f"# Fintwitter Finds — {date.today().isoformat()}\n\n## New mentions\n\n"

    replacement = f"## Telegram summary\n\n{summary}\n"
    if re.search(r"^##\s*Telegram summary\s*$", text, re.MULTILINE | re.IGNORECASE):
        text = re.sub(
            r"^##\s*Telegram summary\s*\n.*?(?=^##\s|\Z)",
            replacement + "\n",
            text,
            count=1,
            flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
    else:
        text = re.sub(
            r"^(#\s+Fintwitter Finds[^\n]*\n)",
            r"\1\n" + replacement + "\n",
            text,
            count=1,
            flags=re.MULTILINE,
        )
        if "## Telegram summary" not in text:
            text = text.rstrip() + "\n\n" + replacement

    MD_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    data = json.loads(JSON_PATH.read_text())
    summary = build_blocks(data)
    inject_into_markdown(summary)
    print(f"Telegram summary: {len(summary)} chars -> {MD_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())