# Scenario ladder — react

List variants for this pattern family. Implement **only** this week's row; link to future weeks for the rest.

| Variant | When you need it | This week | Ships |
|---------|------------------|-----------|-------|
| Fixed chain that always calls the tool (baseline) | The reply always needs the same one lookup | No — the baseline to measure against | w02 |
| Router that picks one fixed path | The branch count is bounded and listable | No | w03 |
| Bounded ReAct loop, one read tool | The next step depends on a tool result and the step count is unknown | **Yes** | w07 |
| Tool calling with a typed contract | One provider-typed tool call, no loop | No | w10 |
| Tools reached through an MCP registry | The tool surface is shared across agents | No | w11 |
| Agent chooses when to retrieve | The agent, not the pipeline, decides whether to search | No | w12 |
| Least-privilege, scoped tools | The loop's credentials must be cut to task scope | No | w29 |
| Inline tool-call governance | Every proposed call must be checked against intent before execution | No | w48 (policy enforcement) |
| Connect a ReAct loop to a remote MCP server | The agent must reach a shared internal MCP endpoint safely | No | w11 |
| ReAct over the ERP (fictional Acme) | The loop queries back-office APIs, not order state | No | w41 (procure-to-pay) |

Only the third row ships this week. The rest need evidence w07 does not have: a branch count that fits a router, a shared tool surface, a scoping rule, or a runtime decision.

## Open questions

- **What stop rule ends the loop, and who owns it?** ReAct (2210.03629) has no built-in terminator; no source gives a max-step, token-budget or wall-clock number for a customer-facing loop. This is the W07 mapping-focus gap.
- **When does a tool loop beat a router calling one fixed tool?** For the Acme case (one tool, one branch) the corpus gives no guidance. W09 (agent or workflow?) is scheduled to answer it, and w07 must not pre-empt it.
- **How do you evaluate a non-deterministic trajectory?** Foundry multi-turn evaluation, Insights and LangSmith trace search all point at it; no source states a pass threshold or a sampling rate for a tool loop.
- **Which runtime hosts the loop?** AgentCore runtime instances, Lambda durable functions and Foundry hosted agents are all documented and compared none. W19, W23 and W38 are meant to settle it.
- **What does inline tool-call governance cost?** Google's semantic policies evaluate every proposed call before execution; AWS bills Bedrock Guardrails per content inspection. Neither publishes the added latency per tool step, and it multiplies by the number of steps.

## Reference

- Topic ladder: [content/topics/](../../content/topics/README.md)
- Acme stage: [07-running-use-case.md](../../docs/roadmap/07-running-use-case.md)
