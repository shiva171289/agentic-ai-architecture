---
title: "Augmented LLM: the pattern most teams should ship first"
description: "Start with search-then-answer: retrieval, a clear prompt, and optional tools—before a full autonomous agent."
pubDate: 2026-10-30
patternWeek: w01
level: Foundation
acmeStage: w01
---

When leadership asks for an “AI agent,” the safest first step is usually an **augmented LLM**: find relevant text, put it in the prompt, get one answer. Optional tools come later. It is like giving a new support rep a **highlighted manual page** instead of letting them wander the warehouse alone.

## Prerequisites

None. If vocabulary is new, read [Start Here](/start-here/) first.

## Context

**Acme Manufacturing** (fictional) sells hardware online. They want natural-language answers from public product docs, with a path to create support tickets later. The architecture question: what is the **smallest** system we can test, observe, and afford?

## Pattern

Follow this recipe (fixed order):

1. **Retrieve** snippets from an approved document set (keyword or vector search).
2. **Compose** one user message that includes those snippets and clear answer rules (“cite the doc”, “say I don’t know if missing”).
3. **Generate** a single model reply (or a short chain: classify → answer).
4. **Optionally call tools** with tight permissions and approval rules.

Add ReAct loops or multi-agent setups only when metrics show this single pass is not enough.

## When not to use

Skip this as the main product when:

- The task needs many branching tool calls or long-running planning.
- Compliance requires fully deterministic output with zero generative variation.
- Search indexes are stale and nobody owns refresh.

Fix data and process first—or use a workflow engine instead of a bigger prompt.

## Apply it to Acme

**Stage w01** in the [Acme Support project](https://github.com/shiva171289/agentic-ai-architecture/tree/main/projects/acme-support): load synthetic policies from `data/policies.json`, run simple keyword retrieval, and answer FAQs with a fixed system prompt. Ticket creation stays disabled until a later week.

Check out the frozen week snapshot: `git fetch --tags && git checkout stage-w01`.

To run tests locally:

```bash
cd projects/acme-support && uv sync --extra dev && uv run pytest
```

See [STAGES.md on GitHub](https://github.com/shiva171289/agentic-ai-architecture/blob/main/projects/acme-support/STAGES.md) for the week-by-week changelog.

## Architect's notebook

| Field | Notes |
|-------|--------|
| Decision | Ship augmented LLM before any agent loop for Acme tier-1 FAQs |
| Rejected alternative | Full ReAct agent on day one — harder to test and observe |
| Top failure mode | Wrong retrieval → confident wrong answer |
| Cost hint | Roughly $0.50–$2 per 1k FAQ turns (one small model call + search) |
| NFRs | p95 latency under ~3s; accurate policy quotes; log which snippets were used |

## Reference implementation

- **Pattern sample:** [`patterns/w01-augmented-llm/code/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/patterns/w01-augmented-llm/code) — minimal isolated demo
- **Acme spine:** [`projects/acme-support/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/projects/acme-support) — same idea with JSON policy data

Tests run without cloud API keys.

## AWS mapping

Typical services (verify names in current docs):

- **Amazon Bedrock** for generation
- **Knowledge Bases** for managed RAG over S3 or OpenSearch
- **Lambda** (or **AgentCore Gateway**) for tools with scoped IAM
- **Bedrock Guardrails** for output filtering

Flow: API Gateway → orchestrator Lambda → retrieve → `InvokeModel` → optional tool Lambda.

## Azure mapping

Typical services (verify names in current docs):

- **Azure OpenAI** or **Foundry** chat deployments
- **Azure AI Search** for hybrid retrieval
- **Azure Functions** for tools with managed identity
- **Content Safety / Prompt Shields** for scanning

Flow: APIM → Functions orchestrator → search → chat completion → optional tool function.

## Production checklist

Before production, walk the [Production Readiness Checklist](/production-readiness-checklist/)—golden tests, tool permissions, tracing, cost caps, rollback.

## Further reading

- Anthropic — building effective agents (pattern maturity ladder)
- AWS Bedrock and Azure Foundry documentation (verify current service names)

## Disclaimer

Views and examples are my own, for learning purposes, and do not represent my employer.
