---
name: code-builder
description: Minimal runnable Python sample with mock LLM mode. Tier 0/1.
---

# CodeBuilder

Apply `_shared/ground-rules.md`.

## Inputs

- Approved `adr.md`
- [templates/code/README.md](../../templates/code/README.md) layout

## Tasks

Under `patterns/{week}-{slug}/code/`:

- `core/` — cloud-agnostic logic
- `aws/` — adapter stub (Bedrock-style interface)
- `azure/` — adapter stub (Foundry-style interface)
- `tests/` — pytest, runs without API keys
- `pyproject.toml` — uv compatible
- `README.md` — run instructions

Use **mock LLM** implementing a small protocol in `core/llm.py`.

## Quality

- Tests must pass: `uv run pytest`
- No secrets in repo

Final polish happens in Cursor on laptop.
