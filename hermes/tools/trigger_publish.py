#!/usr/bin/env python3
"""
Publish an approved weekly pack: run the CI gate, then merge via pull request.

GitHub's `main` ruleset requires changes to arrive through a pull request, so a
direct push from Actions is rejected with GH013. This script:

  1. dispatches the publish-gate workflow (tests the draft branch in CI)
  2. waits for that run and stops on failure
  3. opens a pull request `drafts/wNN` -> `main`
  4. merges that pull request

Steps 3 and 4 need a token with Pull requests write. Store it on the ops host
only (never commit):
  GITHUB_PAT=github_pat_...     # Actions, Contents, Pull requests: read+write
  GITHUB_REPOSITORY=owner/repo  # optional; default shiva171289/agentic-ai-architecture

Usage:
  python3 hermes/tools/trigger_publish.py w01 w01-augmented-llm
  python3 hermes/tools/trigger_publish.py w01 w01-augmented-llm --dry-run
  python3 hermes/tools/trigger_publish.py w01 w01-augmented-llm --skip-ci
  python3 hermes/tools/trigger_publish.py w01 w01-augmented-llm --timeout 1200
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

API = "https://api.github.com"
WORKFLOW_FILE = "publish-approved-week.yml"
DEFAULT_REPO = "shiva171289/agentic-ai-architecture"


class ApiError(RuntimeError):
    def __init__(self, status: int, message: str) -> None:
        super().__init__(f"GitHub API {status}: {message}")
        self.status = status
        self.message = message


def call(repo: str, token: str, method: str, path: str, body: dict | None = None) -> dict:
    url = path if path.startswith("http") else f"{API}/repos/{repo}{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "Hermes-trigger-publish/2.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(detail).get("message", detail)
        except ValueError:
            pass
        raise ApiError(exc.code, detail)


def _epoch(iso: str) -> float:
    return datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def dispatch_ci(repo: str, token: str, draft_branch: str, week: str, pattern_dir: str) -> None:
    call(repo, token, "POST", f"/actions/workflows/{WORKFLOW_FILE}/dispatches", {
        "ref": "main",
        "inputs": {"draft_branch": draft_branch, "week": week, "pattern_dir": pattern_dir},
    })


def wait_for_ci(repo: str, token: str, since_epoch: float, timeout: int) -> dict | None:
    run = None
    deadline = time.time() + 60
    while run is None and time.time() < deadline:
        runs = call(repo, token, "GET",
                    f"/actions/workflows/{WORKFLOW_FILE}/runs?event=workflow_dispatch&per_page=10")
        for candidate in runs.get("workflow_runs", []):
            if _epoch(candidate["created_at"]) >= since_epoch - 60:
                run = candidate
                break
        if run is None:
            time.sleep(3)
    if run is None:
        return None

    print(f"CI run started: {run['html_url']}")
    deadline = time.time() + timeout
    while run["status"] != "completed" and time.time() < deadline:
        time.sleep(10)
        run = call(repo, token, "GET", f"/actions/runs/{run['id']}")
    return run


def ensure_pull_request(repo: str, token: str, draft_branch: str, week: str, pattern_dir: str) -> dict:
    owner = repo.split("/")[0]
    existing = call(repo, token, "GET", f"/pulls?state=open&head={owner}:{draft_branch}&base=main")
    if existing:
        return existing[0]

    return call(repo, token, "POST", "/pulls", {
        "title": f"Publish {week} ({pattern_dir.removeprefix(week + '-')})",
        "head": draft_branch,
        "base": "main",
        "body": (
            f"Automated publish of the approved `{week}` pattern pack.\n\n"
            f"- Pattern folder: `patterns/{pattern_dir}/`\n"
            f"- CI: publish-gate run passed\n\n"
            f"Opened by `hermes/tools/trigger_publish.py` after Telegram approval."
        ),
    })


def merge_pull_request(repo: str, token: str, number: int, week: str) -> dict:
    deadline = time.time() + 90
    while time.time() < deadline:
        pr = call(repo, token, "GET", f"/pulls/{number}")
        if pr.get("mergeable") is True:
            break
        if pr.get("mergeable") is False:
            raise ApiError(409, f"pull request #{number} is not mergeable (state={pr.get('mergeable_state')})")
        time.sleep(5)
    else:
        raise ApiError(408, f"pull request #{number} mergeability unknown after 90s")

    return call(repo, token, "PUT", f"/pulls/{number}/merge", {
        "commit_title": f"Publish {week} after Telegram approval",
        "merge_method": "merge",
    })


def main() -> int:
    parser = argparse.ArgumentParser(description="Test and publish an approved weekly pack")
    parser.add_argument("week", help="Week id, e.g. w01")
    parser.add_argument("pattern_dir", help="Pattern folder, e.g. w01-augmented-llm")
    parser.add_argument("--draft-branch", default=None,
                        help="Override draft branch (default drafts/<week>)")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPO))
    parser.add_argument("--timeout", type=int, default=900, help="Seconds to wait for CI (default 900)")
    parser.add_argument("--skip-ci", action="store_true", help="Skip the CI gate; go straight to the PR")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan; make no changes")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_PAT") or os.environ.get("GH_TOKEN") or ""
    if not token and not args.dry_run:
        print("Set GITHUB_PAT or GH_TOKEN in ~/.hermes/.env", file=sys.stderr)
        return 1

    draft_branch = args.draft_branch or f"drafts/{args.week}"
    repo = args.repo

    if args.dry_run:
        print("DRY RUN")
        print(f"  repo         : {repo}")
        print(f"  draft branch : {draft_branch}")
        print(f"  pattern dir  : patterns/{args.pattern_dir}/")
        print(f"  step 1       : dispatch {WORKFLOW_FILE}")
        print(f"  step 2       : wait for the run (timeout {args.timeout}s)")
        print(f"  step 3       : open pull request {draft_branch} -> main")
        print(f"  step 4       : merge that pull request")
        print(f"  pages path   : /blog/{args.pattern_dir}/")
        return 0

    try:
        if args.skip_ci:
            print("Skipping the CI gate (--skip-ci)")
        else:
            since = time.time()
            dispatch_ci(repo, token, draft_branch, args.week, args.pattern_dir)
            print(f"Dispatched {WORKFLOW_FILE} for {draft_branch}")
            run = wait_for_ci(repo, token, since, args.timeout)
            if run is None:
                print("Could not find the CI run. Check Actions manually.", file=sys.stderr)
                return 1
            if run["status"] != "completed":
                print(f"CI still running after {args.timeout}s: {run['html_url']}", file=sys.stderr)
                return 1
            if run["conclusion"] != "success":
                print(f"CI gate failed: {run['conclusion']} — {run['html_url']}", file=sys.stderr)
                return 1
            print(f"CI gate passed: {run['html_url']}")

        pr = ensure_pull_request(repo, token, draft_branch, args.week, args.pattern_dir)
        print(f"Pull request #{pr['number']}: {pr['html_url']}")
        if pr.get("state") == "open":
            result = merge_pull_request(repo, token, pr["number"], args.week)
            print(f"Merged: {result.get('message')} sha={result.get('sha')}")
        else:
            print(f"Pull request already {pr.get('state')}; nothing to merge")

        print(f"\nPages path: /blog/{args.pattern_dir}/")
        print(f"Actions: https://github.com/{repo}/actions/workflows/{WORKFLOW_FILE}")
        return 0
    except ApiError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
