---
title: "Orchestrator-workers: let the request choose the fan-out"
description: "A model-driven orchestrator decomposes a request at runtime, delegates to workers, and merges the results — after parallelization is not enough."
pubDate: 2026-11-28
patternWeek: w05
level: Foundation
acmeStage: w05
spineLayers: "2"
---

Every pattern so far fixes the shape of the work at design time. Orchestrator-workers is the first where a model chooses it: a lead agent splits the request, delegates to workers, and merges the results.

## Prerequisites

[w01 augmented LLM](/blog/w01-augmented-llm/) · [w02 prompt chaining](/blog/w02-prompt-chaining/) · [w03 routing](/blog/w03-routing/) · [w04 parallelization](/blog/w04-parallelization/).

## Context

Parallelization (w04) fans out a fixed set of calls — policy retrieval and order snippet — for every request. That fails on *"where is my order, and what is the return window?"*: two independent parts, a count that varies per request. A fixed chain over-fetches or under-fetches; the missing piece is a step that decides *what* to do at runtime. **Layer 2** — wrapping.

## Pattern

A lead agent owns decomposition, so the fan-out width is a runtime decision:

- The **orchestrator** reads the request and plans which parts to delegate and what each worker returns.
- Each **worker** does one bounded job — a retrieval or a tool call — and returns a structured result.
- The orchestrator **merges** the attributable results for the existing answer chain.

Two design rules:

- **Deterministic spine, model on the edges.** AWS exposes a Step Functions state machine as MCP tools so the agent "can't skip or reorder" them; Microsoft's Durable Extension gives "deterministic multi-agent orchestrations" that checkpoint and replay.
- **Do not hard-code worker identity into the planner prompt.** DeOrch separates planning from selection: the planner emits a *capability*, a registry resolves it.

VMAO adds an orchestration-level LLM verifier; completeness rises 3.1→4.2 (1–5).

## Scenario ladder

| Variant | Need | This week | Ships |
|---------|------|-----------|-------|
| Fixed fan-out | Steps fixed at design time | No | w04 |
| Orchestrator + workers | Fan-out width varies per request | **Yes** | w05 |
| Nested agent teams | A worker is an orchestrator | No | w16 |
| Long-running workers | Work outlives the request | No | w19 |
| Cross-boundary (A2A) | Agents cross an org boundary | No | w20 |

Only the middle row ships this week.

## When not to use

- A single augmented call with retrieval already clears the bar; add a worker only when the task branches into independent parts.
- Steps known and fixed? Use a workflow engine, not a model-driven orchestrator.
- Tight latency budget: every worker adds a model call plus a merge hop.
- No per-path evaluation exists; a variable-width fan-out needs the orchestration-level check first.
- A single lookup with no merge is a tool call, not orchestration.

## Apply it to Acme

The w05 increment adds `core/orchestrator.py`:

- `decompose(question)` returns the runtime plan; a model emits it in production, a deterministic rule here so replay is stable.
- Workers are `policy_lookup` and `order_lookup`, addressed by capability, capped by `MAX_WORKERS`.
- `answer_with_orchestrator()` plans → delegates → merges → answers via the existing intent chain; `tests/test_orchestrator.py` covers decomposition, the cap, and tool blocking.

Try `"where is order ORD-1001 and the return window?"` — both workers run; `"how do I reset my widget?"` — one. The request chose the fan-out.

```bash
cd projects/acme-support && uv sync --extra dev && uv run pytest
```

Check out the frozen snapshot: `git fetch --tags && git checkout stage-w05`.

## Architect's notebook

| Field | Notes |
|-------|-------|
| Decision | Runtime decomposition + capability-selected workers |
| Rejected | Fixed parallel fan-out (w04) — over/under-fetches |
| Top failure mode | Plausible-but-wrong worker output poisoning the merge |
| Cost hint | One plan + one call per worker + one merge; cap the width |
| NFRs | Latency (slowest worker + merge), cost (worker count) |

## Reference implementation

- **Pattern sample:** [`patterns/w05-orchestrator-workers/code/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/patterns/w05-orchestrator-workers/code)
- **Acme spine:** [`projects/acme-support/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/projects/acme-support)

Tests run without cloud API keys.

## AWS mapping

Typical services (verify current names):

- **Step Functions** as the deterministic spine, exposed to the agent as MCP tools
- **Amazon Bedrock AgentCore** as the orchestrator runtime
- **Lambda** workers, one per capability

Whether one engine is better for agent workers is an **open question**: no head-to-head comparison exists, so treat any "X is better" claim as unresolved.

## Azure mapping

Typical services (verify current names):

- **Durable Functions** (Microsoft Agent Framework Durable Extension) as the spine
- **Microsoft Foundry Agent Service** as the orchestrator runtime
- **Azure Functions** workers, one activity per capability

The same open question holds — nothing ranks Durable Functions against Step Functions — so do not assert a winner.

## Production checklist

Before production, walk the [Production Readiness Checklist](/production-readiness-checklist/) — golden tests, tool permissions, tracing, cost caps, rollback.

## Further reading

- Verified Multi-Agent Orchestration (VMAO): https://arxiv.org/abs/2603.11445
- DeOrch — decoupled multi-agent orchestration: https://arxiv.org/abs/2610.07556
- Microsoft — Durable Extension (Agent Framework): https://learn.microsoft.com/en-us/agent-framework/integrations/azure-functions

## Disclaimer

Views and examples are my own, for learning purposes, and do not represent my employer.
