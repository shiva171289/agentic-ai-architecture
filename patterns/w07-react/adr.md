# ADR — ReAct loop

**Status:** accepted
**Week:** w07

## Context

The Acme support flow produces one reply per request. Retrieval runs, then one answer call runs (w01). Prompt chaining splits the answer by intent (w02). Routing picks a model (w03). Parallelization fetches context from several sources at once (w04). Orchestrator-workers decomposes a request into parts at runtime (w05). Evaluator-optimizer checks and rewrites the draft (w06).

In every one of those patterns the path is fixed before the request runs. The chain, the routes, the worker list and the critic's criteria are all set at design time. The model decides what to say, not what to do next. If a request needs a step the design did not anticipate, the pipeline cannot ask for it.

The order-lookup case makes the gap concrete. A request for order status needs `get_order_status` before a useful reply. But a request that already carries the order number and the delivery date in its text does not need the call, and calling it anyway costs a step and a tool round-trip. Today the code decides this in advance; no step lets the agent decide whether the lookup is needed.

ReAct is the first pattern in the ladder where control flow leaves your code. The model writes a reasoning trace, picks a tool, reads the observation, and decides the next action, looping until it answers. Anthropic's definitional line separates this from everything above it: workflows "are orchestrated through predefined code paths", while agents "dynamically direct their own processes and tool usage". ReAct (2210.03629) is the pattern's origin. It interleaves reasoning traces with task-specific actions, and the traces "help the model induce, track, and update action plans as well as handle exceptions".

Constraints:

- Latency budget: the reply must stay near the existing p95 target. Each tool step is a model round-trip on the critical path, and the design cannot predict the number of steps.
- Cost budget: every step re-sends the tool definitions and the whole message history. A five-step loop pays the tool-use overhead five times.
- Tool surface: small and curated. Each added tool raises every step's prompt cost and lowers selection accuracy.
- Evaluation: the trajectory is non-deterministic, so it must be scored as a whole conversation, not as one answer.
- Governance: the loop acts with order and CRM credentials on text a customer wrote. Tool calls need an allowlist, scoped credentials, and a check before execution.
- Trust boundary: customer text is untrusted input. In a fixed chain, injected text can mislead one answer; in a loop, it can direct the next action.

## Decision

We use a **bounded ReAct loop** for the Acme support reply. The agent reasons, decides whether it needs the order lookup, reads the observation, and either takes another step or writes the reply.

For w07 the increment is one tool and a hard cap:

- The agent runs a reason → act → observe loop against a small tool set. The first tool is `get_order_status`.
- The agent decides whether to call it. A request that already carries the facts can answer without a tool call.
- The loop is capped by our code: a maximum step count and a token and wall-clock budget. ReAct has no built-in terminator, so the stop rule is ours, not the model's.
- Tool calls use the provider's structured contract (a typed tool-call block and a typed tool-result block), not parsed "Thought / Action / Observation" text.

Design rules we adopt from the corpus:

- **Keep the tool set small and the descriptions current.** Toolformer (2302.04761) shows the model can learn when and how to call an API from few demonstrations. Gorilla (2305.15334) shows the failure plainly: models struggle to "generate accurate input arguments" and "hallucinate the wrong usage of an API call". ToolLLM (2307.16789) scales the same problem to 16,464 real REST APIs and needs an API retriever. Argument accuracy degrades as the surface grows, so the set stays small and the descriptions stay current.
- **Expect argument errors and budget for them.** The loop must validate arguments against the tool schema and return a typed error as the observation, so the model can correct on the next step. Gorilla pairs the model with a document retriever so it "adapts to test-time document changes".
- **Use the provider's tool contract, not prose parsing.** Anthropic's API answers with `stop_reason: "tool_use"` and typed `tool_use` blocks that your code executes and returns as `tool_result`. Foundry and AgentCore expose the same shape. A hand-rolled trace parser is a regex over a model's prose, and it is where a loop silently degrades.
- **Own the stop rule.** No source gives a step, token or time limit for a customer-facing loop. The cap is ours: a maximum step count plus a per-request budget. A wrong answer delivered after nine tool calls is worse than a fast, honest "I need to check that".
- **Scope the loop's credentials down.** AWS STS `GetScopedCredentials` exists because each agent should have "only the permissions its tasks require, rather than the full permissions of the session that started it". LangChain's Tool Gateway publishes a curated *tool kit* so the agent "only sees the tools bundled in it", and Foundry's Toolboxes group tools behind one MCP endpoint with a policy that sets approved tool types. The loop reads order data with a read-only identity, and sees only the tools it needs.
- **Check the proposed call before execution.** Google's semantic governance policies "validate every proposed tool call against user intent and natural language constraints before execution", taking AgentDojo attack success from 48.7% to 0.9% on a Gemini 2.5 Flash agent. At minimum the loop allowlists the tool and validates arguments against its schema before the call runs.
- **Treat the loop as a runtime decision, not a prompt trick.** Amazon Bedrock Agents is now "Agents Classic", closed to new sign-ups, and points code-defined agents at the Strands Agents SDK on AgentCore. AgentCore runtime instances are GA with long agent sessions. Long-running tool loops are being sold as a hosting property.

## Alternatives considered

| Option | Pros | Cons |
|--------|------|------|
| Fixed chain that always calls the lookup (w02) | Deterministic order; cheap; fully testable | Pays a tool call on every request, even when the facts are already in the text |
| Router that picks one of N fixed paths (w03) | Deterministic branching; predictable cost | The branch count is fixed at design time, so a request with no matching path falls through |
| Single augmented call, no tool (w01) | One call; lowest latency; simplest eval | Cannot read live order state; answers from the prompt alone |
| Evaluator-optimizer on the draft (w06) | Checks the reply before it ships | Improves the answer, not the path; it cannot decide that a lookup is needed |
| Bounded ReAct loop (this ADR) | The agent decides whether to act, so it can gather facts a fixed path cannot anticipate | Non-deterministic; pays tool overhead per step; opens an action surface driven by customer text |

## When NOT to use

- **The path is known and short.** If the reply always needs the same one lookup, a fixed chain (w02) is cheaper, testable and deterministic. Anthropic's guidance is to find the simplest solution and add complexity only when it demonstrably helps; its pattern material puts agents last, after five workflow patterns.
- **The branch count is bounded.** A router (w03) enumerates the paths. If you can list the paths, list them.
- **The sequence must be auditable before the fact.** A deterministic chain records exactly what will run. A loop's path is known only after it runs. Where a compliance rule fixes the sequence, code the sequence.
- **Argument accuracy is the bottleneck and the tool surface is large.** Gorilla and ToolLLM both needed retrievers. If the set cannot stay small and the descriptions current, the loop calls the wrong tool or passes the wrong arguments.
- **Latency or cost is tight.** Every step is a model round-trip plus a re-send of the tool overhead. If the p95 cannot absorb an unknown number of steps, do not ship the loop.
- **The next step never depends on a tool result.** Then there is nothing for the loop to decide, and it is a chain with extra cost.
- **The tool acts on the world.** The loop is for reads first. A write, a refund or a send stays behind the existing approval gate; the loop must not be the thing that fires a write.

## Consequences

### Positive

- The agent gathers facts a fixed path cannot anticipate: it decides whether the lookup is needed, so a request that carries its own facts skips the call.
- The trajectory is readable. ReAct's traces let a human see why the agent called a tool, which is what makes a support loop debuggable at all.
- Tool selection and argument accuracy become explicit, measurable properties. Google's multi-turn agentic RL trains tool compliance; Foundry's multi-turn evaluation scores whole conversations.
- The tool layer becomes a place to attach identity, scoped credentials, a policy check and a trace per call (Tool Gateway, Toolboxes, Agent Gateway), instead of scattering credentials through prompt code.
- The loop is a natural host for the runtime capabilities arriving this month: long sessions, checkpointing, and sandboxes for agent-generated code.

### Negative / risks

- Non-determinism on the critical path. The number of steps is unknown before the request runs, so latency and cost vary per request.
- Tool-use overhead is paid on every step. The `tools` parameter, the `tool_use` blocks and the `tool_result` blocks are re-sent each turn; a five-step loop pays them five times.
- The loop is where prompt injection becomes action. Customer text can direct the next tool call, and the agent holds order and CRM credentials.
- Argument errors are the normal failure, not the exception. The model will call the wrong tool or pass a wrong argument.
- The loop can fail to terminate, or stop before it has the facts.
- The runtime is unsettled. AgentCore, Lambda durable functions and Foundry hosted agents all document long-running tool loops and compare none.

## Failure modes

- **Infinite or long loop.** ReAct has no built-in terminator. Mitigation: cap the steps and set a token and wall-clock budget in our code.
- **Wrong tool or wrong argument.** Selection accuracy degrades as the tool set grows. Mitigation: keep the set small, keep the descriptions current, validate arguments against the tool schema, and return a typed error as the observation so the model can correct.
- **Injected instruction becomes a tool call.** Customer text in the request, or in a tool result, directs the next action. Mitigation: treat customer text and tool results as data, and check the proposed call against the user's intent before execution.
- **Stop too early.** The agent answers before it calls the tool it needed. Mitigation: name the facts a complete answer requires, and score the trajectory offline against them.
- **Observation poisoning.** A tool returns text that carries instructions and the loop treats it as a step. Mitigation: separate tool-result content from instructions; never let a tool result change the tool allowlist.
- **Trace lost.** The loop runs but the steps are not recorded, so a bad answer cannot be explained. Mitigation: store the trajectory (reason, call, observation) as a trace per request.
- **Silent degradation from prose parsing.** A hand-rolled "Thought / Action" parser breaks when the model formats differently. Mitigation: use the provider's structured tool contract.

## Security notes

- The loop reads text a customer wrote and holds credentials for order and CRM tools. It is the point where injection becomes action.
- Scope the loop's identity down: only the tools it needs, read-only where possible, short-lived credentials (GetScopedCredentials; tool kit and toolbox curation).
- Check the proposed tool call against user intent before execution, not after. The inline policy check is the control that the old "a valid OAuth token implies user intent" model no longer provides.
- Keep writes out of the loop. The loop gathers facts; a write is a separate, gated action.
- Treat tool results as untrusted. A tool can return attacker-influenced text, and the loop must not execute instructions found in it.
- Discover and inventory the tool endpoints. An undocumented public-facing MCP server is a shadow API; AWS WAF now flags it and can screen it with Bedrock Guardrails.
- Sandbox agent-generated code. If a tool runs code the model wrote, run it in an isolated MicroVM, not in the loop's process.

## Cost / latency (order of magnitude)

- One step is one model round-trip plus the tool overhead: the `tools` parameter, the `tool_use` block and the `tool_result` block, plus a per-model tool-use system prompt (about 286 tokens for current Anthropic Opus, Sonnet and Haiku generations, higher on older ones). A five-step loop pays that five times.
- A request that carries its own facts can answer in one call — the loop's saving over a chain that always calls the tool.
- Cost is variable per request, because the number of steps is decided at runtime. Cap it and set a per-request budget.
- The break-even is unmeasured. No source gives the fraction of requests where the extra step pays for itself. Baseline the fixed chain first.
- Inline governance adds latency per proposed call (a semantic policy check, or a WAF and Guardrails inspection). No source publishes the per-step number, and it multiplies by the number of steps.
- The runtime is a separate cost: AgentCore sessions, Lambda durable functions, or a hosted agent. Long sessions bill for the time the loop is open.

## Decision summary

Adopt a bounded ReAct loop for the Acme support reply, with a small curated tool set (`get_order_status` first), scoped read-only credentials, and a stop rule we own (a maximum step count plus a token and wall-clock budget). Use the provider's structured tool contract, not parsed trace text. Check each proposed tool call against the user's intent before execution, and keep writes out of the loop. Record the trajectory as a trace and score it offline against the facts a complete answer requires. Measure the fixed-chain baseline before standing up the loop.

## Open questions

- **What stop rule ends the loop, and who owns it?** No source gives a max-step, token-budget or wall-clock number for a customer-facing loop. This is the W07 mapping-focus gap.
- **How do you evaluate a non-deterministic trajectory?** Foundry multi-turn evaluation, Insights and LangSmith trace search all point at it, but no source states a pass threshold or a sampling rate for a tool loop.
- **Which runtime hosts the Acme loop?** AgentCore runtime instances (long sessions) versus Lambda durable functions with checkpointing versus Foundry hosted agents — the corpus documents all three and compares none. W19, W23 and W38 are meant to settle it.
- **What does inline tool-call governance cost?** Google evaluates every proposed call before execution and AWS bills Bedrock Guardrails per content inspection. Neither publishes the added latency per tool step.
- **When does a tool loop beat a router calling one fixed tool?** For the Acme case (one tool, one branch) the corpus gives no guidance. W09 (agent or workflow?) is scheduled to answer it, and this ADR must not pre-empt it.
- **Does the tool-use system-prompt overhead exist on every provider?** The Anthropic figures are model-specific and explicit; AWS, Microsoft and Google publish no comparable per-request number, so cross-provider cost comparison (W35) cannot be done from these sources yet.
