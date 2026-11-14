"""The deterministic workflow spine.

Ordered nodes, each executed with a per-task context, and an optional
checkpoint dict so a re-run reuses the plan and skips finished work
(deterministic replay). This is the model-free part of the pattern: only
planning and synthesis touch the model.
"""

from __future__ import annotations

from typing import Callable

from core.contracts import Plan, Task, WorkerRegistry, WorkerResult


def run_workflow(
    plan: Plan,
    registry: WorkerRegistry,
    *,
    checkpoint: dict | None = None,
    runner: Callable[[Task, WorkerRegistry], WorkerResult] | None = None,
) -> tuple[list[WorkerResult], dict]:
    """Execute every task in plan order, honouring a checkpoint.

    Returns the results (in plan order) and the updated checkpoint.
    """

    if runner is None:
        runner = _default_runner
    state = checkpoint if checkpoint is not None else {}
    done: dict[str, WorkerResult] = state.get("results", {})
    results: list[WorkerResult] = []
    for task in plan.tasks:
        key = task.kind
        if key in done:
            results.append(done[key])
            continue
        result = runner(task, registry)
        done[key] = result
        results.append(result)
    state["results"] = done
    return results, state


def _default_runner(task: Task, registry: WorkerRegistry) -> WorkerResult:
    return registry.select(task.kind).run(task)


def merge(results: list[WorkerResult]) -> str:
    """Combine attributable worker results into one context string."""

    return "\n".join(r.as_context() for r in results)


def verify(plan: Plan, results: list[WorkerResult]) -> tuple[bool, list[str]]:
    """Orchestration-level check: every planned part must be satisfied.

    This is the VMAO-style verification signal — it lives at the
    orchestration layer, not inside any single worker.
    """

    by_kind = {r.kind: r for r in results}
    missing = [k for k in plan.kinds() if k not in by_kind]
    failed = [k for k in plan.kinds() if k in by_kind and not by_kind[k].ok]
    return (not missing and not failed), missing + failed
