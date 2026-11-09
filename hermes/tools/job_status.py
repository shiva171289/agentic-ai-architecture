#!/usr/bin/env python3
"""
Report the health of every scheduled job on this host.

Facts are gathered deterministically (no LLM, no API call): the crontab is parsed,
each job's log file is stat'ed, and the news queue is read directly. Only with
--qwen is anything sent to a model, and that model is a free Tier-0 slug.

Usage:
  python3 hermes/tools/job_status.py
  python3 hermes/tools/job_status.py --qwen
  python3 hermes/tools/job_status.py --qwen --json

Env:
  OPENROUTER_STATUS_MODEL  default qwen/qwen3-235b-a22b:free
  OPENROUTER_API_KEY       required only for --qwen
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERMES_HOME = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
ENV_FILE = HERMES_HOME / ".env"
QUEUE_FILE = HERMES_HOME / "news-queue" / "queue.json"
DEFAULT_STATUS_MODEL = "qwen/qwen3-235b-a22b:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

LOG_RE = re.compile(r">>\s*(\S+\.log)")


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    if not ENV_FILE.is_file():
        return values
    for line in ENV_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def cron_lines() -> list[str]:
    try:
        out = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError) as exc:
        return [f"# crontab unavailable: {exc}"]
    if out.returncode != 0:
        return [f"# crontab -l failed: {out.stderr.strip() or out.returncode}"]
    return [ln for ln in out.stdout.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]


def describe_job(line: str, now: datetime.datetime) -> dict:
    fields = line.split(None, 5)
    schedule = " ".join(fields[:5]) if len(fields) >= 5 else "?"
    command = fields[5] if len(fields) > 5 else ""
    log_match = LOG_RE.search(command)
    log_path = log_match.group(1) if log_match else None
    script = ""
    for token in command.split():
        if token.endswith((".py", ".sh")) or token == "hermes":
            script = Path(token).name
            break

    job = {
        "schedule": schedule,
        "script": script or (Path(command.split()[0]).name if command else "?"),
        "name": Path(log_path).stem if log_path else (script or "?"),
        "log": log_path,
        "last_run": None,
        "age_minutes": None,
        "last_lines": [],
    }
    if log_path:
        path = Path(os.path.expanduser(log_path))
        if path.is_file():
            mtime = datetime.datetime.fromtimestamp(path.stat().st_mtime, datetime.timezone.utc)
            job["last_run"] = mtime.isoformat(timespec="seconds")
            job["age_minutes"] = round((now - mtime).total_seconds() / 60)
            try:
                tail = path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                tail = []
            job["last_lines"] = [ln for ln in tail[-3:] if ln.strip()]
        else:
            job["last_run"] = "log missing"
    return job


def queue_summary() -> dict:
    if not QUEUE_FILE.is_file():
        return {"error": "queue.json missing"}
    try:
        data = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {"error": str(exc)}
    items = data.get("items") if isinstance(data, dict) else data
    items = items or []
    ready = [i for i in items if i.get("status") == "summarized" and not i.get("sent_at")]
    return {
        "total": len(items),
        "ready_unsent": len(ready),
        "sent": sum(1 for i in items if i.get("sent_at")),
        "pending": sum(1 for i in items if i.get("status") == "pending"),
        "file_mtime": datetime.datetime.fromtimestamp(
            QUEUE_FILE.stat().st_mtime, datetime.timezone.utc
        ).isoformat(timespec="seconds"),
    }


def collect() -> dict:
    now = datetime.datetime.now(datetime.timezone.utc)
    return {
        "now_utc": now.isoformat(timespec="seconds"),
        "cron_jobs": [describe_job(ln, now) for ln in cron_lines()],
        "news_queue": queue_summary(),
    }


def render(report: dict) -> str:
    out = [f"Job status @ {report['now_utc']}", ""]
    for job in report["cron_jobs"]:
        age = job["age_minutes"]
        age_txt = "never" if age is None else (f"{age} min ago" if age < 180 else f"{age // 60} h ago")
        out.append(f"- {job['name']:<22} cron[{job['schedule']}]  last log write: {age_txt}")
        for ln in job["last_lines"]:
            out.append(f"    {ln[:110]}")
    q = report["news_queue"]
    out.append("")
    if "error" in q:
        out.append(f"news queue: {q['error']}")
    else:
        out.append(
            f"news queue: ready={q['ready_unsent']} pending={q['pending']} "
            f"sent={q['sent']} total={q['total']} (written {q['file_mtime']})"
        )
    return "\n".join(out)


def ask_qwen(facts: str, model: str, api_key: str) -> str:
    prompt = (
        "You are a VPS operations assistant. Below are raw facts about scheduled jobs "
        "and a news queue. Write at most 5 short lines. State which jobs look healthy, "
        "which look broken or stalled, and the single most useful next action. Do not "
        "invent facts that are not in the data. Plain text, no markdown headers.\n\n"
        f"{facts}"
    )
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }
    req = urllib.request.Request(
        OPENROUTER_URL,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body["choices"][0]["message"]["content"].strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Report scheduled-job health")
    parser.add_argument("--qwen", action="store_true",
                        help="Add a short summary from the free Tier-0 model")
    parser.add_argument("--json", action="store_true", help="Print raw facts as JSON")
    args = parser.parse_args()

    report = collect()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render(report))

    if not args.qwen:
        return 0

    env = load_env()
    api_key = env.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    model = env.get("OPENROUTER_STATUS_MODEL") or os.environ.get(
        "OPENROUTER_STATUS_MODEL", DEFAULT_STATUS_MODEL
    )
    if not api_key:
        print("\n--qwen needs OPENROUTER_API_KEY in ~/.hermes/.env", file=sys.stderr)
        return 1
    try:
        summary = ask_qwen(render(report), model, api_key)
    except (urllib.error.URLError, KeyError, ValueError) as exc:
        print(f"\nqwen summary failed ({model}): {exc}", file=sys.stderr)
        return 1
    print(f"\n--- {model} ---")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
