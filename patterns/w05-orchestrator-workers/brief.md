# Brief — w05 orchestrator-workers

**Topic:** Orchestrator-workers (an orchestrator decomposes a task, delegates to worker agents, and merges their results)
**Date researched:** 2026-11-13
**Corpus:** `content/source-corpus/latest.md` (201 entries, window 7 days, generated 2026-11-13)

## Summary

The orchestrator-workers pattern puts a lead agent in charge of decomposition: it splits a task, hands each part to a worker, then merges the results into one answer. It is the first pattern in the ladder where the *structure* of the work is decided at runtime by a model instead of by code. This week's corpus shows the pattern moving from "multi-agent" demos toward production plumbing: durable runtimes, async background workers, and inter-agent protocols that cross organizational boundaries. Two vendor lines now converge on the same idea — a deterministic workflow engine (AWS Step Functions, Microsoft Durable Functions) for the steps you can predict, and a model-driven orchestrator for the steps you cannot. For Acme this is the week the support flow stops being a fixed chain and starts delegating: an orchestrator hands off "lookup order" to a worker, then merges that result into the reply. The honest caution is in the corpus too: orchestration adds latency, cost, and a new class of failure (a worker that returns plausible but wrong output), so the pattern should arrive only after a single augmented call has actually failed.

## Sources

| Title | URL | Date accessed |
|-------|-----|---------------|
| AWS — Build composable, interoperable multi-agent systems with A2A on AWS | https://aws.amazon.com/blogs/machine-learning/build-composable-interoperable-multi-agent-systems-with-a2a-on-aws/ | 2026-11-13 |
| AWS — Run agents securely and efficiently with the next generation AgentCore runtime | https://aws.amazon.com/blogs/machine-learning/run-agents-securely-and-efficiently-with-the-next-generation-agentcore-runtime/ | 2026-11-13 |
| AWS — How Natera designed an agentic AI system for lab ops with Amazon Bedrock AgentCore | https://aws.amazon.com/blogs/machine-learning/how-natera-designed-an-agentic-ai-system-for-lab-ops-with-amazon-bedrock-agentcore/ | 2026-11-13 |
| AWS — Build autonomous AI agents with Amazon Bedrock and Spring AI | https://aws.amazon.com/blogs/machine-learning/build-autonomous-ai-agents-with-amazon-bedrock-and-spring-ai/ | 2026-11-13 |
| AWS — How DXC Technology built a multi-model AI substrate on Amazon Bedrock | https://aws.amazon.com/blogs/machine-learning/how-dxc-technology-built-a-multi-model-ai-substrate-on-amazon-bedrock/ | 2026-11-13 |
| LangChain — Agents Are Going Async | https://www.langchain.com/blog/agents-are-going-async | 2026-11-13 |
| LangChain — How Workday Built an Enterprise-Scale AI Agent Platform with LangGraph and LangSmith | https://www.langchain.com/blog/how-workday-built-an-enterprise-scale-ai-agent-platform-with-langgraph-and-langsmith | 2026-11-13 |
| LangChain — How Stripe Built Kai on Deep Agents in 1 Week | https://www.langchain.com/blog/how-stripe-built-their-knowledge-ai-platform-on-deep-agents | 2026-11-13 |
| Databricks — How Block powers collaborative AI agents with Buzz and Unity Gateway | https://www.databricks.com/blog/how-block-powers-collaborative-ai-agents-buzz-and-unity-gateway | 2026-11-13 |
| NVIDIA — Agent Substrate: Advancing Kubernetes for Agents at Scale | https://developer.nvidia.com/blog/agent-substrate-advancing-kubernetes-for-agents-at-scale/ | 2026-11-13 |
| AWS — Step Functions: Discover use cases (Tools for AI agents) | https://docs.aws.amazon.com/step-functions/latest/dg/use-cases.html | 2026-11-13 |
| AWS — Prescriptive guidance: Orchestration models, from rule-based to AI-native | https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/orchestration-models.html | 2026-11-13 |
| Microsoft — Durable Extension for Microsoft Agent Framework | https://learn.microsoft.com/en-us/agent-framework/integrations/azure-functions | 2026-11-13 |
| Microsoft — AI integration options for Azure Functions | https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-ai-enabled-apps | 2026-11-13 |
| arXiv — The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption (2601.13671) | https://arxiv.org/abs/2601.13671 | 2026-11-13 |
| arXiv — Verified Multi-Agent Orchestration: Plan-Execute-Verify-Replan (2603.11445) | https://arxiv.org/abs/2603.11445 | 2026-11-13 |
| arXiv — Decoupled Multi-Agent Orchestration / DeOrch (2610.07556) | https://arxiv.org/abs/2610.07556 | 2026-11-13 |
| arXiv — AdaptOrch: Task-Adaptive Multi-Agent Orchestration (2602.16873) | https://arxiv.org/abs/2602.16873 | 2026-11-13 |
| arXiv — Autonomous Event-Driven Multi-Agent Orchestration for Enterprise AI at Scale (2606.20058) | https://arxiv.org/abs/2606.20058 | 2026-11-13 |

Corpus note: `content/source-corpus/latest.md` contains **no** vendor-blog entries for "Step Functions" or "Durable Functions" this week (0 matches on both strings). The two orchestration-engine claims below therefore cite the official AWS and Microsoft documentation pages fetched in this session, not the corpus. Do not upgrade them to vendor-blog claims.

## Key concepts

- **The orchestrator decides *what*, the worker does *how*.** AWS draws the line explicitly: Step Functions "manages how things happen," while an agent "decides what should happen based on user goals." Orchestrator-workers is the pattern where a model owns the "what."
- **Dynamic delegation is the difference from parallelization (w04).** w04 fans out a *fixed* set of calls known at design time. w05 lets the orchestrator choose how many workers to spawn and with what instructions — the fan-out width is a runtime decision.
- **Async is how the pattern survives long work.** LangChain's "Agents Are Going Async" splits an agent into an orchestrator that stays reachable and background subagents that report back on completion. Their tool surface is the whole contract: `start_async_task`, `check_async_task`, `update_async_task`, `cancel_async_task`, `list_async_tasks`.
- **Deterministic spine, model-driven edges.** Both engines offer the same shape: Microsoft's Durable Extension gives "deterministic multi-agent orchestrations" that checkpoint and replay; AWS's Step Functions connector exposes a state machine to an agent as MCP tools so "the agent can't skip or reorder" the steps. Use the engine for the steps that must run in order; use the model for the steps that vary.
- **Cross-boundary orchestration needs a protocol, not a shared SDK.** The A2A reference architecture has a LangChain orchestrator on ECS calling a Strands agent on AgentCore across two AWS accounts, OAuth-authenticated in both directions, with no shared secrets and neither side depending on the other's framework.
- **Worker pools change; the planner should not have to.** DeOrch (2610.07556) separates worker-agnostic planning from worker selection, so new workers can be added "without retraining the planner or matcher" — a warning against hard-coding worker identity into the orchestrator prompt.
- **Orchestration is now a first-class design axis, not just model choice.** AdaptOrch (2602.16873) argues that as models converge on benchmarks, "orchestration topology... now dominates system-level performance," reporting 12–23% gains over a static single-topology baseline on identical models.
- **Orchestration-level verification is a quality lever.** VMAO (2603.11445) raises answer completeness from 3.1 to 4.2 (1–5) on market-research queries by adding an LLM verifier as an *orchestration* signal, not a per-agent one.
- **Idle workers are the cost model.** NVIDIA's Agent Substrate points out that agents "spend most of their time idle, waiting on a human prompt, a tool result or a model response," which is why one-Pod-per-agent is the wrong unit and durable/event-driven hosting wins.

## Contrarian angles

1. **Most tasks do not need workers.** Anthropic's own guidance is to "find the simplest solution possible, and only increase complexity when needed" — for many applications, a single augmented LLM call with retrieval is enough. Add a worker only when the task genuinely branches into parts that can run independently and merge.
2. **Fan-out multiplies cost and adds a new failure mode.** Every worker is another model call and another chance to return plausible-but-wrong output. The orchestrator's merge step then becomes the new latency bottleneck and the new place where a bad worker result silently poisons the answer. Measure the merge before celebrating the parallelism.
3. **The framework is not the moat — the tool and state contract is.** The value in these systems lives in the worker's tool schema, the handover format, and the merge rule, not in which orchestrator library you picked. A2A-style interoperability only pays for itself when agents cross an organizational boundary; inside one team, a fixed workflow engine (Step Functions / Durable Functions) is cheaper than a model-driven orchestrator.

## Open questions

- **Orchestrator-workers vs parallelization (w04).** Both fan out. The corpus supports the distinction (dynamic delegation vs fixed calls) but no source measures the break-even point where runtime delegation beats a hard-coded parallel fan-out. Open question for the blog.
- **Step Functions vs Durable Functions for agent workers.** Both vendors now ship durable, replayable orchestration for agents, but no corpus entry or doc page compares them head to head. Treat any "X is better" claim as **Open question** until a primary comparison exists.
- **Does the orchestrator's context become the ceiling?** Natera (SWARM on AgentCore) and DXC (a "trusted harness that orchestrates, governs, and audits") both describe an orchestrator holding the plan and results, but neither quantifies how orchestrator context scales as worker count grows.
- **How do you evaluate a path whose shape changes per request?** A golden set assumes a fixed pipeline. VMAO answers with an orchestration-level verifier, but the minimum eval set for a variable-width worker fan-out is unresolved.
- **When is async required vs merely nice?** LangChain's async subagents target long tasks; the corpus does not say at what task duration the orchestrator must be decoupled from the worker rather than blocking.
