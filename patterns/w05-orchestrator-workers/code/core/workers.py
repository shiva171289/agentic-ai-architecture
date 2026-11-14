"""Worker implementations and a registry factory."""

from __future__ import annotations

import json

from core.contracts import Task, WorkerResult, WorkerRegistry
from core.llm import WORKER_MARKER, LLM

WORKER_PROTOCOL = (
    f"{WORKER_MARKER}\n"
    "You are a bounded Acme support worker. Perform the task and return "
    "JSON with fields 'detail' (string) and 'ok' (boolean). Do not invent data."
)


class LookupWorker:
    """A bounded retrieval/tool worker. One call, one structured result."""

    def __init__(self, kind: str, llm: LLM) -> None:
        self.kind = kind
        self._llm = llm

    def run(self, task: Task) -> WorkerResult:
        user = f"Kind: {self.kind}\nTask: {json.dumps({'instruction': task.instruction})}"
        raw = self._llm.complete(WORKER_PROTOCOL, user).text
        try:
            data = json.loads(raw)
        except (ValueError, TypeError):
            # A plausible-but-wrong worker output is the new failure class.
            return WorkerResult(kind=self.kind, ok=False, detail="unparseable worker output")
        return WorkerResult(
            kind=self.kind,
            ok=bool(data.get("ok", False)),
            detail=str(data.get("detail", "")),
        )


def default_registry(llm: LLM) -> WorkerRegistry:
    """The w05 worker pool: one policy lookup, one order lookup."""

    return WorkerRegistry(
        [
            LookupWorker("policy_lookup", llm),
            LookupWorker("order_lookup", llm),
        ]
    )
