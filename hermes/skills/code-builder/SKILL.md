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

## Acme Support Platform (running use-case)

Also apply the same pattern to **`projects/acme-support/`** per [docs/roadmap/07-running-use-case.md](../../../docs/roadmap/07-running-use-case.md):

1. Read the week's **Acme stage** row in [content/calendar.md](../../../content/calendar.md).
2. Increment the existing codebase (do not rewrite from scratch).
3. Append one line to `projects/acme-support/STAGES.md` (`wNN — summary`).
4. Keep diff ~50–150 LOC; synthetic Acme data only.
5. Ensure `uv run pytest` passes in `projects/acme-support/`.

Week w09 (agent-or-workflow) may be docs-only in Acme (ADR + notebook, no code spike).

## Quality

- Tests must pass: `uv run pytest`
- No secrets in repo

Final polish happens in Cursor on laptop.
