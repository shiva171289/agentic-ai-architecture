## Week 1 snapshot (Acme Support Platform)

Fictional **Acme Manufacturing** customer support at the first weekly increment: keyword retrieval over synthetic policy docs, FAQ answers with a fixed prompt contract, **mock LLM only** (no cloud API keys).

### Try it

```bash
git fetch --tags
git checkout stage-w01
cd projects/acme-support && uv sync --extra dev && uv run pytest
```

Demo from `projects/acme-support/`:

```bash
uv run python -m core.demo
```

### Learn

- Blog: [Week 1 — Augmented LLM](https://shiva171289.github.io/agentic-ai-architecture/blog/w01-augmented-llm/)
- Primer: [Start Here](https://shiva171289.github.io/agentic-ai-architecture/start-here/)
- Pattern sample at this tag: [patterns/w01-augmented-llm/code](https://github.com/shiva171289/agentic-ai-architecture/tree/stage-w01/patterns/w01-augmented-llm/code)
- Acme code at this tag: [projects/acme-support](https://github.com/shiva171289/agentic-ai-architecture/tree/stage-w01/projects/acme-support)
- Changelog: [STAGES.md](https://github.com/shiva171289/agentic-ai-architecture/blob/stage-w01/projects/acme-support/STAGES.md)

### Tag convention

Weekly Acme snapshots: `stage-wNN`. Quarter releases: `v1` (w13), `v2` (w26), `v3` (w39), `v4` (w46).

Learning material only; synthetic data; not employer representations.
