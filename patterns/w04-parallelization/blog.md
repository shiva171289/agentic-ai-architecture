---
title: "Parallelization: fetch policy and order context together"
description: "Independent I/O in parallel, then one synthesis call — before orchestrator-workers."
pubDate: 2026-11-21
patternWeek: w04
level: Foundation
acmeStage: w04
spineLayers: "2"
---

Most support questions need one lookup. Some need two: the policy that governs the item, and the current state of a specific order. Neither depends on the other, yet a sequential chain still pays for both, one after the other. Parallelization removes that wait — and the independence check it enforces carries into every later multi-agent pattern.

## Prerequisites

[w03 routing](/blog/w03-routing/). You should already have a retrieve-then-answer chain.

## Context

**Acme Manufacturing** (fictional) sells hardware online and runs a tier-1 support assistant. The w01–w03 stages answer FAQ and policy questions from synthetic documents. More traffic now mixes two sources: the return or warranty policy, and one order's status. Neither informs the other.

Sequentially, the user waits for the sum; together, for the slower of the two. The architecture question: can we cut wall-clock latency without a second model call and without changing the answer? This is **Layer 2** of the spine — wrapping.

## Pattern

Follow this recipe:

1. Find lookups that do not depend on each other. Confirm neither reads the other's result.
2. Wrap each lookup in a function that takes only the question.
3. Submit both functions to a thread pool. Use `ThreadPoolExecutor(max_workers=2)`.
4. Collect each future's result.
5. Merge the snippets into one labelled context block.
6. Run the existing answer chain once over the merged context.
7. Log each snippet and its source. Keep the answer attributable.

The fan-out width is fixed at design time — two lookups today. That keeps the merge deterministic.

## Scenario ladder

| Variant | When you need it | This week | Ships |
|---------|------------------|-----------|-------|
| Sequential I/O | Fast dependencies | No | w02 chain |
| Parallel independent I/O | Policy + order unrelated | **Yes** | w04 |
| Agent fan-out workers | Dynamic subtasks | No | w05 |

This week ships only the middle row. When the lookup count varies per request, you need a step that chooses the fan-out at runtime — orchestration, shipping in w05.

## When not to use

- **When the calls are not actually independent.** If lookup B reads A's output, parallelism is a bug, not an optimization.
- **When shared clients are not thread-safe.** A client reused across threads can race. Use one client per task, or async with a proper pool.
- When the parts vary per request. A fixed fan-out over- or under-fetches. Use w05.
- When one lookup already answers the question. A second source adds cost and a new failure mode.

## Apply it to Acme

**Stage w04** adds `answer_with_parallel_context()` to [`core/support.py`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/projects/acme-support). It loads synthetic data from `data/policies.json` and `data/orders.json`, submits a policy retrieval and an order snippet to a two-worker `ThreadPoolExecutor`, merges them, then runs the existing intent chain. Tool blocking from w02 still applies.

Order data is synthetic: `ORD-1001` (shipped, Acme Widget Pro) and `ORD-2044` (processing, Acme Widget Mini). The real `get_order_status` tool arrives in **w10**.

```bash
cd projects/acme-support && uv sync --extra dev && uv run pytest
```

`test_parallel_includes_order` covers the merge. Frozen snapshot: `git fetch --tags && git checkout stage-w04`.

## Architect's notebook

| Field | Notes |
|-------|-------|
| Decision | Two-worker thread pool, then one synthesis call |
| Rejected alternative | Sequential fetch — pays the sum of two latencies |
| Top failure mode | Race on a shared, non-thread-safe client |
| Cost hint | Saves wall-clock latency, not tokens |
| NFRs | Lower p95 latency on mixed requests; keep answers attributable |

## Reference implementation

- **Pattern sample:** [`patterns/w04-parallelization/code/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/patterns/w04-parallelization/code) — `run_parallel()` fans out and merges two lookups.
- **Acme spine:** [`projects/acme-support/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/projects/acme-support) — the same shape over JSON policy and order data.

Tests run without cloud API keys.

## AWS mapping

Typical services (verify names in current docs):

- **Lambda** parallel invocations for the two lookups
- **Step Functions** `Parallel` state to fan out and merge
- **Amazon Bedrock** for the final synthesis call

Flow: API Gateway → Step Functions `Parallel` → two Lambdas → merge → `InvokeModel`.

## Azure mapping

Typical services (verify names in current docs):

- **Durable Functions** fan-out/fan-in orchestration
- **Azure Functions** for the two lookups, with managed identity
- **Azure OpenAI** for the final synthesis call

For I/O-bound work, `asyncio` in one Function app is often simpler.

## Production checklist

Before production, walk the [Production Readiness Checklist](/production-readiness-checklist/) — golden tests, tool permissions, tracing, cost caps, rollback.

## Further reading

- Anthropic — building effective agents
- AWS Step Functions `Parallel` state documentation (docs.aws.amazon.com)
- Azure Durable Functions fan-out/fan-in documentation (learn.microsoft.com)

## Disclaimer

Views and examples are my own, for learning purposes, and do not represent my employer.
