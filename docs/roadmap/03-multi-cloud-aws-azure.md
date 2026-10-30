# Multi-cloud: AWS and Azure

Every pattern includes `cloud-mapping.md` with cloud-agnostic core first, then mappings below.

## Service map

| Concern | AWS | Azure |
|---------|-----|-------|
| Models | Amazon Bedrock | Azure OpenAI / Foundry Models |
| Managed agent runtime | Bedrock AgentCore, Bedrock Agents | Azure AI Foundry Agent Service |
| Agent SDKs | Strands Agents | Microsoft Agent Framework |
| RAG | Bedrock Knowledge Bases, OpenSearch Serverless | Azure AI Search |
| Guardrails | Bedrock Guardrails | AI Content Safety, Prompt Shields |
| Orchestration / events | Step Functions, EventBridge, SQS | Durable Functions, Logic Apps, Event Grid, Service Bus |
| Identity | IAM, Cognito, AgentCore Identity | Entra ID, Entra Agent ID, managed identities |
| MCP / tools | AgentCore Gateway, Lambda | API Management (MCP), Azure Functions |
| Observability / evals | CloudWatch, X-Ray, AgentCore Observability | Application Insights, Foundry tracing/evals |
| IaC | Terraform (`infra/templates/aws/`) | Bicep (`infra/templates/azure/`) |

Service names change frequently. CloudMapper skill must verify current docs each week.

## Sandbox rules

1. Use **personal** AWS and Azure accounts only.
2. Set **$5 budget alerts** before first deploy.
3. Every demo has a **`destroy`** step — tear down same day.
4. No production data; synthetic fixtures only.
5. Document indicative cost per 1,000 agent runs in `cloud-mapping.md`.

## Code layout (per pattern)

```text
patterns/wNN-slug/code/
  core/       # cloud-agnostic logic
  aws/        # Bedrock / AgentCore adapters (stubs OK early Year 1)
  azure/      # Foundry / Agent Framework adapters
  tests/
```

Run locally with **mock LLM** — no cloud keys required for CI.

## Monthly sandbox day

Deploy one flagship component to AWS *or* Azure, record a 2-minute demo, destroy resources.
