#!/usr/bin/env python3
"""
Send Inshorts card(s) per run to Telegram (cron or manual).

Sends one card when the ready queue fits the daily pulse budget; sends more per
run when summarized items would not clear within one day.

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
import time
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
    telegram_bot_token,
    telegram_chat_id,
    utc_now_iso,
)

TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"
CAPTION_MAX = 1024
DEFAULT_RUNS_PER_DAY = 12
DEFAULT_MAX_PER_RUN = 10
SEND_GAP_SEC = 1.0


def ready_pool(items: list[dict]) -> list[dict]:
    return [
        r
        for r in items
        if r.get("status") == STATUS_SUMMARIZED
        and not r.get("sent_at")
        and r.get("headline")
    ]


def pulse_batch_size(
    ready_count: int,
    *,
    runs_per_day: int = DEFAULT_RUNS_PER_DAY,
    min_per_run: int = 1,
    max_per_run: int = DEFAULT_MAX_PER_RUN,
) -> int:
    if ready_count <= 0:
        return 0
    if ready_count <= runs_per_day:
        return min_per_run
    needed = (ready_count + runs_per_day - 1) // runs_per_day
    return min(max_per_run, max(min_per_run, needed))


def int_env(name: str, default: int) -> int:
    raw = (os.environ.get(name) or "").strip()
    if not raw:
        return default
    try:
        return max(1, int(raw))
    except ValueError:
        return default


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


def pick_candidates(items: list[dict], count: int) -> list[dict]:
    pool = ready_pool(items)
    if not pool or count <= 0:
        return []
    n = min(count, len(pool))
    return random.sample(pool, n)


def main() -> int:
    parser = argparse.ArgumentParser(description="Send Inshorts card(s) to Telegram")
    parser.add_argument("--dry-run", action="store_true", help="Print choice without sending")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Same as default send (for manual news today hook)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help="Cards to send this run (default: auto from queue depth)",
    )
    args = parser.parse_args()
    _ = args.force

    load_env_file()
    runs_per_day = int_env("HERMES_NEWS_RUNS_PER_DAY", DEFAULT_RUNS_PER_DAY)
    max_per_run = int_env("HERMES_NEWS_MAX_PER_RUN", DEFAULT_MAX_PER_RUN)

    token = telegram_bot_token()
    chat_id = telegram_chat_id()
    if not args.dry_run and (not token or not chat_id):
        print(
            "Set TELEGRAM_BOT_TOKEN and a chat id in ~/.hermes/.env "
            "(TELEGRAM_CHAT_ID, TELEGRAM_HOME_CHANNEL, or TELEGRAM_ALLOWED_USERS)",
            file=sys.stderr,
        )
        return 1

    with queue_lock():
        items = load_queue()
        pool = ready_pool(items)
        if not pool:
            print("No summarized unsent items in queue")
            return 0

        batch = (
            args.count
            if args.count is not None
            else pulse_batch_size(
                len(pool), runs_per_day=runs_per_day, max_per_run=max_per_run
            )
        )
        rows = pick_candidates(items, batch)
        if not rows:
            print("No summarized unsent items in queue")
            return 0

        if args.dry_run:
            for row in rows:
                print(format_message(row))
                print("---")
            return 0

    sent_headlines: list[str] = []
    for i, row in enumerate(rows):
        try:
            send_card(token, chat_id, row)
        except (urllib.error.URLError, RuntimeError) as exc:
            print(f"Send failed: {exc}", file=sys.stderr)
            return 1
        with queue_lock():
            items = load_queue()
            for r in items:
                if r.get("id") == row.get("id"):
                    r["sent_at"] = utc_now_iso()
                    break
            save_queue(items)
        sent_headlines.append(str(row.get("headline")))
        if i + 1 < len(rows):
            time.sleep(SEND_GAP_SEC)

    if len(sent_headlines) == 1:
        print(f"Sent: {sent_headlines[0]}")
    else:
        print(f"Sent {len(sent_headlines)} cards (batch size {len(rows)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
