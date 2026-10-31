# Acme Support — stage changelog

Git tags mark each weekly increment on this hub repo: **`stage-wNN`** after merge, plus **`v1`** (w13), **`v2`** (w26), **`v3`** (w39), **`v4`** (w46) at quarter releases.

## Checkout a stage

```bash
git fetch --tags
git checkout stage-w01   # example: Week 1 — augmented LLM
cd projects/acme-support && uv sync --extra dev && uv run pytest
```

Return to latest work: `git checkout main`.

## Released tags

| Tag | Week | Pattern | Summary |
|-----|------|---------|---------|
| `stage-w01` | w01 | augmented-llm | Keyword retrieval over synthetic policy docs; FAQ answers with a fixed prompt contract (mock LLM, no API keys) |

Future rows append here as each `stage-wNN` is tagged.

## Week log

| Week | Summary |
|------|---------|
| w01 | Augmented LLM: keyword retrieval over synthetic policy docs + prompt contract for FAQ answers |
