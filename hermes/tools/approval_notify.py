#!/usr/bin/env python3
"""
Send Telegram approval cards for the weekly gates.

Cards are text-only and name the exact reply command. They deliberately carry NO
inline buttons: the gateway's CallbackQueryHandler dispatches on known
callback_data prefixes (ea:, sc:, cl:, mp:, ...) and silently drops anything
else, and the separate telegram_poll_approvals.py poller cannot work beside the
gateway because Telegram allows one getUpdates consumer per bot. Buttons on these
cards were a dead control — 1,464 consecutive HTTP 409s in the poller log and not
one callback ever handled.

Usage:
  python3 hermes/tools/approval_notify.py --gate adr --week w06 --slug evaluator-optimizer
  python3 hermes/tools/approval_notify.py --gate publish --week w06 --slug evaluator-optimizer
  python3 hermes/tools/approval_notify.py --gate adr --next
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from approval_store import set_pending  # noqa: E402
from news_queue import load_env_file, telegram_bot_token  # noqa: E402
from telegram_api import send_message  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REPO = "shiva171289/agentic-ai-architecture"
DEFAULT_PAGES = "https://shiva171289.github.io/agentic-ai-architecture"


def approval_chat_id() -> str:
    """Resolve where gate cards go: the owner's DM, never the news chat.

    news_queue.telegram_chat_id() prefers TELEGRAM_CHAT_ID, and that is set to the
    news GROUP — which is exactly why gate cards were arriving in the group. Gate
    approvals are owner-only, so resolve an explicit DM target and skip
    TELEGRAM_CHAT_ID entirely.
    """
    for key in ("TELEGRAM_APPROVAL_CHAT_ID", "TELEGRAM_HOME_CHANNEL"):
        val = (os.environ.get(key) or "").strip()
        if val:
            return val
    allowed = (os.environ.get("TELEGRAM_ALLOWED_USERS") or "").strip()
    if allowed:
        first = allowed.split(",")[0].strip()
        if first:
            return first
    return ""


def _read_excerpt(path: Path, words: int, ref: str | None = None) -> str | None:
    """Read an excerpt, preferring a git ref over the working tree.

    The pipeline sends gate cards after the pack agent has left the repo checked
    out on drafts/wNN, and it invokes this file as a subprocess — so the tools
    that run are whatever that branch contains. Looking the content up through a
    ref keeps the excerpt correct no matter which branch is checked out.
    """
    body = ""
    if ref:
        rel = path.relative_to(ROOT).as_posix()
        proc = subprocess.run(
            ["git", "show", f"{ref}:{rel}"], cwd=ROOT, capture_output=True, text=True
        )
        if proc.returncode == 0:
            body = proc.stdout
    if not body and path.is_file():
        body = path.read_text(encoding="utf-8")
    if not body:
        return None
    if body.startswith("---"):
        parts = body.split("---", 2)
        body = parts[2] if len(parts) > 2 else body
    tokens = body.split()
    return " ".join(tokens[:words]) + ("…" if len(tokens) > words else "")


def _pack_excerpt(week: str, slug: str, filenames: tuple[str, ...], words: int) -> str:
    """Excerpt for wNN, read from drafts/wNN so it does not depend on the checkout."""
    ref = f"origin/drafts/{week}"
    for name in filenames:
        text = _read_excerpt(ROOT / "patterns" / f"{week}-{slug}" / name, words, ref=ref)
        if text:
            return text
    return f"(no pack files found for {week}-{slug} — check drafts/{week})"


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
        _pack_excerpt(week, slug, ("adr.md", "brief.md"), 100),
        "",
        f"ADR: https://github.com/{REPO}/blob/{branch}/patterns/{week}-{slug}/adr.md",
        f"Branch: https://github.com/{REPO}/tree/{branch}",
        "",
        "To APPROVE and run the full pack, reply:",
        f"adr approve {week}",
        "",
        f"To REJECT and revise, reply: adr reject {week}: <your notes>",
    ]
    return "\n".join(lines)


def build_publish_message(week: str, slug: str) -> str:
    blog = ROOT / "patterns" / f"{week}-{slug}" / "blog.md"
    lines = [
        f"Publish gate — {week} {slug}",
        "",
        _pack_excerpt(week, slug, ("blog.md",), 120),
        "",
        f"Pack: https://github.com/{REPO}/tree/drafts/{week}",
        "Approving runs CI, merges the PR, and deploys GitHub Pages.",
        f"Preview after merge: {DEFAULT_PAGES}/blog/{week}-{slug}/",
        "",
        "To PUBLISH, reply:",
        f"publish approve {week}",
    ]
    return "\n".join(lines)


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
    chat_id = approval_chat_id()
    if not token or not chat_id:
        print(
            "Set TELEGRAM_BOT_TOKEN and a DM target in ~/.hermes/.env "
            "(TELEGRAM_APPROVAL_CHAT_ID or TELEGRAM_HOME_CHANNEL)",
            file=sys.stderr,
        )
        return 1

    if args.gate == "adr":
        text = build_adr_message(week, slug)
    else:
        text = build_publish_message(week, slug)

    send_message(token, chat_id, text)
    set_pending(week, args.gate, slug)
    print(f"Sent {args.gate} approval for {week} {slug} to {chat_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
