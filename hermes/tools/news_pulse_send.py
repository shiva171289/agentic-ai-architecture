#!/usr/bin/env python3
"""
Send one Inshorts card per run to Telegram (hourly cron or manual).

Usage:
  python3 hermes/tools/news_pulse_send.py
  python3 hermes/tools/news_pulse_send.py --dry-run
  python3 hermes/tools/news_pulse_send.py --force
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from news_queue import (  # noqa: E402
    STATUS_SUMMARIZED,
    load_env_file,
    load_queue,
    queue_lock,
    save_queue,
    utc_now_iso,
)

TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"
CAPTION_MAX = 1024


def format_message(row: dict) -> str:
    headline = row.get("headline") or row.get("title") or "News"
    body = row.get("body") or ""
    link = row.get("link") or ""
    lines = [f"📰 {headline}", "", body, "", f"🔗 {link}"]
    text = "\n".join(lines).strip()
    if len(text) > CAPTION_MAX:
        budget = CAPTION_MAX - len(link) - 20
        body_short = body[: max(0, budget)]
        text = f"📰 {headline}\n\n{body_short}\n\n🔗 {link}"
    return text[:CAPTION_MAX]


def telegram_request(token: str, method: str, params: dict) -> dict:
    url = TELEGRAM_API.format(token=token, method=method)
    if method in ("sendMessage", "sendPhoto"):
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
    else:
        req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send_card(token: str, chat_id: str, row: dict) -> None:
    text = format_message(row)
    image_url = row.get("image_url")
    if image_url:
        result = telegram_request(
            token,
            "sendPhoto",
            {"chat_id": chat_id, "photo": image_url, "caption": text},
        )
    else:
        result = telegram_request(
            token,
            "sendMessage",
            {"chat_id": chat_id, "text": text, "disable_web_page_preview": "false"},
        )
    if not result.get("ok"):
        raise RuntimeError(f"Telegram error: {result}")


def pick_candidate(items: list[dict]) -> dict | None:
    pool = [
        r
        for r in items
        if r.get("status") == STATUS_SUMMARIZED
        and not r.get("sent_at")
        and r.get("headline")
    ]
    if not pool:
        return None
    return random.choice(pool)


def main() -> int:
    parser = argparse.ArgumentParser(description="Send one Inshorts card to Telegram")
    parser.add_argument("--dry-run", action="store_true", help="Print choice without sending")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Same as default send (for manual news today hook)",
    )
    args = parser.parse_args()
    _ = args.force

    load_env_file()
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not args.dry_run and (not token or not chat_id):
        print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in ~/.hermes/.env", file=sys.stderr)
        return 1

    with queue_lock():
        items = load_queue()
        row = pick_candidate(items)
        if not row:
            print("No summarized unsent items in queue")
            return 0

        if args.dry_run:
            print(format_message(row))
            return 0

        row["sent_at"] = utc_now_iso()
        save_queue(items)

    try:
        send_card(token, chat_id, row)
    except (urllib.error.URLError, RuntimeError) as exc:
        with queue_lock():
            items = load_queue()
            for r in items:
                if r.get("id") == row.get("id"):
                    r["sent_at"] = None
                    break
            save_queue(items)
        print(f"Send failed: {exc}", file=sys.stderr)
        return 1

    print(f"Sent: {row.get('headline')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
