# Enterprise Agentic AI Architecture Framework (v0.1)

Twelve pillars for designing production agent systems. Each weekly pattern maps to one or more pillars.

| # | Pillar | Question it answers |
|---|--------|---------------------|
| 1 | Business use cases | Is an agent justified vs automation/rules? |
| 2 | Agent design | Single vs multi-agent; control flow |
| 3 | Context architecture | Windows, summarization, memory tiers |
| 4 | Data architecture | Sources, freshness, lineage |
| 5 | Tool architecture | MCP, APIs, least privilege |
| 6 | Identity & authorization | Who is the agent acting as? |
| 7 | Security | Prompt injection, exfiltration, sandboxing |
| 8 | Governance | Policy, registry, approvals |
| 9 | Evaluation | Offline/online metrics, golden sets |
| 10 | Observability | Traces, logs, cost attribution |
| 11 | Cost management | Model routing, caching, budgets |
| 12 | Deployment & operations | CI/CD, rollback, DR |

## How to use

1. For each initiative, score maturity 1–5 per pillar.
2. Block production if security, identity, or eval pillars < 3.
3. Tie weekly patterns to weak pillars in your self-assessment.

## v0.1 scope

Conceptual framework only. Checklists and ADR templates live in `patterns/` and [production-readiness-checklist.md](production-readiness-checklist.md).

## Disclaimer

Learning material only. See [docs/roadmap/00-ground-rules.md](../docs/roadmap/00-ground-rules.md).
