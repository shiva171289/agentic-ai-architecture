# LinkedIn — w05 orchestrator-workers

## Post A — Pattern

A fixed pipeline runs the wrong shape of work for some requests.

"Where is my order, and what's the return window?" has two independent parts. The count varies per request. A fixed chain over-fetches or under-fetches.

Orchestrator-workers fixes that: a lead agent decides WHAT at runtime, workers do HOW.

- Orchestrator reads the request, emits a short plan.
- Each worker runs one bounded lookup/tool call, returns a structured result.
- Orchestrator merges the attributable results, then answers.
- Fan-out width is a runtime decision — not a design-time constant.

That last point is the whole difference from parallelization (w04).

Keep the deterministic spine (Step Functions / Durable Functions) for the steps that must run in order. Put the model only on the edges.

Full write-up in the first comment.

## Post B — Opinion

Most support systems do not need an orchestrator.

If a single augmented call with retrieval meets the bar, adding workers only adds latency, cost, and a new failure class. If the steps are known and fixed, use a workflow engine — not a model-driven planner.

The new failure class is the point. A worker can return plausible-but-wrong output, and the merge step cannot tell it from a correct one. One bad worker poisons the answer. Add an orchestration-level verifier that checks every planned part came back, and cap the fan-out before it caps you.

AWS and Azure now ship the same shape: a durable replayable engine (Step Functions / Durable Functions) plus an agent runtime (AgentCore / Foundry Agent Service). Which engine is better for agent workers is still an open question — I have not seen a primary comparison.

Do you measure the merge, or just celebrate the parallelism?

/blog/w05-orchestrator-workers/

## Comment starters

1. "How many workers before the orchestrator's context becomes your ceiling?"
2. "Do you run the merge synchronously, or checkpoint it in the durable engine?"
3. "Where do you draw the line between a tool call and a worker?"
