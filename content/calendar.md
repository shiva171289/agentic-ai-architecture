# 52-week pattern calendar

Status column: `planned` | `draft` | `published`. AWS/Azure mapping themes in **Mapping focus** (details in each `cloud-mapping.md`).

**Flagships:** F1 customer support (Q1) · F2 multi-agent enterprise (Q2) · F3 finance workflow (Q3) · F4 ERP · F5 governance (Q4)

| Week | Slug | Pattern | Mapping focus | Flagship |
|------|------|---------|---------------|----------|
| w01 | augmented-llm | Augmented LLM | Bedrock vs Foundry models | |
| w02 | prompt-chaining | Prompt chaining | Invocation pipelines | |
| w03 | routing | Routing | Model router / gateway | |
| w04 | parallelization | Parallelization | Concurrent invokes | |
| w05 | orchestrator-workers | Orchestrator-workers | Step Functions vs Durable Functions | |
| w06 | evaluator-optimizer | Evaluator-optimizer | Online eval hooks | |
| w07 | react | ReAct loop | Tool use runtimes | |
| w08 | plan-and-execute | Plan-and-execute | Long-running planners | |
| w09 | reflection | Reflection / self-critique | Trace + replay | |
| w10 | tool-calling | Tool calling | Lambda vs Functions | |
| w11 | mcp-servers | MCP servers | AgentCore Gateway vs APIM MCP | |
| w12 | agentic-rag | Agentic RAG | Knowledge Bases vs AI Search | |
| w13 | memory-context | Memory & context engineering | AgentCore Memory vs Foundry threads | **F1 split** |
| w14 | q1-retrospective | Q1 retrospective | Quarter round-up | buffer |
| w15 | supervisor | Supervisor pattern | Multi-agent runtime | F2 start |
| w16 | hierarchical-teams | Hierarchical teams | Nested orchestration | F2 |
| w17 | handoff-swarm | Handoff & swarm | Session handoff | F2 |
| w18 | blackboard | Blackboard | Shared state store | F2 |
| w19 | debate-consensus | Debate / consensus | Multi-model vote | F2 |
| w20 | a2a-protocol | Agent-to-agent (A2A) | Inter-agent APIs | F2 |
| w21 | event-driven-agents | Event-driven agents | EventBridge vs Event Grid | F2 |
| w22 | saga-compensation | Saga & compensation | Step Functions sagas | F2 |
| w23 | durable-execution | Durable execution | Checkpoints / Durable Functions | F2 |
| w24 | human-in-the-loop | Human-in-the-loop | Approval workflows | F2 |
| w25 | kg-rag | Knowledge-graph RAG | Neptune vs Cosmos DB | F2 |
| w26 | multi-agent-reference | Multi-agent reference architecture | End-to-end map | **F2 split** |
| w27 | q2-retrospective | Q2 retrospective | Quarter round-up | buffer |
| w28 | prompt-injection-defense | Prompt injection defense | Guardrails vs Prompt Shields | F3 start |
| w29 | least-privilege-tools | Least-privilege tools | Scoped IAM / RBAC | F3 |
| w30 | agent-identity | Agent identity | AgentCore Identity vs Entra Agent ID | F3 |
| w31 | mcp-gateways | MCP gateways | Gateway patterns | F3 |
| w32 | offline-evals | Offline evaluations | Eval datasets | F3 |
| w33 | online-evals | Online evaluations | Production eval hooks | F3 |
| w34 | otel-tracing | OpenTelemetry tracing | CloudWatch/X-Ray vs App Insights | F3 |
| w35 | model-routing-cost | Model routing & cost | Caching, tiered models | F3 |
| w36 | reliability-fallbacks | Reliability & fallbacks | Circuit breakers | F3 |
| w37 | agent-cicd | Agent CI/CD | Pipeline gates | F3 |
| w38 | managed-runtime-showdown | AgentCore vs Foundry Agent Service | Managed runtime compare | F3 |
| w39 | finance-workflow-reference | Finance workflow reference | End-to-end map | **F3 split** |
| w40 | q3-retrospective | Q3 retrospective | Quarter round-up | buffer |
| w41 | procure-to-pay-agent | Procure-to-pay agent | ERP APIs (fictional Acme) | F4 |
| w42 | finance-reconciliation | Finance reconciliation | Batch + agent | F4 |
| w43 | inventory-planning | Inventory & planning | Planning agents | F4 |
| w44 | compliance-audit-agent | Compliance & audit | Audit trails | F4 |
| w45 | erp-mcp-integration | ERP integration via MCP | SAP/D365 angles (generic) | F4 |
| w46 | agentic-erp-reference | Agentic ERP reference architecture | Full ERP layer map | **F4 split** |
| w47 | governance-registry | Agent governance registry | Registry + policy | F5 |
| w48 | policy-enforcement | Policy enforcement | OPA-style patterns | F5 |
| w49 | approval-workflows | Approval workflows | Human gates | F5 |
| w50 | audit-observability | Audit & observability | Immutable logs | F5 |
| w51 | multi-cloud-reference | Multi-cloud reference | AWS + Azure together | F5 |
| w52 | year-retrospective | Year in patterns | Annual round-up | **F5 split** |

## Hermes content factory repo

Target **~Month 3**: extract [hermes/skills](../hermes/skills/) to `shiva171289/hermes-content-factory`.

## Notes

- Rename slugs when creating folders: `patterns/w01-augmented-llm/`
- Buffer weeks still get a short post (retrospective / budget review)
