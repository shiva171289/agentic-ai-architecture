#!/usr/bin/env python3
"""
Deterministic Monday weekly-pack nudge (no LLM). For cron or manual runs.

Usage:
  python3 hermes/tools/weekly_reminder.py
  python3 hermes/tools/weekly_reminder.py --json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    tool = ROOT / "hermes" / "tools" / "calendar_week.py"
    proc = subprocess.run(
        [sys.executable, str(tool), "--next", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    info = json.loads(proc.stdout)
    corpus_note = (
        f"Corpus is {info['corpus_age_days']} days old."
        if info["corpus_age_days"] != "missing"
        else "Corpus file missing — run harvest_sources.py."
    )
    lines = [
        "Weekly pattern reminder",
        f"Publishing week: {info['week']} — {info['pattern']} ({info['slug']})",
        corpus_note,
        f"Telegram: brief {info['week']} {info['slug']}",
        f"After ADR approve: pack {info['week']}",
        "Cron does not run pack wNN automatically.",
    ]
    message = "\n".join(lines)
    if args.json:
        print(json.dumps({"message": message, **info}, indent=2))
        return
    print(message)


if __name__ == "__main__":
    main()
