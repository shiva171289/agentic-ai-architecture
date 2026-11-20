#!/usr/bin/env python3
"""
Send a plain Telegram message to the OWNER'S DM — never the news group.

Automation kept sending status notes to the news group because the sending code
picked the chat id itself and defaulted to `TELEGRAM_CHAT_ID`, which is the group.
Use this helper instead: it resolves the target internally, so a caller cannot
pick the wrong one.

Resolution order (same as approval_notify): TELEGRAM_APPROVAL_CHAT_ID, then
TELEGRAM_HOME_CHANNEL, then the first TELEGRAM_ALLOWED_USERS entry. TELEGRAM_CHAT_ID
is deliberately never consulted.

Usage:
  python3 hermes/tools/notify_dm.py --text "w06 pack pushed to drafts/w06"
  python3 hermes/tools/notify_dm.py --file /tmp/w06-checklist.txt
  echo "..." | python3 hermes/tools/notify_dm.py --stdin
  python3 hermes/tools/notify_dm.py --text "hi" --dry-run
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from approval_notify import approval_chat_id  # noqa: E402
from news_queue import load_env_file, telegram_bot_token  # noqa: E402
from telegram_api import send_message  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Message body")
    group.add_argument("--file", type=Path, help="Read the body from this file")
    group.add_argument("--stdin", action="store_true", help="Read the body from stdin")
    parser.add_argument("--dry-run", action="store_true",
                        help="Resolve the target and print the body; send nothing")
    args = parser.parse_args()

    if args.text is not None:
        body = args.text
    elif args.file is not None:
        if not args.file.is_file():
            print(f"No such file: {args.file}", file=sys.stderr)
            return 1
        body = args.file.read_text(encoding="utf-8")
    else:
        body = sys.stdin.read()

    body = body.strip()
    if not body:
        print("Refusing to send an empty message", file=sys.stderr)
        return 1

    load_env_file()
    chat_id = approval_chat_id()
    if not chat_id:
        print(
            "No DM target in ~/.hermes/.env "
            "(set TELEGRAM_APPROVAL_CHAT_ID or TELEGRAM_HOME_CHANNEL)",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        print(f"DRY RUN — would send {len(body)} chars to {chat_id} (DM)")
        print(body)
        return 0

    token = telegram_bot_token()
    if not token:
        print("Set TELEGRAM_BOT_TOKEN in ~/.hermes/.env", file=sys.stderr)
        return 1

    send_message(token, chat_id, body)
    print(f"Sent {len(body)} chars to {chat_id} (DM)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
