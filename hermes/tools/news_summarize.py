#!/usr/bin/env python3
"""
Summarize pending queue items via OpenRouter (free model). One completion per item.

Usage:
  python3 hermes/tools/news_summarize.py
  python3 hermes/tools/news_summarize.py --limit 5
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

from news_queue import (  # noqa: E402
    STATUS_PENDING,
    STATUS_SUMMARIZED,
    load_env_file,
    load_queue,
    queue_lock,
    save_queue,
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "qwen/qwen3-235b-a22b:free"
FALLBACK_MODEL = "google/gemma-2-9b-it:free"

SYSTEM_PROMPT = """You write Inshorts-style news cards for enterprise AI readers.
Use ASD-STE100: short sentences, simple words, no hype.
Use ONLY facts from the user message. Do not invent product names or features.
Reply with a single JSON object only, no markdown fences:
{"headline": "12 words or fewer", "body": "80 words or fewer", "has_diagram": false}
Set has_diagram true only if the source text mentions a diagram, architecture figure, or chart."""


def parse_summary_json(text: str) -> dict | None:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return None
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    if not isinstance(data, dict):
        return None
    return data


def word_count(s: str) -> int:
    return len(re.findall(r"\S+", s or ""))


def clamp_fields(data: dict) -> dict:
    headline = (data.get("headline") or "").strip()
    body = (data.get("body") or "").strip()
    if word_count(headline) > 12:
        headline = " ".join(headline.split()[:12])
    if word_count(body) > 80:
        body = " ".join(body.split()[:80])
    has_diagram = bool(data.get("has_diagram"))
    return {"headline": headline, "body": body, "has_diagram": has_diagram}


def openrouter_complete(model: str, user_content: str, api_key: str) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.3,
        "max_tokens": 400,
    }
    req = urllib.request.Request(
        OPENROUTER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/shiva171289/agentic-ai-architecture",
            "X-Title": "Hermes News Inshorts",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    choices = body.get("choices") or []
    if not choices:
        raise RuntimeError(f"OpenRouter empty response: {body}")
    return (choices[0].get("message") or {}).get("content") or ""


def summarize_one(row: dict, api_key: str, models: list[str]) -> dict | None:
    title = row.get("title") or ""
    summary = row.get("summary") or ""
    link = row.get("link") or ""
    low_confidence = not summary or summary.startswith("(no summary")
    user_msg = (
        f"Title: {title}\n"
        f"URL: {link}\n"
        f"Feed excerpt:\n{summary if summary else '(empty — use title only)'}\n"
    )
    if low_confidence:
        user_msg += "\nNote: excerpt is thin; stay conservative and do not invent details.\n"

    last_err: Exception | None = None
    for model in models:
        for attempt in range(3):
            try:
                raw = openrouter_complete(model, user_msg, api_key)
                parsed = parse_summary_json(raw)
                if parsed:
                    return clamp_fields(parsed)
                last_err = RuntimeError(f"Invalid JSON from model: {raw[:200]}")
            except urllib.error.HTTPError as exc:
                last_err = exc
                if exc.code == 429:
                    time.sleep(2 ** attempt)
                    continue
                break
            except (urllib.error.URLError, TimeoutError, RuntimeError) as exc:
                last_err = exc
                time.sleep(1 + attempt)
        if last_err and isinstance(last_err, urllib.error.HTTPError) and last_err.code == 429:
            continue
    if last_err:
        print(f"  summarize failed {row.get('id')}: {last_err}", file=sys.stderr)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize pending news queue items")
    parser.add_argument("--limit", type=int, default=0, help="Max items to summarize (0 = all pending)")
    args = parser.parse_args()

    load_env_file()
    api_key = __import__("os").environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("OPENROUTER_API_KEY not set (~/.hermes/.env)", file=sys.stderr)
        return 1

    primary = __import__("os").environ.get("OPENROUTER_NEWS_MODEL", DEFAULT_MODEL)
    if primary.startswith("openrouter/"):
        primary = primary.removeprefix("openrouter/")
    models = [primary]
    fallback = __import__("os").environ.get("OPENROUTER_NEWS_MODEL_FALLBACK", FALLBACK_MODEL)
    if fallback.startswith("openrouter/"):
        fallback = fallback.removeprefix("openrouter/")
    if fallback not in models:
        models.append(fallback)

    done = 0
    failed = 0
    with queue_lock():
        items = load_queue()
        pending = [r for r in items if r.get("status") == STATUS_PENDING]
        if args.limit > 0:
            pending = pending[: args.limit]

        for row in pending:
            result = summarize_one(row, api_key, models)
            if not result:
                failed += 1
                continue
            row["headline"] = result["headline"]
            row["body"] = result["body"]
            row["has_diagram"] = result["has_diagram"]
            if row.get("image_url"):
                row["has_diagram"] = True
            row["status"] = STATUS_SUMMARIZED
            done += 1
            print(f"Summarized: {row.get('headline')}")

        save_queue(items)

    print(f"Done: {done} summarized, {failed} failed")
    return 0 if failed == 0 or done > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
