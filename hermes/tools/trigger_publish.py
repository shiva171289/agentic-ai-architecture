#!/usr/bin/env python3
"""
Dispatch GitHub Actions workflow to merge an approved draft branch to main.

Store on VPS only (never commit):
  GITHUB_PAT=ghp_...          # fine-grained or classic: repo contents + actions
  GITHUB_REPOSITORY=owner/repo  # optional; default shiva171289/agentic-ai-architecture

Usage:
  python3 hermes/tools/trigger_publish.py w01 w01-augmented-llm
  python3 hermes/tools/trigger_publish.py w01 w01-augmented-llm --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

WORKFLOW_FILE = "publish-approved-week.yml"
DEFAULT_REPO = "shiva171289/agentic-ai-architecture"


def dispatch(repo: str, token: str, draft_branch: str, week: str, pattern_dir: str, dry_run: bool) -> int:
    url = f"https://api.github.com/repos/{repo}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    body = {
        "ref": "main",
        "inputs": {
            "draft_branch": draft_branch,
            "week": week,
            "pattern_dir": pattern_dir,
        },
    }
    payload = json.dumps(body).encode("utf-8")
    if dry_run:
        print("DRY RUN", url, body)
        return 0

    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "Hermes-trigger-publish/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status not in (200, 204):
                print(f"Unexpected status: {resp.status}", file=sys.stderr)
                return 1
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        print(f"GitHub API error {exc.code}: {err_body}", file=sys.stderr)
        return 1
    print(f"Dispatched {WORKFLOW_FILE} for {draft_branch} → main (week {week})")
    print(f"Track Actions: https://github.com/{repo}/actions/workflows/{WORKFLOW_FILE}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Trigger publish-approved-week workflow")
    parser.add_argument("week", help="Week id, e.g. w01")
    parser.add_argument("pattern_dir", help="Pattern folder, e.g. w01-augmented-llm")
    parser.add_argument(
        "--draft-branch",
        default=None,
        help="Override draft branch (default drafts/<week>)",
    )
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPO))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_PAT") or os.environ.get("GH_TOKEN")
    if not token and not args.dry_run:
        print("Set GITHUB_PAT or GH_TOKEN in ~/.hermes/.env", file=sys.stderr)
        return 1

    draft_branch = args.draft_branch or f"drafts/{args.week}"
    return dispatch(
        args.repo,
        token or "",
        draft_branch,
        args.week,
        args.pattern_dir,
        args.dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())
