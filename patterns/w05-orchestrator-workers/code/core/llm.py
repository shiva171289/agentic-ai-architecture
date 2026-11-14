"""Deterministic mock LLM.

The same four call shapes the real orchestrator would make:

1. plan      - decompose the request into tasks (JSON)
2. worker    - a worker's bounded answer (JSON)
3. merge     - (no model call; deterministic in code)
4. synthesize- one answer over the merged context (text)

The mock is deterministic so tests and replay are stable: the same
question always yields the same plan.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

PLAN_MARKER = "TASK:PLAN"
WORKER_MARKER = "TASK:WORKER"
SYNTH_MARKER = "TASK:SYNTHESIZE"

ORDER_HINTS = ("order", "ord-", "ship", "delivery", "where is", "track")
POLICY_HINTS = ("policy", "return", "warranty", "refund", "window", "reset")


@dataclass
class LLMResponse:
    text: str


class LLM:
    def complete(self, system: str, user: str) -> LLMResponse:  # pragma: no cover
        raise NotImplementedError


def _needs_order(question: str) -> bool:
    q = question.lower()
    return any(h in q for h in ORDER_HINTS) or "ord-" in q


def _needs_policy(question: str) -> bool:
    q = question.lower()
    return any(h in q for h in POLICY_HINTS)


def _decompose(question: str) -> dict:
    parts: list[dict] = []
    if _needs_order(question):
        parts.append({"kind": "order_lookup", "instruction": "Find the order status."})
    if _needs_policy(question):
        parts.append({"kind": "policy_lookup", "instruction": "Find the matching policy."})
    if not parts:
        parts.append({"kind": "policy_lookup", "instruction": "Find the matching policy."})
    return {"tasks": parts}


class MockLLM(LLM):
    """Deterministic stand-in for a real model."""

    def complete(self, system: str, user: str) -> LLMResponse:
        if PLAN_MARKER in system:
            question = user.split("Question:", 1)[-1].strip()
            return LLMResponse(text=json.dumps(_decompose(question)))
        if WORKER_MARKER in system:
            kind = _field(user, "Kind")
            payload = json.loads(user.split("Task:", 1)[-1].strip() or "{}")
            return LLMResponse(text=_worker_answer(kind, payload.get("instruction", "")))
        if SYNTH_MARKER in system:
            context = user.split("Context:", 1)[-1].strip()
            return LLMResponse(
                text="Based on Acme policy and order Context: " + context
            )
        return LLMResponse(text="Please describe your Acme product issue.")


def _field(text: str, key: str) -> str:
    for line in text.splitlines():
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip()
    return ""


def _worker_answer(kind: str, instruction: str) -> str:
    if kind == "order_lookup":
        return json.dumps({"detail": "Order ORD-1001 shipped.", "ok": True})
    if kind == "policy_lookup":
        return json.dumps({"detail": "12-month warranty; 30-day return window.", "ok": True})
    return json.dumps({"detail": "no worker available", "ok": False})
