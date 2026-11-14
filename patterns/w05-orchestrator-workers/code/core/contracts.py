"""Shared contracts for the orchestrator-workers sample.

The orchestrator decides *what* to do (a plan); a worker does *how*
(bounded retrieval or tool call). Workers are addressed by capability,
never by a hard-coded name, so the pool can change without changing the
planner (see DeOrch in the ADR).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class Task:
    """One unit of delegated work, produced by the plan step."""

    kind: str
    instruction: str


@dataclass
class WorkerResult:
    """Structured worker output. Must be attributable to its task."""

    kind: str
    ok: bool
    detail: str

    def as_context(self) -> str:
        status = "ok" if self.ok else "unavailable"
        return f"{self.kind}: {self.detail} ({status})"


@dataclass
class Plan:
    """The orchestrator's decomposition. Inspectable, replayable."""

    tasks: list[Task] = field(default_factory=list)

    def kinds(self) -> list[str]:
        return [t.kind for t in self.tasks]


class Worker(Protocol):
    """A bounded unit of work selected by capability."""

    kind: str

    def run(self, task: Task) -> WorkerResult:  # pragma: no cover - protocol
        ...


class WorkerRegistry:
    """Maps a task kind to a worker instance.

    Planning is separated from worker selection: the orchestrator emits a
    *kind*, and the registry resolves it. New workers register here without
    touching the planner.
    """

    def __init__(self, workers: list[Worker] | None = None) -> None:
        self._by_kind: dict[str, Worker] = {}
        for w in workers or []:
            self.register(w)

    def register(self, worker: Worker) -> None:
        self._by_kind[worker.kind] = worker

    def kinds(self) -> set[str]:
        return set(self._by_kind)

    def knows(self, kind: str) -> bool:
        return kind in self._by_kind

    def select(self, kind: str) -> Worker:
        if kind not in self._by_kind:
            raise KeyError(f"no worker registered for kind {kind!r}")
        return self._by_kind[kind]
