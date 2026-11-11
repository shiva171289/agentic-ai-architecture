"""Pending weekly approval state in ~/.hermes/weekly-approvals.json."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

STORE = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes") / "weekly-approvals.json"


def _load() -> dict:
    if not STORE.is_file():
        return {"pending": {}, "offset": 0}
    return json.loads(STORE.read_text(encoding="utf-8"))


def _save(data: dict) -> None:
    STORE.parent.mkdir(parents=True, exist_ok=True)
    STORE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def set_pending(week: str, gate: str, slug: str, *, extra: dict | None = None) -> None:
    data = _load()
    row = {
        "gate": gate,
        "slug": slug,
        "updated": datetime.now(timezone.utc).isoformat(),
    }
    if extra:
        row.update(extra)
    data["pending"][week] = row
    _save(data)


def clear_pending(week: str) -> None:
    data = _load()
    data["pending"].pop(week, None)
    _save(data)


def get_pending(week: str) -> dict | None:
    return _load().get("pending", {}).get(week)


def get_offset() -> int:
    return int(_load().get("offset") or 0)


def set_offset(offset: int) -> None:
    data = _load()
    data["offset"] = offset
    _save(data)
