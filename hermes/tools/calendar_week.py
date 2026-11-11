#!/usr/bin/env python3
"""
Resolve the current publishing pattern week from content/calendar.md.

Program week 1 starts on PROGRAM_START (first week pilot). Override with --week wNN.

Usage:
  python3 hermes/tools/calendar_week.py
  python3 hermes/tools/calendar_week.py --json
  python3 hermes/tools/calendar_week.py --week w05
  python3 hermes/tools/calendar_week.py --brief-prompt
  python3 hermes/tools/calendar_week.py --next --brief-prompt
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CALENDAR = ROOT / "content" / "calendar.md"
PROGRAM_START = dt.date(2026, 10, 27)

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(_TOOLS))


def load_calendar_rows() -> list[dict[str, str]]:
    text = CALENDAR.read_text(encoding="utf-8")
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.startswith("| w"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4:
            continue
        week = parts[1]
        slug = parts[2]
        pattern = parts[3]
        if not re.match(r"w\d{2}", week):
            continue
        rows.append({"week": week, "slug": slug, "pattern": pattern})
    return rows


def week_from_date(today: dt.date | None = None) -> int:
    today = today or dt.date.today()
    delta = (today - PROGRAM_START).days
    if delta < 0:
        return 1
    return min(52, delta // 7 + 1)


def resolve(
    week_id: str | None = None,
    today: dt.date | None = None,
    *,
    use_publish_queue: bool = False,
) -> dict[str, str]:
    from publish_progress import load, next_pack_week

    rows = load_calendar_rows()
    by_week = {r["week"]: r for r in rows}
    if week_id:
        if week_id not in by_week:
            raise SystemExit(f"Unknown week {week_id!r} in calendar")
        row = by_week[week_id]
        wid = week_id
    elif use_publish_queue:
        wid = next_pack_week()
        if wid not in by_week:
            raise SystemExit(f"Calendar has no row for {wid}")
        row = by_week[wid]
        prog = load()
        row = {
            **row,
            "last_published_week": prog.get("last_published_week"),
            "last_merged_to_main_week": prog.get("last_merged_to_main_week"),
            "mode": "next_publish",
        }
    else:
        n = week_from_date(today)
        wid = f"w{n:02d}"
        if wid not in by_week:
            raise SystemExit(f"Calendar has no row for {wid}")
        row = by_week[wid]
    corpus = ROOT / "content" / "source-corpus" / "latest.md"
    corpus_age_days: int | None = None
    if corpus.exists():
        mtime = dt.datetime.fromtimestamp(corpus.stat().st_mtime, tz=dt.timezone.utc)
        corpus_age_days = (dt.datetime.now(tz=dt.timezone.utc) - mtime).days
    if not use_publish_queue and not week_id:
        wid = f"w{week_from_date(today):02d}"
    return {
        **row,
        "program_week_number": wid,
        "corpus_age_days": str(corpus_age_days) if corpus_age_days is not None else "missing",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week", metavar="wNN", help="Force a calendar week id")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument(
        "--brief-prompt",
        action="store_true",
        help="One-line instruction for ResearchScout cron",
    )
    parser.add_argument(
        "--next",
        action="store_true",
        help="Next week after content/publish-progress.json (automation default)",
    )
    args = parser.parse_args()
    if args.week and args.next:
        raise SystemExit("Use either --week or --next")
    if args.week:
        info = resolve(args.week)
    elif args.next:
        info = resolve(None, use_publish_queue=True)
    else:
        info = resolve(None)
    if args.brief_prompt:
        mode = info.get("mode", "calendar_date")
        print(
            f"Run research-scout for {info['week']} {info['slug']} ({mode}): "
            f"write patterns/{info['week']}-{info['slug']}/brief.md from content/calendar.md "
            f"and content/source-corpus/latest.md (corpus age: {info['corpus_age_days']} days). "
            f"Use Qwen / Tier 0 per docs/setup/model-tiers-qwen.md."
        )
        return
    if args.json:
        print(json.dumps(info, indent=2))
        return
    print(f"{info['week']} {info['slug']}")


if __name__ == "__main__":
    main()
