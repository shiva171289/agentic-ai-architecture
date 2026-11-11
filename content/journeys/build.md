# Build AI systems (this repository)

This hub’s flagship **Build 201** path is the [52-week pattern calendar](../calendar.md): one pattern per week, AWS and Azure mapping notes, and a growing [Acme Support](../../projects/acme-support/) codebase.

## How to follow

1. Read [Start Here](../start-here.md).
2. Open the calendar row for your week.
3. Read the blog post under `patterns/wNN-slug/blog.md`.
4. Run pattern sample tests, then Acme tests:

```bash
cd patterns/w01-augmented-llm/code && uv sync --extra dev && uv run pytest
cd ../../../projects/acme-support && uv sync --extra dev && uv run pytest
```

## Levels

| Level | Calendar weeks | Outcome |
|-------|----------------|---------|
| Foundation | w01–w14 | Single agent: RAG, tools, memory |
| Practitioner | w15–w27 | Multi-agent flows and sagas |
| Production | w28–w39 | Security, evals, observability |
| Architect | w41–w52 | ERP integration and fleet governance |

## Topics

Browse cross-cutting ladders: [content/topics/README.md](../topics/README.md).

## System-design spine

Each post notes which layers apply. See [framework/five-layer-spine.md](../../framework/five-layer-spine.md).
