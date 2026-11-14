"""w05 — orchestrator-workers for the Acme support flow.

The orchestrator decomposes a request into independent parts at runtime and
delegates each part to a lookup worker. Workers are addressed by capability;
the deterministic spine runs them in order and merges their results before
the existing answer chain runs.

Kept intentionally small: the w04 stage fetched policy + order for every
request. Here the fan-out width is a runtime decision, capped by
``MAX_WORKERS``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from core.llm import LLM, LLMResponse
from core.support import answer_for_intent, classify_intent, fetch_order_snippet

MAX_WORKERS = 3


@dataclass(frozen=True)
class Task:
    kind: str
    instruction: str


@dataclass
class WorkerResult:
    kind: str
    detail: str

    def as_context(self) -> str:
        return f"{self.kind}: {self.detail}"


PolicyLookup = Callable[[str], str]
OrderLookup = Callable[[str], str]
Worker = Callable[[Task], WorkerResult]


def policy_worker(question: str, lookup: PolicyLookup) -> Worker:
    def run(_task: Task) -> WorkerResult:
        return WorkerResult("policy_lookup", lookup(question))

    return run


def order_worker(question: str, lookup: OrderLookup) -> Worker:
    def run(_task: Task) -> WorkerResult:
        return WorkerResult("order_lookup", lookup(question))

    return run


def decompose(question: str) -> list[Task]:
    """Runtime decomposition — which parts does this request need?

    In production a model emits this plan; here a small deterministic rule
    stands in so tests and replay are stable.
    """

    q = question.lower()
    tasks: list[Task] = []
    if any(h in q for h in ("order", "ord-", "ship", "track")):
        tasks.append(Task("order_lookup", "Find the order status."))
    if any(h in q for h in ("policy", "return", "warranty", "refund", "window", "reset")):
        tasks.append(Task("policy_lookup", "Find the matching policy."))
    if not tasks:
        tasks.append(Task("policy_lookup", "Find the matching policy."))
    return tasks[:MAX_WORKERS]


def merge(results: list[WorkerResult]) -> str:
    return "\n".join(r.as_context() for r in results)


def answer_with_orchestrator(
    llm: LLM,
    question: str,
    *,
    policy_lookup: PolicyLookup,
    order_lookup: OrderLookup,
    allow_tools: bool = False,
) -> LLMResponse:
    """w05 — decompose, delegate to workers, merge, then answer."""

    plan = decompose(question)
    workers: dict[str, Worker] = {
        "policy_lookup": policy_worker(question, policy_lookup),
        "order_lookup": order_worker(question, order_lookup),
    }
    results = [workers[t.kind](t) for t in plan]
    context = merge(results)
    intent = classify_intent(question)
    response = answer_for_intent(llm, question, intent, context)
    if response.tool_call and not allow_tools:
        return LLMResponse(text="Tool blocked by policy.", tool_call=None)
    return response


def default_orchestrator(
    llm: LLM, question: str, *, allow_tools: bool = False
) -> LLMResponse:
    """Convenience entry point wiring the Acme lookups."""

    from core.support import retrieve_policy_snippet

    return answer_with_orchestrator(
        llm,
        question,
        policy_lookup=retrieve_policy_snippet,
        order_lookup=fetch_order_snippet,
        allow_tools=allow_tools,
    )
