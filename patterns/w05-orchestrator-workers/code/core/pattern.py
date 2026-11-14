"""Orchestrator-workers: decompose at runtime, delegate, merge, answer."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Callable

from core.contracts import Plan, Task, WorkerRegistry, WorkerResult
from core.llm import PLAN_MARKER, SYNTH_MARKER, LLM
from core.plan import merge, run_workflow, verify
from core.workers import default_registry

DEFAULT_MAX_WORKERS = 3

PLAN_PROTOCOL = (
    f"{PLAN_MARKER}\n"
    "You are an Acme support orchestrator. Decompose the request into the "
    "smallest set of independent tasks needed. Return JSON: "
    '{"tasks": [{"kind": "<worker kind>", "instruction": "<what to return>"}]}. '
    "Do not invent worker kinds."
)

SYNTH_PROTOCOL = (
    f"{SYNTH_MARKER}\n"
    "You are Acme Manufacturing tier-1 support. Answer using Context only. "
    "Do not invent policy. Be concise."
)


@dataclass
class Orchestration:
    """Full, inspectable record of one orchestrator-workers run."""

    plan: Plan
    results: list[WorkerResult] = field(default_factory=list)
    complete: bool = False
    problems: list[str] = field(default_factory=list)
    answer: str = ""
    checkpoint: dict = field(default_factory=dict)


def make_plan(llm: LLM, question: str, registry: WorkerRegistry, *,
              max_workers: int = DEFAULT_MAX_WORKERS) -> Plan:
    """Ask the model to decompose, then bound the fan-out.

    Planning is separated from worker selection: the model emits kinds, the
    registry decides what those kinds resolve to.
    """

    raw = llm.complete(PLAN_PROTOCOL, f"Question: {question}").text
    try:
        data = json.loads(raw)
    except (ValueError, TypeError):
        data = {"tasks": []}
    tasks = [
        Task(kind=str(t["kind"]), instruction=str(t.get("instruction", "")))
        for t in data.get("tasks", [])
        if isinstance(t, dict) and t.get("kind") in registry.kinds()
    ]
    # Cap the fan-out: never spawn more workers than the budget allows.
    return Plan(tasks=tasks[:max_workers])


def run_orchestrator(
    llm: LLM,
    question: str,
    *,
    registry: WorkerRegistry | None = None,
    max_workers: int = DEFAULT_MAX_WORKERS,
    checkpoint: dict | None = None,
    runner: Callable[[Task, WorkerRegistry], WorkerResult] | None = None,
) -> Orchestration:
    """Plan -> delegate -> merge -> verify -> synthesize."""

    registry = registry or default_registry(llm)
    plan = make_plan(llm, question, registry, max_workers=max_workers)
    results, state = run_workflow(plan, registry, checkpoint=checkpoint, runner=runner)
    complete, problems = verify(plan, results)
    context = merge(results)
    answer = llm.complete(SYNTH_PROTOCOL, f"Question: {question}\nContext: {context}").text
    return Orchestration(
        plan=plan,
        results=results,
        complete=complete,
        problems=problems,
        answer=answer,
        checkpoint=state,
    )
