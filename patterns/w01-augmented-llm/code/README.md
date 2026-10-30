# w01 — Augmented LLM sample

Minimal **cloud-agnostic** orchestrator with mock LLM and in-memory retrieval.

## Run tests

```bash
cd patterns/w01-augmented-llm/code
uv sync --extra dev
uv run pytest
```

## Run demo

```bash
uv run python -m core.demo
```

## Layout

- `core/` — orchestration logic
- `aws/`, `azure/` — adapter stubs for Bedrock / Foundry wiring

No API keys required for tests.
