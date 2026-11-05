#!/usr/bin/env python3
"""Persistent news queue on the VPS (~/.hermes/news-queue/). Stdlib only."""

from __future__ import annotations

import json
import os
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

DEFAULT_QUEUE_DIR = Path(os.path.expanduser("~/.hermes/news-queue"))
QUEUE_FILE = "queue.json"
HARVEST_LATEST = "harvest-latest.json"
LOCK_FILE = "queue.lock"

STATUS_PENDING = "pending"
STATUS_SUMMARIZED = "summarized"


def queue_dir() -> Path:
    env = os.environ.get("HERMES_NEWS_QUEUE_DIR")
    if env:
        return Path(env).expanduser()
    return DEFAULT_QUEUE_DIR


def queue_path() -> Path:
    return queue_dir() / QUEUE_FILE


def harvest_latest_path() -> Path:
    return queue_dir() / HARVEST_LATEST


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def queue_lock(timeout: float = 30.0) -> Iterator[None]:
    lock_path = queue_dir() / LOCK_FILE
    queue_dir().mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout
    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Could not acquire queue lock: {lock_path}")
            time.sleep(0.1)
    try:
        yield
    finally:
        try:
            lock_path.unlink(missing_ok=True)
        except OSError:
            pass


def load_queue() -> list[dict[str, Any]]:
    path = queue_path()
    if not path.is_file():
        return []
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"]
    return []


def save_queue(items: list[dict[str, Any]]) -> None:
    queue_dir().mkdir(parents=True, exist_ok=True)
    path = queue_path()
    payload = json.dumps(items, indent=2, ensure_ascii=False)
    fd, tmp = tempfile.mkstemp(dir=str(queue_dir()), suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def find_by_id(items: list[dict[str, Any]], item_id: str) -> dict[str, Any] | None:
    for row in items:
        if row.get("id") == item_id:
            return row
    return None


def load_env_file(path: Path | None = None) -> None:
    """Load KEY=VALUE lines from ~/.hermes/.env into os.environ (no override)."""
    env_path = path or Path(os.path.expanduser("~/.hermes/.env"))
    if not env_path.is_file():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value
