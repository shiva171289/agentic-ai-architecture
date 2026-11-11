#!/usr/bin/env python3
"""
Create git tag stage-wNN after a week is merged to main.

Usage:
  python3 hermes/tools/tag_stage.py w04
  python3 hermes/tools/tag_stage.py w04 --push
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTES = ROOT / ".github" / "release-notes"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("week", help="wNN")
    parser.add_argument("--push", action="store_true", help="git push origin tag")
    parser.add_argument("--no-push", action="store_true", help="Annotated tag only")
    args = parser.parse_args()
    tag = f"stage-{args.week}"
    note = NOTES / f"stage-{args.week}.md"
    msg = note.read_text(encoding="utf-8") if note.is_file() else f"Acme stage {args.week}"
    cmd = ["git", "tag", "-a", tag, "-m", msg.split("\n")[0][:200]]
    rc = subprocess.run(cmd, cwd=ROOT).returncode
    if rc != 0:
        return rc
    print(f"Created tag {tag}")
    if args.push:
        return subprocess.run(["git", "push", "origin", tag], cwd=ROOT).returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
