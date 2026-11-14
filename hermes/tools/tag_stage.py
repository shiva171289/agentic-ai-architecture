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
    parser.add_argument(
        "--at",
        default="origin/main",
        help="Commit to tag (default: origin/main — the published merge). "
             "Never rely on HEAD here: after an automated publish HEAD is usually "
             "still on the drafts branch, which is how stage-w05 first got tagged "
             "at a commit that never reached main.",
    )
    args = parser.parse_args()
    tag = f"stage-{args.week}"
    note = NOTES / f"stage-{args.week}.md"
    msg = note.read_text(encoding="utf-8") if note.is_file() else f"Acme stage {args.week}"

    subprocess.run(["git", "fetch", "--quiet", "origin", "main"], cwd=ROOT, check=False)

    already = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
        cwd=ROOT,
        capture_output=True,
    ).returncode == 0

    if already:
        print(f"Tag {tag} already exists locally — leaving it, will push if asked")
    else:
        rc = subprocess.run(
            ["git", "tag", "-a", tag, args.at, "-m", msg.split("\n")[0][:200]], cwd=ROOT
        ).returncode
        if rc != 0:
            return rc
        print(f"Created tag {tag} at {args.at}")

    if args.push:
        # Push even when the tag already existed locally: the old code returned early
        # on `git tag` failure, so a tag that existed only locally never reached origin.
        return subprocess.run(["git", "push", "origin", tag], cwd=ROOT).returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
