#!/usr/bin/env python3
"""
Drop sent queue rows older than 3 days and old dated corpus files on the VPS clone.

Usage:
  python3 hermes/tools/news_cleanup.py
  python3 hermes/tools/news_cleanup.py --retention-days 3
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from news_queue import load_queue, queue_lock, save_queue  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS_DIR = REPO_ROOT / "content" / "source-corpus"
DATE_FILE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")


def parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Retention cleanup for news queue and corpus")
    parser.add_argument("--retention-days", type=int, default=3)
    args = parser.parse_args()

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.retention_days)
    removed_queue = 0

    with queue_lock():
        items = load_queue()
        kept: list[dict] = []
        for row in items:
            sent = parse_iso(row.get("sent_at"))
            if sent and sent < cutoff:
                removed_queue += 1
                continue
            kept.append(row)
        save_queue(kept)

    removed_corpus = 0
    if CORPUS_DIR.is_dir():
        for path in CORPUS_DIR.iterdir():
            if path.name == "latest.md":
                continue
            match = DATE_FILE.match(path.name)
            if not match:
                continue
            try:
                file_day = datetime.strptime(match.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            if file_day < cutoff:
                path.unlink(missing_ok=True)
                removed_corpus += 1

    print(f"Removed {removed_queue} queue rows and {removed_corpus} corpus files (>{args.retention_days}d)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
