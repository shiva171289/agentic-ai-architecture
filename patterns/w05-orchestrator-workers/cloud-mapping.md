# Cloud mapping — Orchestrator-workers

## Cloud-agnostic core

The pattern has four moving parts, none of them cloud-specific:

- **Orchestrator** — a model-driven planner. It reads the request and emits a short plan: which parts to delegate and what each worker must return.
- **Worker** — a bounded unit of work (a retrieval or a tool call). Workers are selected by capability, not by a hard-coded name, so the pool can change without changing the planner.
- **Merge** — combines the attributable worker results into one context, then hands it to the existing answer chain.
- **Deterministic spine** — a state-machine runner for the steps that must run in order, with checkpoints so a retried run takes the same path.

The portability question is where the spine lives. Every cloud ships a durable orchestrator (AWS Step Functions, Azure Durable Functions) and an agent runtime (AgentCore, Foundry Agent Service). The worker tool schema, the handover format, and the merge rule are the real contract — they move; the orchestrator library does not.

## AWS

| Component | Service | Notes |
|-----------|---------|-------|
| Model | Amazon Bedrock | Orchestrator plan + worker calls + final synthesis |
| Durable spine | AWS Step Functions | State machine exposed to the agent as MCP tools so "the agent can't skip or reorder" the fixed steps |
| Agent runtime | Amazon Bedrock AgentCore | Hosts the orchestrator; durable, event-driven hosting |
| Workers | AWS Lambda | One function per worker; stateless, bounded |
| State / checkpoints | Step Functions execution history + DynamoDB | Plan and worker results persisted for deterministic replay |
| Identity | IAM roles (per worker) | Workers get least-privilege, read-only credentials |
| Observability | CloudWatch + X-Ray | Trace the plan, each handover, and the merge |

### AWS diagram notes

The orchestrator runs on AgentCore. It calls the Step Functions state machine (via the MCP tool surface) for the ordered spine. The state machine's `Map`/`Parallel` state fans out to Lambda workers. Each worker returns a structured result to the execution history. The merge step reads those results and calls Bedrock once more for the answer.

## Azure

| Component | Service | Notes |
|-----------|---------|-------|
| Model | Azure OpenAI / Microsoft Foundry models | Orchestrator plan + worker calls + final synthesis |
| Durable spine | Durable Functions (Microsoft Agent Framework Durable Extension) | "Deterministic multi-agent orchestrations" that checkpoint and replay |
| Agent runtime | Microsoft Foundry Agent Service | Hosts the orchestrator agent |
| Workers | Azure Functions | One function per worker |
| State / checkpoints | Durable Functions orchestrator/entity state + Cosmos DB | Plan and results persisted for replay |
| Identity | Microsoft Entra ID managed identity | Per-worker scoped permissions |
| Observability | Application Insights | Distributed trace of plan → workers → merge |

### Azure diagram notes

A Durable Functions orchestrator owns the spine and is deterministic by construction: it replays its history on resume. Workers are activity functions. The orchestrator awaits them concurrently, collects results, and performs the merge before the final synthesis call.

## Comparison

| Dimension | AWS | Azure |
|-----------|-----|-------|
| Managed agent runtime | Bedrock AgentCore | Microsoft Foundry Agent Service |
| Durable orchestration engine | Step Functions | Durable Functions / Durable Extension |
| Worker compute | Lambda | Azure Functions |
| Identity | IAM per-worker roles | Entra ID managed identity |
| Typical lock-in | State-machine DSL + AgentCore runtime | Durable orchestrator API + Foundry runtime |

> **Open question (from ADR/brief):** Step Functions vs Durable Functions for agent workers — both ship durable replay; no primary head-to-head comparison exists. Do not state that one is better.

## Indicative cost (1,000 runs)

Assumptions: a run fans out to a mean of **1.6 workers** (the ADR caps fan-out), each worker is one short retrieval call + one orchestrator plan call + one merge/synthesis call at a small model. Model token cost dominates; the compute is small.

| Cloud | Est. USD (order of magnitude) |
|-------|-------------------------------|
| AWS | ~single-digit dollars per 1,000 runs (≈ {1 plan + 1.6 worker + 1 merge} model calls each) |
| Azure | ~single-digit dollars per 1,000 runs (same call shape) |

The differentiator is not the price per call — it is **how many workers each request spawns**. Cap the fan-out and the per-request budget; idle workers are the cost model.

## Portability notes

- The deterministic spine is where lock-in lives: the Step Functions state-machine DSL and the Durable Functions orchestrator API are not portable. Keep the spine thin.
- The worker, tool-schema, and handover contract is portable. Design workers as plain functions behind an interface so a move only rewrites the thin adapter.
- Orchestrator-workers does **not** need a cross-organization protocol. The A2A pattern (OAuth in both directions, no shared secrets) pays for itself only when agents cross an **organizational** boundary; inside one team, a fixed workflow engine is cheaper than a model-driven orchestrator.
- **verify docs** before quoting any per-service price or a renamed service; vendor pricing pages change.
