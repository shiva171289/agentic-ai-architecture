---
title: "Orchestrator-workers: let the request choose the fan-out"
description: "A model-driven orchestrator decomposes a request at runtime, delegates to workers, and merges the results — after parallelization is not enough."
pubDate: 2026-11-28
patternWeek: w05
level: Foundation
acmeStage: w05
spineLayers: "2"
---

## Prerequisites

[w01 augmented LLM](/blog/w01-augmented-llm/) · [w02 prompt chaining](/blog/w02-prompt-chaining/) · [w03 routing](/blog/w03-routing/) · [w04 parallelization](/blog/w04-parallelization/).

## The problem

Every pattern so far decides the *shape* of the work at design time. Code picks the steps; the model fills them in. Parallelization (w04) is the sharpest example: it fans out a fixed set of calls — policy retrieval and order snippet — for every request, and merges them.

That is wrong for a request like *"where is my order, and what is the return window for that item?"* It has two independent parts, and the number of parts varies per request. A fixed chain either over-fetches (runs every step for every request) or under-fetches (misses a part). The missing piece is a step that decides *what* to do at runtime.

## The pattern

Orchestrator-workers puts a lead agent in charge of decomposition:

- The **orchestrator** reads the request and produces a short plan: which parts to delegate and what each worker must return.
- Each **worker** does one bounded job — a retrieval or a tool call — and returns a structured result.
- The orchestrator **merges** the attributable results and hands the merged context to the existing answer chain.

The fan-out width is a runtime decision. That is the whole difference from w04: w04 fans out a fixed set of calls known at design time; w05 lets the orchestrator choose how many workers to spawn and with what instructions.

Two design rules keep it honest:

- **Keep the deterministic spine; put the model only on the edges.** Run the steps that must happen in order in a workflow engine, and let the model drive only the steps that vary. AWS exposes a Step Functions state machine to an agent as MCP tools so the agent "can't skip or reorder" the fixed steps; Microsoft's Durable Extension gives "deterministic multi-agent orchestrations" that checkpoint and replay.
- **Do not hard-code worker identity into the planner prompt.** DeOrch separates worker-agnostic planning from worker selection, so new workers can be added without retraining the planner. The planner emits a *capability*; a registry resolves it.

Add an orchestration-level check too. VMAO raises answer completeness from 3.1 to 4.2 (1–5) by adding an LLM verifier as an *orchestration* signal, not a per-agent one — it checks that every planned part came back.

## When NOT to use it

- A single augmented call with retrieval already meets the quality bar. Add a worker only when the task genuinely branches into parts that run independently and merge.
- The steps are known and fixed. Use a workflow engine, not a model-driven orchestrator.
- The latency budget is tight. Every worker adds a model call plus a merge hop.
- No per-path evaluation exists. A golden set assumes a fixed pipeline; a variable-width fan-out needs the orchestration-level check first.
- It is a single lookup with no merge. That is a tool call, not orchestration.

## Apply it to Acme

The w05 increment adds `core/orchestrator.py`:

- `decompose(question)` returns the runtime plan. In production a model emits it; here a small deterministic rule stands in so replay is stable.
- Workers are `policy_lookup` and `order_lookup`, addressed by capability, with a `MAX_WORKERS` fan-out cap.
- `answer_with_orchestrator()` plans → delegates → merges → answers via the existing intent chain. `core/tests` covers multi-part decomposition, the fan-out cap, and the tool-blocking rule.

Try `"where is order ORD-1001 and the return window?"` — both workers run. Ask `"how do I reset my widget?"` — one worker runs. The request chose the fan-out.

## Architect's notebook

| Field | Notes |
|-------|-------|
| Decision | Runtime decomposition + capability-selected workers |
| Rejected | Fixed parallel fan-out (w04) — over/under-fetches |
| Top failure mode | Plausible-but-wrong worker output poisoning the merge |
| Cost hint | One plan + one call per worker + one merge; cap the width |
| NFRs | Latency (slowest worker + merge), cost (worker count) |

## AWS vs Azure notes

Both vendors now offer the same shape: a durable, replayable orchestration engine plus an agent runtime. AWS — Step Functions (spine) + AgentCore (orchestrator) + Lambda workers. Azure — Durable Functions (spine) + Foundry Agent Service (orchestrator) + Functions workers. Which engine is better for agent workers is an **open question**: no primary head-to-head comparison exists, so treat any "X is better" claim as unresolved until one does.

## Disclaimer

Learning material only.
