# Cloud mapping — Augmented LLM

## Cloud-agnostic core

Single orchestration function: `retrieve(query) → context`, `llm.complete(system, user+context)`, optional `tool.execute()` with policy check.

## AWS

| Component | Service | Notes |
|-----------|---------|-------|
| Model | Amazon Bedrock (Claude, Nova, etc.) | Model ID pinned per environment |
| Retrieval | Bedrock Knowledge Bases + OpenSearch Serverless / S3 vectors | Sync jobs for doc corpus |
| Tool execution | Lambda behind AgentCore Gateway or direct SDK | IAM role per tool |
| Guardrails | Bedrock Guardrails | Block PII patterns on output |
| Observability | CloudWatch + OTel via AgentCore Observability | Token/cost tags |

### AWS diagram notes

Client → API Gateway → Lambda orchestrator → Knowledge Base retrieve → Bedrock InvokeModel → optional Lambda tool.

## Azure

| Component | Service | Notes |
|-----------|---------|-------|
| Model | Azure OpenAI / Foundry Models | Deployment name versioning |
| Retrieval | Azure AI Search (vector + semantic) | Index from blob storage |
| Tool execution | Azure Functions | Managed identity to downstream APIs |
| Safety | Azure AI Content Safety + Prompt Shields | Input/output scanning |
| Observability | Application Insights + Foundry tracing | Custom dimensions per tenant |

### Azure diagram notes

Client → APIM → Functions orchestrator → AI Search → chat completions → optional Functions tool.

## Comparison

| Dimension | AWS | Azure |
|-----------|-----|-------|
| Managed RAG | Knowledge Bases integrated with Bedrock | AI Search mature for hybrid search |
| Agent runtime | Optional AgentCore for later upgrade | Foundry Agent Service for later upgrade |
| Identity | IAM + Cognito patterns | Entra ID + managed identity |

## Indicative cost (1,000 runs)

Assumptions: 2k input tokens, 500 output, 1 retrieval, mid-tier model, small index.

| Cloud | Est. USD |
|-------|----------|
| AWS | 3–15 |
| Azure | 3–15 |

Verify with current pricing calculators.

## Portability notes

- Keep orchestration in `core/`; swap `aws/` and `azure/` adapters
- Store prompts versioned in git; avoid vendor-specific prompt DSL in core
