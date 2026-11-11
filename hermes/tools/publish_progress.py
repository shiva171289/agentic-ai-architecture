#!/usr/bin/env python3
"""Read/update content/publish-progress.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROGRESS_FILE = ROOT / "content" / "publish-progress.json"


def load() -> dict:
    if not PROGRESS_FILE.is_file():
        return {"last_published_week": "w00", "last_merged_to_main_week": "w00"}
    return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    PROGRESS_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def week_num(wid: str) -> int:
    m = re.match(r"w(\d{2})", wid)
    if not m:
        raise ValueError(wid)
    return int(m.group(1))


def format_week(n: int) -> str:
    return f"w{n:02d}"


def next_pack_week() -> str:
    data = load()
    last = data.get("last_published_week") or "w00"
    return format_week(week_num(last) + 1)
