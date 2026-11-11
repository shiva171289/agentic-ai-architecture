#!/usr/bin/env python3
"""
Poll Telegram for inline approval callbacks (run every 1-2 minutes from cron).

Callback data: adr:ok:w05 | adr:no:w05 | pub:ok:w05 | pub:no:w05
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from approval_store import clear_pending, get_pending, get_offset, set_offset  # noqa: E402
from news_queue import load_env_file, telegram_bot_token  # noqa: E402
from telegram_api import answer_callback, get_updates, send_message  # noqa: E402


def allowed_user_ids() -> set[str]:
    raw = (__import__("os").environ.get("TELEGRAM_ALLOWED_USERS") or "").strip()
    return {x.strip() for x in raw.split(",") if x.strip()}


def handle_callback(data: str, user_id: str) -> None:
    parts = data.split(":")
    if len(parts) != 3:
        return
    gate, action, week = parts
    if user_id not in allowed_user_ids():
        return
    pending = get_pending(week)
    if not pending:
        return
    slug = pending.get("slug", "")
    if action == "no":
        clear_pending(week)
        load_env_file()
        token = telegram_bot_token()
        chat = user_id
        send_message(token, chat, f"Rejected {gate} for {week}. Send revise notes via Hermes chat.")
        return
    if gate == "adr" and action == "ok":
        subprocess.run(
            [
                sys.executable,
                str(_TOOLS / "weekly_pipeline.py"),
                "on-adr-approved",
                "--week",
                week,
                "--slug",
                slug,
            ],
            check=False,
        )
        return
    if gate == "pub" and action == "ok":
        subprocess.run(
            [
                sys.executable,
                str(_TOOLS / "weekly_pipeline.py"),
                "on-publish-approved",
                "--week",
                week,
                "--slug",
                slug,
            ],
            check=False,
        )
        return


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true", help="Single poll (for cron)")
    args = parser.parse_args()

    load_env_file()
    token = telegram_bot_token()
    if not token:
        print("TELEGRAM_BOT_TOKEN missing", file=sys.stderr)
        return 1
    if not allowed_user_ids():
        print("TELEGRAM_ALLOWED_USERS missing", file=sys.stderr)
        return 1

    offset = get_offset()
    updates = get_updates(token, offset if offset else None, timeout=0)
    max_id = offset
    for upd in updates:
        uid = upd.get("update_id", 0)
        max_id = max(max_id, uid + 1)
        cb = upd.get("callback_query")
        if not cb:
            continue
        from_user = cb.get("from") or {}
        user_id = str(from_user.get("id", ""))
        data = cb.get("data") or ""
        answer_callback(token, cb.get("id", ""), "Processing…")
        handle_callback(data, user_id)
    if max_id > offset:
        set_offset(max_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
