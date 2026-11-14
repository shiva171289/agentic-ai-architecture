# w05 orchestrator-workers

The orchestrator decides **what** to do at runtime; each worker does **how**.

```bash
# with uv (on the laptop)
uv sync --extra dev && uv run pytest

# without uv (bundled interpreter)
python3 -m pytest -q
```

No API keys are needed — the sample uses a deterministic mock LLM (`core/llm.py`).

`core/contracts.py` holds the shared contracts (`Task`, `WorkerResult`, `Plan`,
`WorkerRegistry`). `core/plan.py` is the deterministic spine with checkpointing.
`core/pattern.py` is the orchestrator (plan → delegate → merge → verify → synthesize).
