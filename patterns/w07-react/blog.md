---
title: "ReAct: the loop where control flow leaves your code"
description: "The model reasons, picks a tool, reads the observation, and decides the next step itself. Here is what you own: the tool set, the pre-execution check, and the stop rule."
pubDate: 2026-12-12
patternWeek: w07
level: Foundation
acmeStage: w07
spineLayers: "2,3"
---

Every pattern so far has fixed the execution path at design time. You defined the chain, selected the route, or orchestrated the workers — control stayed in your code. This week, that changes. The agent now owns the control flow: it decides whether to call a tool, based on the request and its internal reasoning. You no longer sequence steps — you define the arena in which the agent operates. This shift introduces dynamism, but also uncertainty. The model now interleaves reasoning with action, and the path emerges during execution. You trade predictability for flexibility, and your responsibility shifts from directing every step to designing guardrails and boundaries.

The agent pattern is not new, but its practical use has been limited by reliability. Earlier approaches like prompt chaining or routing could not adapt to runtime context. If a user's query already contained the answer, you still called the tool — wasting cost and latency. ReAct changes that by allowing the model to reason about whether a tool call is needed at all. This is not just about efficiency. It is about aligning the execution path with the actual information state of the request. When done right, the agent avoids unnecessary calls. When done wrong, it hallucinates, misuses APIs, or loops indefinitely. The key is not to let the agent run free, but to bound the loop, validate every call, and retain ownership of the safety perimeter.

## Prerequisites

This pattern builds on [w01 augmented LLM](/blog/w01-augmented-llm/), [w02 prompt chaining](/blog/w02-prompt-chaining/), [w03 routing](/blog/w03-routing/), [w04 parallelization](/blog/w04-parallelization/), [w05 orchestrator-workers](/blog/w05-orchestrator-workers/), and [w06 evaluator-optimizer](/blog/w06-evaluator-optimizer/).

## Context

The gap lies in dynamic decision-making. Consider a request for order status. If the user already provides the order number and delivery date, no tool call is needed. But if the request is open-ended — "What is the status of order ORD-2044?" — the agent must retrieve it. No prior pattern allows this kind of runtime branching based on the presence or absence of facts. This is where Layer 2 (wrapping tools) meets Layer 3 (guardrails). You must expose tools, but also constrain their use. The agent gains autonomy, but only within a tightly defined boundary.

## Pattern

The ReAct pattern is a loop: reason, act, observe. The model generates a reasoning trace, selects a tool, executes it, reads the result, and decides the next step — all dynamically. Anthropic defines the distinction clearly: workflows are "orchestrated through predefined code paths", while agents "dynamically direct their own processes and tool usage". ReAct (arXiv 2210.03629) formalizes this by interleaving reasoning traces with task-specific actions, enabling the model to "induce, track, and update action plans as well as handle exceptions". Later work like Toolformer (2302.04761), Gorilla (2305.15334), and ToolLLM (2307.16789) highlights the core challenge: tool selection and argument accuracy. Gorilla shows that models "hallucinate the wrong usage of an API call", and ToolLLM, with 16,464 REST APIs, underscores the need for an API retriever. The lesson is clear: keep your tool set small and well-defined. Complexity scales with surface area, not capability.

The loop has also moved from a prompt scaffold to a runtime problem. AWS has put Bedrock Agents into maintenance mode as "Agents Classic" and points code-defined agents at the Strands Agents SDK on AgentCore, whose runtime instances run long agent sessions; the corpus documents Lambda durable functions and Foundry hosted agents alongside it and compares none. Bedrock's tool-use system prompt adds about 286 tokens on current Anthropic generations, and the `tools` parameter is re-sent on every step, so a loop's cost is per step, not per request. That is why the stop rule matters: a non-deterministic trajectory with no cap is a cost you cannot forecast.

## Scenario ladder

| Variant | Need | This week | Ships |
|---------|------|-----------|-------|
| Fixed chain that always calls the tool | Baseline | No — the baseline to measure | w02 |
| Router picking one fixed path | Deterministic branching | No | w03 |
| Bounded ReAct loop with one read tool | Dynamic decision to call | **Yes** | w07 |
| Tool calling with a typed contract | Structured input/output | No | w10 |
| Tools through an MCP registry | Discovery and composition | No | w11 |
| Agent chooses when to retrieve | Adaptive retrieval | No | w12 |
| Least-privilege scoped tools | Security boundary | No | w29 |

Only the middle row ships this week. The rest need evidence w07 does not have: a branch count that fits a router, a shared tool surface, or a scoping rule.

## When not to use

Do not use ReAct when the path is known and short, the branch count is bounded, or the sequence must be auditable before execution. Avoid it when argument accuracy is the bottleneck and the API surface is large. It is not suitable when latency or cost is tight, the next step never depends on a tool result, or the tool acts on the world. Keep write operations out of the loop. This pattern is for read-heavy, fact-dependent decisions where dynamic branching adds value. And evaluate it as a trajectory, not an answer: the path is known only after the run, so a loop is scored as a whole conversation. No source in this week's corpus sets a pass threshold or a sampling rate for that — it is an open question, not a settled number.

## Apply it to Acme

The w07 increment introduces `projects/acme-support/core/react.py`, built on the w06 critic. It implements a bounded ReAct loop (`MAX_STEPS = 4`) with one read-only tool: `get_order_status`. A pre-execution hook, `check_tool_call`, validates the tool name and arguments against an allowlist. If validation fails, the error becomes the observation, allowing the model to self-correct. Requests that state facts (e.g. "Order ORD-1001 status: shipped") are answered directly. Requests lacking facts (e.g. "What is the status of order ORD-2044?") trigger a single tool call, and the response is generated from the observation. The demo covers both cases.

```bash
cd projects/acme-support && uv sync --extra dev && uv run pytest
```

The test suite runs 37 tests in mock mode, requiring no API keys. The pattern sample at `patterns/w07-react/code` adds 11 more.

## Architect's notebook

| Field | Notes |
|------|-------|
| Decision | Bounded ReAct loop, one read tool, checked calls, cap owned by code |
| Rejected | Open-ended loop, parsing "Thought / Action / Observation" prose |
| Top failure mode | A hijacked or malformed call executed without a check |
| Cost hint | 1 call when the request carries its facts, 2 when a lookup is needed, versus 1 for w01 — tool-use overhead is re-sent every step |
| NFRs | Latency: unknown step count on the critical path; security: read-only scoped identity, allowlist + intent check before execution; audit: trajectory stored per request |

## Reference implementation

The pattern sample is at `patterns/w07-react/code/`. The Acme spine is at `projects/acme-support/`. Tests run without cloud API keys.

## AWS mapping

Amazon Bedrock model returns typed tool_use blocks. AgentCore runtime instances host the loop (GA, long sessions; Bedrock Agents is now "Agents Classic" and points code-defined agents at the Strands Agents SDK). The tool is a Lambda under an STS GetScopedCredentials read-only identity. An inline policy check and Bedrock Guardrails gate the call. CloudWatch holds the trajectory. Verify current names.

## Azure mapping

Microsoft Foundry Agent Service hosts the agent (threads, tool calls). A Foundry model deployment returns a typed function-call block. A Foundry Toolbox groups tools behind one MCP endpoint with a tool policy. The tool is an Azure Functions app under an Entra ID managed identity with scoped read. Durable Functions owns the loop when it must survive a restart. Application Insights plus multi-turn evaluation score the trajectory. Verify current names.

## Production checklist

Refer to the Production Readiness Checklist. Key items here: the tool allowlist, the pre-execution check, the stop rule, and the trace.

## Further reading

- Anthropic Building effective agents https://www.anthropic.com/research/building-effective-agents
- ReAct https://arxiv.org/abs/2210.03629
- Toolformer https://arxiv.org/abs/2302.04761
- Gorilla https://arxiv.org/abs/2305.15334
- ToolLLM https://arxiv.org/abs/2307.16789

## Disclaimer

Views and examples are my own, for learning purposes, and do not represent my employer.
