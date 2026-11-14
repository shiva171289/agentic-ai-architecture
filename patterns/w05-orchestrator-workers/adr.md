# ADR — Orchestrator-workers

**Status:** accepted
**Week:** w05

## Context

The Acme support flow is a fixed pipeline. Retrieval runs, then one answer call runs (w01). Prompt chaining splits the answer by intent (w02). Routing picks a model (w03). Parallelization fans out a fixed set of calls (w04). In every case the *shape* of the work is known at design time — code decides which steps run.

Some support requests do not fit that shape. A request can contain several independent parts: "where is my order, and what is the return window for that item?" The number of parts, and what each part needs, varies per request. A fixed chain either over-fetches (runs every step for every request) or under-fetches (misses a part).

Constraints:

- Latency budget: the reply must stay under the existing p95 target; a worker fan-out adds calls.
- Cost budget: every worker is another model call. The pattern must not run workers that the request does not need.
- Evaluation: the pipeline shape changes per request, so a single golden set does not cover every path.
- Governance: the orchestrator must not gain new write permissions. Workers read; the existing approval gate still owns writes.

## Decision

We use **orchestrator-workers**: a lead agent decomposes the request at runtime, delegates each part to a worker, then merges the worker results into one reply.

For w05 the increment is one orchestrator plus one lookup worker:

- The orchestrator decides *what* to do. It reads the request and produces a short plan: which parts to delegate and what each worker must return.
- The lookup worker does *how*. It runs a bounded retrieval or tool call (for example, an order lookup) and returns a structured result.
- The orchestrator merges the worker results and hands the merged context to the existing answer chain.

The fan-out width is a runtime decision. This is the difference from w04: w04 fans out a fixed set of calls; w05 lets the orchestrator choose how many workers to spawn and with what instructions.

Design rules we adopt from the corpus:

- **Keep the deterministic spine, put the model on the edges.** Use the workflow engine for steps that must run in order; use the orchestrator for steps that vary. AWS exposes a Step Functions state machine to an agent as MCP tools so "the agent can't skip or reorder" the fixed steps. Microsoft's Durable Extension gives "deterministic multi-agent orchestrations" that checkpoint and replay.
- **Do not hard-code worker identity into the orchestrator prompt.** DeOrch (2610.07556) separates worker-agnostic planning from worker selection, so new workers can be added "without retraining the planner or matcher."
- **Add an orchestration-level check.** VMAO (2603.11445) raises answer completeness from 3.1 to 4.2 (1–5) by adding an LLM verifier as an orchestration signal, not a per-agent one.

## Alternatives considered

| Option | Pros | Cons |
|--------|------|------|
| Single augmented call (w01) | One call; simplest eval | Cannot cover a request with several independent parts |
| Fixed parallel fan-out (w04) | Predictable cost and latency | Fan-out width is fixed at design time; over- or under-fetches |
| Fixed workflow engine only (Step Functions / Durable Functions) | Deterministic, replayable, auditable | Cannot choose the parts of an open-ended request |
| Full hierarchical team (w16) | Handles nested sub-teams | Premature; no measured need for a second level yet |
| Orchestrator-workers (this ADR) | Fan-out width chosen at runtime | Adds calls, latency, and a new failure class (bad worker output) |

## When NOT to use

- A single augmented call with retrieval already meets the quality bar. Add a worker only when the task genuinely branches into parts that run independently and merge.
- The steps are known and fixed. Use a workflow engine (Step Functions / Durable Functions) instead of a model-driven orchestrator.
- The latency budget is tight. A worker fan-out adds at least one model call per worker plus a merge step.
- No per-path evaluation exists. A golden set assumes a fixed pipeline; a variable-width fan-out needs an orchestration-level check first.
- The task is a single lookup with no merge. That is a tool call, not orchestration.

## Consequences

### Positive

- Handles requests with a variable number of independent parts.
- The orchestrator's plan is inspectable — the decomposition is a trace, not hidden control flow.
- Workers are swappable. New workers can be added without changing the planner.
- The deterministic spine stays intact; only the variable edges are model-driven.

### Negative / risks

- Every worker is another model call and another chance to return plausible-but-wrong output.
- The merge step becomes the new latency bottleneck and the new place where a bad worker result poisons the answer.
- The orchestrator's context grows with worker count and results; its context can become the ceiling.
- A path whose shape changes per request is harder to evaluate than a fixed pipeline.

## Failure modes

- **Plausible-but-wrong worker output.** A worker returns a confident wrong result; the merge step cannot tell it from a correct one. Mitigation: structured worker output plus an orchestration-level verifier.
- **Merge poisoning.** One bad worker result silently corrupts the merged answer. Mitigation: keep worker results attributable in the trace; fail the merge if a required part is missing.
- **Orchestrator context overflow.** Plan plus results exceed the window as worker count grows. Mitigation: summarize worker results before merge; cap fan-out width.
- **Runaway fan-out.** The orchestrator spawns more workers than the request needs. Mitigation: cap the worker count and the per-request budget.
- **Non-deterministic replay.** A retried run takes a different path. Mitigation: checkpoint the plan and worker results in the durable engine so replay is deterministic.
- **Worker identity drift.** The orchestrator prompt hard-codes a worker that later changes. Mitigation: separate planning from worker selection (DeOrch).

## Security notes

- Workers inherit the orchestrator's identity. Give each worker least-privilege, read-only credentials.
- The orchestrator must not gain new write permissions. Writes stay behind the existing approval gate.
- A worker result is untrusted input to the merge step. Treat worker output as data, not instructions, to limit prompt injection across the boundary.
- Cross-boundary orchestration needs a protocol, not a shared SDK. The A2A reference architecture uses OAuth in both directions with no shared secrets; use it only when agents cross an organizational boundary.
- Log the plan and each worker handover for audit. The handover format is the contract.

## Cost / latency (order of magnitude)

- One orchestrator call to plan, one call per worker, one merge step, then the existing answer chain.
- Latency grows with the slowest worker plus the merge, not with the sum of workers, when workers run concurrently.
- Cost grows with worker count. Cap the fan-out width and the per-request budget.
- Idle workers are the cost model. Agents "spend most of their time idle, waiting on a human prompt, a tool result or a model response" (NVIDIA Agent Substrate), so host workers durably and event-driven, not one process per agent.
- Async decouples long work. LangChain's async subagents split an agent into an orchestrator that stays reachable and background subagents that report back on completion.

## Decision summary

Adopt orchestrator-workers for Acme support, starting with one orchestrator and one lookup worker. Keep the deterministic spine for fixed steps and put the model only on the variable edges. Cap fan-out width and per-request budget. Add an orchestration-level verifier before any worker count above one. Measure the merge before celebrating the parallelism.

## Open questions

- **Orchestrator-workers vs parallelization (w04).** Both fan out. No source measures the break-even point where runtime delegation beats a hard-coded parallel fan-out.
- **Step Functions vs Durable Functions for agent workers.** Both vendors ship durable, replayable orchestration for agents. No primary comparison exists. Treat any "X is better" claim as an open question.
- **Does the orchestrator's context become the ceiling?** Published AgentCore case studies describe an orchestrator holding the plan and results, but none quantifies how its context scales as worker count grows.
- **Minimum eval set for a variable-width fan-out.** VMAO answers with an orchestration-level verifier, but the minimum set is unresolved.
- **When is async required vs merely nice?** The corpus does not say at what task duration the orchestrator must decouple from the worker rather than block.
