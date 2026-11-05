#!/usr/bin/env python3
"""Print news queue counts (for manual checks / Telegram hook)."""

from __future__ import annotations

import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from news_queue import STATUS_PENDING, STATUS_SUMMARIZED, load_queue  # noqa: E402


def main() -> int:
    items = load_queue()
    pending = sum(1 for r in items if r.get("status") == STATUS_PENDING)
    summarized = sum(
        1 for r in items if r.get("status") == STATUS_SUMMARIZED and not r.get("sent_at")
    )
    sent = sum(1 for r in items if r.get("sent_at"))
    print(f"pending={pending} ready={summarized} sent={sent} total={len(items)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
