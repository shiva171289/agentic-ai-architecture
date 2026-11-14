#!/usr/bin/env python3
"""
Medium weekly automation: ADR draft → Telegram approve → pack → publish approve.

Uses Hermes CLI for LLM steps. Uses Qwen-friendly models per docs/setup/model-tiers-qwen.md.

Usage:
  python3 hermes/tools/weekly_pipeline.py friday-adr
  python3 hermes/tools/weekly_pipeline.py friday-adr --week w05
  python3 hermes/tools/weekly_pipeline.py on-adr-approved --week w05 --slug orchestrator-workers
  python3 hermes/tools/weekly_pipeline.py on-publish-approved --week w05 --slug orchestrator-workers
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from approval_store import clear_pending, set_pending  # noqa: E402
from publish_progress import save, load, format_week, week_num  # noqa: E402


def run(cmd: list[str], *, cwd: Path | None = None) -> int:
    print("+", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd or ROOT, check=False).returncode


def hermes_oneshot(prompt: str, skill: str) -> int:
    hermes = os.environ.get("HERMES_BIN", "hermes")
    return run(
        [hermes, "chat", "-q", prompt, "-s", skill, "--oneshot"],
        cwd=ROOT,
    )


def week_info(week: str | None) -> dict:
    cmd = [sys.executable, str(_TOOLS / "calendar_week.py"), "--json"]
    if week:
        cmd.extend(["--week", week])
    else:
        cmd.append("--next")
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(proc.stdout)


def ensure_branch(week: str) -> None:
    """Make sure drafts/wNN exists and is checked out before the LLM steps write files."""
    branch = f"drafts/{week}"
    exists = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", branch],
        cwd=ROOT,
        capture_output=True,
    ).returncode == 0
    run(["git", "checkout", branch] if exists else ["git", "checkout", "-b", branch], cwd=ROOT)


def commit_and_push_pack(week: str, slug: str) -> int:
    """Commit the generated ADR/brief and push drafts/wNN.

    The Telegram gate card links to `drafts/wNN` on GitHub, so the branch and the
    ADR must exist on origin BEFORE approval_notify runs. Skipping this is why the
    w05 card pointed at a branch that did not exist and an uncommitted ADR.
    """
    pattern_dir = f"patterns/{week}-{slug}"
    run(["git", "add", pattern_dir], cwd=ROOT)
    staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet"], cwd=ROOT, capture_output=True
    ).returncode != 0
    if staged and run(["git", "commit", "-m", f"{week}: ADR for {slug}"], cwd=ROOT) != 0:
        return 1
    if run(["git", "push", "-u", "origin", f"drafts/{week}"], cwd=ROOT) != 0:
        print(
            f"push of drafts/{week} failed — not sending a gate card with dead links",
            file=sys.stderr,
        )
        return 1
    return 0


def friday_adr(week: str | None) -> int:
    info = week_info(week)
    w, slug = info["week"], info["slug"]
    ensure_branch(w)
    scout_prompt = (
        f"Run research-scout for {w} {slug}. "
        f"Write patterns/{w}-{slug}/brief.md. Use Tier 0 / Qwen where configured."
    )
    if hermes_oneshot(scout_prompt, "research-scout") != 0:
        return 1
    arch_prompt = (
        f"Run pattern-architect for {w} {slug}. "
        f"Write patterns/{w}-{slug}/adr.md only. Stop before code/blog."
    )
    if hermes_oneshot(arch_prompt, "pattern-architect") != 0:
        return 1
    if commit_and_push_pack(w, slug) != 0:
        return 1
    return run(
        [
            sys.executable,
            str(_TOOLS / "approval_notify.py"),
            "--gate",
            "adr",
            "--week",
            w,
            "--slug",
            slug,
        ]
    )


def on_adr_approved(week: str, slug: str) -> int:
    pack_prompt = (
        f"ADR for {week} is approved via Telegram. "
        f"Run weekly-pack: complete cloud-mapper, code-builder, diagram, blog-writer, "
        f"linkedin-editor, reviewer-critic for {week} {slug}. Push drafts/{week}. "
        f"Prefer OPENROUTER_NEWS_MODEL / Qwen for Tier 0 draft steps."
    )
    rc = hermes_oneshot(pack_prompt, "weekly-pack")
    if rc != 0:
        return rc
    clear_pending(week)
    set_pending(week, "publish", slug)
    return run(
        [
            sys.executable,
            str(_TOOLS / "approval_notify.py"),
            "--gate",
            "publish",
            "--week",
            week,
            "--slug",
            slug,
        ]
    )


def record_publish(week: str) -> int:
    """Record the publish on the drafts branch so the merge carries it to main.

    `main` is ruleset-protected, so the VPS cannot push this file after the merge.
    Writing it only in the working tree leaves main on the old week, and
    publish_progress.next_pack_week() then re-targets a week that already
    published. Commit it to drafts/wNN BEFORE trigger_publish runs.
    """
    data = load()
    data["last_merged_to_main_week"] = week
    data["last_published_week"] = week
    save(data)
    run(["git", "add", "content/publish-progress.json"], cwd=ROOT)
    subprocess.run(
        ["git", "commit", "-m", f"{week}: record publish in publish-progress.json"],
        cwd=ROOT,
        capture_output=True,
    )  # rc 1 == nothing to commit, which is fine
    return run(["git", "push", "-u", "origin", f"drafts/{week}"], cwd=ROOT)


def on_publish_approved(week: str, slug: str) -> int:
    pattern_dir = f"{week}-{slug}"
    ensure_branch(week)
    if record_publish(week) != 0:
        return 1
    rc = run([sys.executable, str(_TOOLS / "trigger_publish.py"), week, pattern_dir])
    if rc == 0:
        clear_pending(week)
        # --push: the stage tag is part of publishing. tag_stage now targets origin/main
        # explicitly instead of HEAD, which after this flow is still the drafts branch.
        run([sys.executable, str(_TOOLS / "tag_stage.py"), week, "--push"])
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_fri = sub.add_parser("friday-adr", help="Scout + ADR + Telegram ADR card")
    p_fri.add_argument("--week")
    p_ok = sub.add_parser("on-adr-approved")
    p_ok.add_argument("--week", required=True)
    p_ok.add_argument("--slug", required=True)
    p_pub = sub.add_parser("on-publish-approved")
    p_pub.add_argument("--week", required=True)
    p_pub.add_argument("--slug", required=True)
    args = parser.parse_args()

    if args.cmd == "friday-adr":
        return friday_adr(args.week)
    if args.cmd == "on-adr-approved":
        return on_adr_approved(args.week, args.slug)
    if args.cmd == "on-publish-approved":
        return on_publish_approved(args.week, args.slug)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
