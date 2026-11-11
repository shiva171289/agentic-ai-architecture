"""Minimal Telegram Bot API helpers (stdlib)."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any

API = "https://api.telegram.org/bot{token}/{method}"


def call(token: str, method: str, params: dict[str, Any]) -> dict:
    url = API.format(token=token, method=method)
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send_message(
    token: str,
    chat_id: str,
    text: str,
    *,
    reply_markup: dict | None = None,
    disable_preview: bool = False,
) -> dict:
    params: dict[str, Any] = {
        "chat_id": chat_id,
        "text": text[:4096],
        "disable_web_page_preview": disable_preview,
    }
    if reply_markup:
        params["reply_markup"] = json.dumps(reply_markup)
    return call(token, "sendMessage", params)


def answer_callback(token: str, callback_id: str, text: str = "") -> dict:
    return call(token, "answerCallbackQuery", {"callback_query_id": callback_id, "text": text[:200]})


def get_updates(token: str, offset: int | None, timeout: int = 0) -> list[dict]:
    params: dict[str, Any] = {"timeout": timeout}
    if offset is not None:
        params["offset"] = offset
    result = call(token, "getUpdates", params)
    return result.get("result") or []
