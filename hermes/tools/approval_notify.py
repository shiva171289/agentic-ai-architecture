#!/usr/bin/env python3
"""
Send Telegram approval cards with inline buttons for weekly gates.

Usage:
  python3 hermes/tools/approval_notify.py --gate adr --week w05 --slug orchestrator-workers
  python3 hermes/tools/approval_notify.py --gate publish --week w05 --slug orchestrator-workers
  python3 hermes/tools/approval_notify.py --gate adr --next
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from approval_store import set_pending  # noqa: E402
from news_queue import load_env_file, telegram_bot_token, telegram_chat_id  # noqa: E402
from telegram_api import send_message  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REPO = "shiva171289/agentic-ai-architecture"
DEFAULT_PAGES = "https://shiva171289.github.io/agentic-ai-architecture"


def _read_excerpt(path: Path, words: int = 80) -> str:
    if not path.is_file():
        return "(file not on disk yet — check drafts branch)"
    body = path.read_text(encoding="utf-8")
    if body.startswith("---"):
        parts = body.split("---", 2)
        body = parts[2] if len(parts) > 2 else body
    tokens = body.split()
    return " ".join(tokens[:words]) + ("…" if len(tokens) > words else "")


def _run_calendar_next() -> tuple[str, str]:
    proc = subprocess.run(
        [sys.executable, str(_TOOLS / "calendar_week.py"), "--next", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    import json

    info = json.loads(proc.stdout)
    return info["week"], info["slug"]


def build_adr_message(week: str, slug: str) -> str:
    adr = ROOT / "patterns" / f"{week}-{slug}" / "adr.md"
    brief = ROOT / "patterns" / f"{week}-{slug}" / "brief.md"
    branch = f"drafts/{week}"
    lines = [
        f"Weekly ADR gate — {week} {slug}",
        "",
        _read_excerpt(adr, 100) if adr.is_file() else _read_excerpt(brief, 100),
        "",
        f"ADR: https://github.com/{REPO}/blob/{branch}/patterns/{week}-{slug}/adr.md",
        f"Branch: https://github.com/{REPO}/tree/{branch}",
        "",
        "Approve to run full pack (Qwen-heavy draft steps). Reject to revise.",
        "",
        "Or via Hermes: adr approve " + week,
    ]
    return "\n".join(lines)


def build_publish_message(week: str, slug: str) -> str:
    blog = ROOT / "patterns" / f"{week}-{slug}" / "blog.md"
    lines = [
        f"Publish gate — {week} {slug}",
        "",
        _read_excerpt(blog, 120),
        "",
        f"Pack: https://github.com/{REPO}/tree/drafts/{week}",
        f"Approve runs CI + PR merge → GitHub Pages.",
        f"Preview after merge: {DEFAULT_PAGES}/blog/{week}-{slug}/",
        "",
        "Or via Hermes: publish approve " + week,
    ]
    return "\n".join(lines)


def keyboard(gate: str, week: str) -> dict:
    prefix = "adr" if gate == "adr" else "pub"
    return {
        "inline_keyboard": [
            [
                {"text": "Approve", "callback_data": f"{prefix}:ok:{week}"},
                {"text": "Reject", "callback_data": f"{prefix}:no:{week}"},
            ]
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", choices=("adr", "publish"), required=True)
    parser.add_argument("--week", help="wNN")
    parser.add_argument("--slug", help="pattern slug")
    parser.add_argument("--next", action="store_true", help="Use next week from publish-progress")
    args = parser.parse_args()

    week = args.week
    slug = args.slug
    if args.next or not week:
        week, slug = _run_calendar_next()
    if not slug:
        raise SystemExit("Pass --slug or use --next")

    load_env_file()
    token = telegram_bot_token()
    chat_id = telegram_chat_id()
    if not token or not chat_id:
        print("Set TELEGRAM_BOT_TOKEN and chat id in ~/.hermes/.env", file=sys.stderr)
        return 1

    if args.gate == "adr":
        text = build_adr_message(week, slug)
    else:
        text = build_publish_message(week, slug)

    send_message(token, chat_id, text, reply_markup=keyboard(args.gate, week))
    set_pending(week, args.gate, slug)
    print(f"Sent {args.gate} approval for {week} {slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
