#!/usr/bin/env python3
"""
Upsert harvested RSS items into ~/.hermes/news-queue/queue.json.

Usage:
  python3 hermes/tools/news_ingest.py
  python3 hermes/tools/news_ingest.py --harvest ~/.hermes/news-queue/harvest-latest.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from news_queue import (
    STATUS_PENDING,
    find_by_id,
    harvest_latest_path,
    load_queue,
    queue_lock,
    save_queue,
    utc_now_iso,
)

PREFERRED_TAGS = frozenset({"agents", "enterprise", "mcp", "cloud", "karpathy"})
AGENT_KEYWORDS = re.compile(
    r"\b(agent|agents|llm|rag|bedrock|mcp|orchestrat|tool\s*call|multimodal)\b",
    re.I,
)
HTML_INDEX_MARKER = "HTML index entry"


def load_harvest(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        return list(data.get("items") or [])
    if isinstance(data, list):
        return data
    return []


def should_ingest(row: dict) -> bool:
    summary = row.get("summary") or ""
    title = row.get("title") or ""
    tags = set(row.get("tags") or [])
    feed_id = row.get("feed_id") or ""

    if HTML_INDEX_MARKER in summary:
        if not AGENT_KEYWORDS.search(title):
            return False

    if feed_id == "aws-main-blog" and not AGENT_KEYWORDS.search(f"{title} {summary}"):
        return False

    if tags & PREFERRED_TAGS:
        return True
    if AGENT_KEYWORDS.search(f"{title} {summary}"):
        return True
    if "karpathy" in tags:
        return True
    return False


def cap_per_publisher(candidates: list[dict], max_per: int = 2) -> list[dict]:
    counts: dict[str, int] = defaultdict(int)
    kept: list[dict] = []
    for row in sorted(
        candidates,
        key=lambda r: r.get("published") or "",
        reverse=True,
    ):
        pub = row.get("publisher") or "Unknown"
        if counts[pub] >= max_per:
            continue
        counts[pub] += 1
        kept.append(row)
    return kept


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest harvest JSON into news queue")
    parser.add_argument(
        "--harvest",
        type=Path,
        default=None,
        help="Harvest JSON path (default: ~/.hermes/news-queue/harvest-latest.json)",
    )
    parser.add_argument("--max-per-publisher", type=int, default=2)
    args = parser.parse_args()

    harvest_path = args.harvest or harvest_latest_path()
    if not harvest_path.is_file():
        print(f"Harvest file missing: {harvest_path}", file=sys.stderr)
        return 1

    harvested = load_harvest(harvest_path)
    candidates = [row for row in harvested if should_ingest(row)]

    added = 0
    with queue_lock():
        items = load_queue()
        # De-duplicate BEFORE capping. Capping first lets items that are already in the
        # queue consume each publisher's budget (30 of 36 slots in a real 7-day run),
        # which starves the genuinely new items and makes the feed look empty.
        fresh = [
            row for row in candidates
            if row.get("id") and not find_by_id(items, row["id"])
        ]
        skipped = len(candidates) - len(fresh)
        for row in cap_per_publisher(fresh, args.max_per_publisher):
            items.append(
                {
                    "id": row.get("id"),
                    "title": row.get("title"),
                    "link": row.get("link"),
                    "publisher": row.get("publisher"),
                    "feed_id": row.get("feed_id"),
                    "published": row.get("published"),
                    "summary": row.get("summary") or "",
                    "image_url": row.get("image_url"),
                    "tags": row.get("tags") or [],
                    "status": STATUS_PENDING,
                    "headline": None,
                    "body": None,
                    "has_diagram": False,
                    "sent_at": None,
                    "ingested_at": utc_now_iso(),
                }
            )
            added += 1
        save_queue(items)

    print(f"Ingested {added} new items ({skipped} already in queue)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
