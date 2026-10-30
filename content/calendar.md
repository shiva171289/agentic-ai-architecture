# 52-week pattern calendar

Status column: `planned` | `draft` | `published`. AWS/Azure mapping themes in **Mapping focus** (details in each `cloud-mapping.md`).

**Running use-case:** [Acme Support Platform](../docs/roadmap/07-running-use-case.md) — one evolving system in `projects/acme-support/` (split → `acme-agentic-support` at W13).

**Releases:** Acme v1 (W13) · Acme v2 (W26) · Acme v3 (W39) · Acme v4 (W46) · F5 governance (W52)

| Week | Slug | Pattern | Level | Acme stage (summary) | Mapping focus | Release |
|------|------|---------|-------|----------------------|---------------|---------|
| w01 | augmented-llm | Augmented LLM | Foundation | FAQ + naive policy retrieval | Bedrock vs Foundry models | |
| w02 | prompt-chaining | Prompt chaining | Foundation | Classify → answer chain | Invocation pipelines | |
| w03 | routing | Routing | Foundation | Fast vs capable model routes | Model router / gateway | |
| w04 | parallelization | Parallelization | Foundation | Parallel policy + order fetch | Concurrent invokes | |
| w05 | orchestrator-workers | Orchestrator-workers | Foundation | Orchestrator + lookup worker | Step Functions vs Durable Functions | |
| w06 | evaluator-optimizer | Evaluator-optimizer (+ reflection) | Foundation | Draft → policy critic → rewrite | Online eval hooks | |
| w07 | react | ReAct loop | Foundation | ReAct before order tool | Tool use runtimes | |
| w08 | plan-and-execute | Plan-and-execute | Foundation | Plan replacement-part flow | Long-running planners | |
| w09 | agent-or-workflow | Agent or workflow? (decision framework) | Foundation | Architect doc: workflow vs agent | Decision criteria | |
| w10 | tool-calling | Tool calling | Foundation | `get_order_status` tool | Lambda vs Functions | |
| w11 | mcp-servers | MCP servers | Foundation | Order/CRM MCP registry | AgentCore Gateway vs APIM MCP | |
| w12 | agentic-rag | Agentic RAG | Foundation | Agent chooses when to search | Knowledge Bases vs AI Search | |
| w13 | memory-context | Memory & context engineering | Foundation | Customer thread memory | AgentCore Memory vs Foundry threads | **Acme v1 split** |
| w14 | q1-retrospective | Q1 retrospective + design challenge | Foundation | Returns at 10× volume challenge | Quarter round-up | buffer |
| w15 | supervisor | Supervisor pattern | Practitioner | Supervisor → specialists | Multi-agent runtime | |
| w16 | hierarchical-teams | Hierarchical teams | Practitioner | Warranty dispute sub-team | Nested orchestration | |
| w17 | handoff-swarm | Handoff & swarm | Practitioner | Hand off to human | Session handoff | |
| w18 | blackboard | Blackboard | Practitioner | Shared refund investigation board | Shared state store | |
| w19 | long-running-background-agents | Long-running background agents | Practitioner | Durable case agent + resume | Checkpoints / events | |
| w20 | a2a-protocol | Agent-to-agent (A2A) | Practitioner | Typed inter-agent messages | Inter-agent APIs | |
| w21 | event-driven-agents | Event-driven agents | Practitioner | Ticket-created workflow | EventBridge vs Event Grid | |
| w22 | saga-compensation | Saga & compensation | Practitioner | Refund + reship saga | Step Functions sagas | |
| w23 | durable-execution | Durable execution | Practitioner | Checkpoint saga steps | Checkpoints / Durable Functions | |
| w24 | human-in-the-loop | Human-in-the-loop | Practitioner | High-value refund approval | Approval workflows | |
| w25 | kg-rag | Knowledge-graph RAG | Practitioner | Product–symptom–policy graph | Neptune vs Cosmos DB | |
| w26 | multi-agent-reference | Multi-agent reference architecture | Practitioner | End-to-end multi-agent map | End-to-end map | **Acme v2 split** |
| w27 | q2-retrospective | Q2 retrospective + design challenge | Practitioner | Multi-agent failure modes | Quarter round-up | buffer |
| w28 | prompt-injection-defense | Prompt injection defense | Production | Sanitize customer email | Guardrails vs Prompt Shields | |
| w29 | least-privilege-tools | Least-privilege tools | Production | Role-scoped tools | Scoped IAM / RBAC | |
| w30 | agent-identity | Agent identity | Production | Service principal + audit actor | AgentCore Identity vs Entra Agent ID | |
| w31 | mcp-gateways | MCP gateways | Production | Central MCP gateway | Gateway patterns | |
| w32 | offline-evals | Offline evaluations | Production | Golden refund/policy set | Eval datasets | |
| w33 | online-evals | Online evaluations | Production | Production regression sampling | Production eval hooks | |
| w34 | otel-tracing | OpenTelemetry tracing | Production | Trace supervisor → tools | CloudWatch/X-Ray vs App Insights | |
| w35 | model-routing-cost | Model routing & cost | Production | Cache + tiered models | Caching, tiered models | |
| w36 | reliability-fallbacks | Reliability & fallbacks | Production | Circuit breaker degraded mode | Circuit breakers | |
| w37 | agent-cicd | Agent CI/CD | Production | Eval gates in pipeline | Pipeline gates | |
| w38 | managed-runtime-showdown | AgentCore vs Foundry Agent Service | Production | Managed runtime sketch | Managed runtime compare | |
| w39 | finance-workflow-reference | Finance workflow reference | Production | Refund → finance handoff | End-to-end map | **Acme v3 split** |
| w40 | q3-retrospective | Q3 retrospective + design challenge | Production | Cost vs quality SLA | Quarter round-up | buffer |
| w41 | procure-to-pay-agent | Procure-to-pay agent | Architect | Replacement-part PO | ERP APIs (fictional Acme) | |
| w42 | finance-reconciliation | Finance reconciliation | Architect | Refund batch reconcile | Batch + agent | |
| w43 | inventory-planning | Inventory & planning | Architect | Spares from ticket trends | Planning agents | |
| w44 | compliance-audit-agent | Compliance & audit | Architect | Immutable refund audit | Audit trails | |
| w45 | erp-mcp-integration | ERP integration via MCP | Architect | ERP via MCP | SAP/D365 angles (generic) | |
| w46 | agentic-erp-reference | Agentic ERP reference architecture | Architect | Full back-office map | Full ERP layer map | **Acme v4 split** |
| w47 | governance-registry | Agent governance registry | Architect | Agent registry | Registry + policy | F5 start |
| w48 | policy-enforcement | Policy enforcement | Architect | Fleet policy engine | OPA-style patterns | F5 |
| w49 | computer-use-agents | Computer-use agents (legacy UI) | Architect | ERP screen automation stub | Desktop automation patterns | F5 |
| w50 | audit-observability | Audit & observability | Architect | Fleet audit search | Immutable logs | F5 |
| w51 | multi-cloud-reference | Multi-cloud reference | Architect | AWS + Azure together | AWS + Azure together | F5 |
| w52 | year-retrospective | Year in patterns | Architect | Annual round-up | Annual round-up | **F5 split** |

## Hermes content factory repo

Target **~Month 3**: extract [hermes/skills](../hermes/skills/) to `shiva171289/hermes-content-factory`.

## Notes

- Rename slugs when creating folders: `patterns/w01-augmented-llm/`
- Buffer weeks still get a short post (retrospective / budget review / design challenge)
- **Pattern Radar:** first Friday of each month → `content/radar/YYYY-MM.md` (see [07-running-use-case.md](../docs/roadmap/07-running-use-case.md))
