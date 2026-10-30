# Agentic AI production readiness checklist

Use before calling any agent workflow "production". Fictional examples only.

## Use case & design

- [ ] Problem cannot be solved cheaper with rules, search, or workflow engine
- [ ] Success metrics defined (quality, latency, cost per task)
- [ ] Human escalation path documented
- [ ] "When not to use agent" documented in ADR

## Data & context

- [ ] Data sources licensed for intended use
- [ ] PII handling and retention defined
- [ ] Context window strategy (trim, summarize, retrieve)
- [ ] RAG eval set with known answers (if RAG)

## Tools & integration

- [ ] Tools follow least privilege (scoped credentials)
- [ ] MCP/API timeouts and idempotency considered
- [ ] Side effects require approval where needed

## Security

- [ ] Prompt injection mitigations (input filtering, tool isolation)
- [ ] Output filtering for sensitive data
- [ ] Secrets in vault/parameter store, not in prompts
- [ ] Guardrails / content safety configured (Bedrock Guardrails or Azure Prompt Shields)

## Identity

- [ ] Agent identity separate from end-user identity
- [ ] Audit log ties actions to agent + user + session

## Evaluation & quality

- [ ] Offline eval suite in CI
- [ ] Canary or shadow traffic plan for online eval
- [ ] Regression triggers on model/prompt change

## Observability & cost

- [ ] Distributed tracing (OpenTelemetry) with LLM spans
- [ ] Cost per task tracked by tenant/use case
- [ ] Alerts on error rate, latency, spend anomalies

## Operations

- [ ] Versioned prompts and models
- [ ] Rollback procedure tested
- [ ] Runbooks for provider outage (fallback model)
- [ ] `destroy` script for cloud sandboxes after demos

## Multi-cloud notes

- [ ] AWS and Azure mappings documented if deploying to either
- [ ] Vendor lock-in risks acknowledged in ADR

---

**Newsletter:** offer this checklist as a PDF/email signup on the blog.

**License:** CC BY 4.0 (see LICENSE-content)
