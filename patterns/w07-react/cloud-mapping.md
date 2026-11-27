# Cloud mapping — ReAct loop

## Cloud-agnostic core

The pattern has four moving parts, and only one of them is a model:

- **Model / loop controller** — reasons, chooses a tool, reads the observation, and decides the next action. This is the part that leaves your code.
- **Tool layer** — the small curated set of tools the loop may call. For Acme the first tool is `get_order_status`, a read.
- **Pre-execution gate** — the control that runs *before* a proposed call: allowlist the tool, validate the arguments against its schema, and check the proposed call against the user's intent.
- **Stop rule** — a maximum step count plus a token and wall-clock budget, owned by your code. ReAct has no built-in terminator.

Two things are portable across clouds and one is not:

- **The typed tool contract is portable.** Bedrock, Foundry and AgentCore all return a typed tool-call block that your code executes and returns as a typed tool-result block (`stop_reason: "tool_use"` on Anthropic's API; function-call blocks on Foundry). A hand-rolled "Thought / Action / Observation" parser is a regex over a model's prose, and it is where a loop silently degrades.
- **The trace shape is portable.** A trajectory of (reason, call, observation) per step is a plain document you can write to either telemetry surface.
- **The runtime is not portable.** AWS sells AgentCore runtime instances (long agent sessions) and Lambda durable functions with MicroVMs; Azure sells Foundry Agent Service threads and Durable Functions. Each runtime publishes its own session model, and the corpus compares none of them.

One thing a loop should not own: the stop decision. Keep the cap and the budget in your code, never in the prompt — Anthropic's own definitions note the model "dynamically direct[s] its own processes", so a model-decided stop is a second thing that can be wrong.

## AWS

| Component | Service | Notes |
|-----------|---------|-------|
| Model (loop controller) | Amazon Bedrock | Returns typed `tool_use` blocks; the loop executes them and returns `tool_result` blocks. Do not parse trace prose |
| Agent runtime | Amazon Bedrock AgentCore (runtime instances) | Hosts the loop. Runtime instances are GA with long agent sessions; Bedrock Agents is now "Agents Classic", closed to new sign-ups, and points code-defined agents at the Strands Agents SDK |
| Tool | AWS Lambda (`get_order_status`) | Reads order state through a read-only role |
| Scoped credentials | AWS STS `GetScopedCredentials` | The loop gets "only the permissions its tasks require", not the caller's full session |
| Pre-execution gate | Inline policy check + Amazon Bedrock Guardrails | Allowlist the tool and validate arguments; a semantic policy check validates the proposed call against user intent before execution |
| Endpoint discovery / screening | AWS WAF (LLM/MCP/A2A endpoint discovery) + Bedrock Guardrails | Flags an undocumented public-facing MCP server as a "shadow API" and screens requests |
| Sandbox for agent code | Lambda durable functions orchestrating Lambda MicroVMs | Isolated VMs for untrusted or agent-generated code |
| Trajectory telemetry | CloudWatch (agent traces) / AgentCore Observability | One trajectory (reason, call, observation) per request |

### AWS diagram notes

A channel invokes the AgentCore-hosted loop through Bedrock. The model answers with `stop_reason: "tool_use"` and a typed `tool_use` block; the loop checks the proposed call (tool in the allowlist, arguments valid, intent check) and, if it passes, invokes the read-only `get_order_status` Lambda, which runs under an STS-scoped identity. The `tool_result` block goes back to the model, which either takes another step or returns the reply. The step cap and the token and wall-clock budget live in our code; the state is checkpointed so a restart resumes the loop. Each trajectory is written to CloudWatch. If a tool runs agent-generated code, it runs in a MicroVM, not in the loop's process.

## Azure

| Component | Service | Notes |
|-----------|---------|-------|
| Model (loop controller) | Microsoft Foundry models (Azure OpenAI) | Returns typed function-call blocks; same execute-and-return shape |
| Agent runtime | Microsoft Foundry Agent Service | Hosts the agent's threads and tool calls. A preview tool policy centrally sets the approved tool types, MCP endpoints and connectors |
| Tool curation | Foundry Toolboxes | Groups tools into a versioned collection behind one MCP endpoint; the agent "only sees the tools bundled in it" |
| Tool | Azure Functions (`get_order_status`) | Reads order state through a scoped identity |
| Pre-execution gate | Tool policy + schema validation | Validate arguments against the tool schema and the toolbox policy before execution |
| Identity | Microsoft Entra ID managed identity / Entra Agent ID | Scoped read on the order store; no write role in the loop |
| Durable loop (optional) | Durable Functions | Deterministic, replay-safe orchestrator; the trajectory and the step count are checkpointed |
| Sandbox for agent code | Container Apps sandbox / isolated compute | Run agent-generated code outside the loop's process |
| Trajectory telemetry | Application Insights (custom events) + Foundry multi-turn evaluation | Multi-turn evaluation scores the whole conversation, because that is how most agents fail |

### Azure diagram notes

A channel starts a Foundry Agent Service thread. A Foundry model deployment returns a typed function-call block; the orchestrator validates the call against the toolbox policy and the tool schema, then runs the `get_order_status` activity function under an Entra ID managed identity with scoped read. The typed tool result returns to the model, which steps or answers. When the trajectory must survive a host restart, a Durable Functions orchestrator owns the loop and checkpoints the step count; otherwise the Agent Service thread holds it. The trajectory is emitted to Application Insights and scored by Foundry's multi-turn evaluation.

## Comparison

| Dimension | AWS | Azure |
|-----------|-----|-------|
| Managed agent runtime | Bedrock AgentCore (runtime instances, long sessions) | Foundry Agent Service (threads, tool policy) |
| Loop host for durability | Lambda durable functions (checkpointing) | Durable Functions (replay-safe orchestrator) |
| Typed tool contract | Bedrock `tool_use` / `tool_result` blocks | Foundry function-call blocks |
| Tool curation | Small curated set; AgentCore Gateway | Foundry Toolboxes behind one MCP endpoint |
| Scoped credentials | STS `GetScopedCredentials`; AgentCore Identity | Entra ID managed identity / Entra Agent ID |
| Pre-execution gate | Inline policy check + Bedrock Guardrails | Toolbox policy + schema validation |
| Sandbox for agent code | Lambda MicroVMs | Container Apps sandbox / isolated compute |
| Tool traj telemetry | CloudWatch / AgentCore Observability | Application Insights + multi-turn evaluation |
| Typical lock-in | AgentCore session model, Gateway tool config | Agent Service thread model, Toolbox/MCP config |

> **Open question (from ADR/brief):** no source compares AgentCore runtime instances, Lambda durable functions and Foundry hosted agents for a tool loop, and no source publishes the added latency of an inline tool-call policy check per step. W19, W23 and W38 are the weeks scheduled to settle the runtime question. Do not state a winner here.

## Indicative cost (1,000 runs)

Assumptions: a small model; the request averages ~50 tokens, the system prompt plus tool definitions ~450 tokens (the `tools` parameter is re-sent every step), and each step adds a `tool_use` block plus a `tool_result` block. Cost is model tokens, not compute — the Lambda/Function hop and the identity check are negligible beside them.

| Cloud | Est. USD (order of magnitude) | Multiplier vs a fixed chain |
|-------|-------------------------------|-----------------------------|
| AWS | ~single-digit dollars per 1,000 runs | 1 step when the request carries its facts; 2 steps when a lookup is needed |
| Azure | ~single-digit dollars per 1,000 runs | same call shape, so the same multiple |

The multiplier is the number that matters. Anthropic's tool-use page counts tool-use overhead in three places — the `tools` parameter in every request, `tool_use` blocks in requests and responses, and `tool_result` blocks sent back — plus a per-model tool-use system prompt (about 286 tokens on current Opus/Sonnet/Haiku generations, higher on older ones). A lookup-free request costs one call; a request that needs the lookup costs two, and it pays the tool overhead each time. The saving over a fixed chain (w02) is the fraction of requests that carry their own facts: on those, the loop answers in one call where the chain would have paid for the tool anyway. Measure that fraction on the fixed chain before you budget the loop.

## Portability notes

- The typed tool contract is the portable part: execute the model's `tool_use`/function-call block and return a typed result. Never parse the model's prose for a call.
- The stop rule belongs in your code. AgentCore sessions, Durable Functions and a plain `for` loop can all carry it; the `for` loop has the least lock-in if the reply is short-lived.
- Keep the tool set small and the descriptions current. Argument accuracy degrades as the surface grows (Gorilla, ToolLLM both needed an API retriever); a curated tool kit or toolbox is the managed answer to the same problem.
- Scope the loop's identity down: read-only where possible, short-lived credentials, a check on the proposed call before execution. This is the control set the "a valid OAuth token implies user intent" model no longer provides.
- Keep writes out of the loop. The loop gathers facts; a refund or a send stays behind the existing approval gate.
- **Verify docs** before quoting a per-service price or a renamed service; the agent-runtime names in this table moved this month (Bedrock Agents → Agents Classic; AgentCore runtime instances to GA).
