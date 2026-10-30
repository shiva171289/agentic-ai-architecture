# Acme Support Platform (running use-case)

Fictional **Acme Manufacturing** customer support system. One increment per weekly pattern; tags `stage-wNN`, releases `v1`–`v4`.

- Storyline: [docs/roadmap/07-running-use-case.md](../../docs/roadmap/07-running-use-case.md)
- Stage log: [STAGES.md](STAGES.md)
- Split at W13 → `acme-agentic-support` @ `v1`

## Run tests

```bash
cd projects/acme-support
uv sync --extra dev
uv run pytest
```

## Run demo (stage w01)

```bash
uv run python -m core.demo
```

## Layout

- `core/` — cloud-agnostic support logic (grows weekly)
- `data/` — synthetic policies and fixtures (no real customer data)
- `tests/` — pytest, mock LLM only

No API keys required.
