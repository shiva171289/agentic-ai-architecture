---
title: "Augmented LLM: the pattern most teams should ship first"
description: "Cloud-agnostic augmented LLM with retrieval and guarded tools, mapped to AWS Bedrock and Azure AI Foundry."
pubDate: 2026-10-30
patternWeek: w01
level: Foundation
acmeStage: w01
---

Most enterprise “agent” projects should start as an **augmented LLM**: retrieval plus a structured prompt plus optional tools—not a open-ended autonomous loop.

## Prerequisites

None — start here, or read [Start Here](/start-here/) for vocabulary and the Acme storyline.

## Context

Fictional **Acme Manufacturing** wants natural-language answers over public product documentation, with a controlled path to create support tickets. Leadership asked for an “AI agent.” Architecture review question: what is the **minimum** intelligence layer that is testable, observable, and affordable?

## Pattern

1. **Retrieve** relevant passages from an approved corpus (vector or hybrid search).
2. **Compose** a single user message that includes retrieved context and explicit answer rules.
3. **Generate** one model response (or a fixed two-step chain for classification → answer).
4. **Optionally invoke tools** with least privilege and policy gates.

This is not anti-agent—it is **honest sequencing**. You add ReAct loops or multi-agent orchestration when metrics show single-pass augmentation fails.

## When not to use

Skip augmentation-as-product when:

- The task needs many branching tool calls or multi-hour planning.
- Compliance requires fully deterministic behavior with zero generative variance.
- The retrieval index is stale and nobody owns refresh SLAs.

In those cases, fix data/process first—or choose workflow engines, not bigger prompts.

## Apply it to Acme

**Stage w01** in [`projects/acme-support/`](../../projects/acme-support/): load synthetic policies from `data/policies.json`, run naive keyword retrieval, and answer FAQs with a fixed system prompt. Ticket creation stays blocked until a later week enables tools.

Checkout tag `stage-w01` (when published) or run:

```bash
cd projects/acme-support && uv sync --extra dev && uv run pytest
```

See [STAGES.md](../../projects/acme-support/STAGES.md) for the running changelog.

## Architect's notebook

| Field | Notes |
|-------|--------|
| Decision | Ship augmented LLM before any agent loop for Acme tier-1 FAQs |
| Rejected alternative | Full ReAct agent on day one — harder to test and observe |
| Top failure mode | Stale or wrong retrieval sends confident wrong answers |
| Cost hint | ~$0.50–$2 per 1k FAQ turns (single small model call + search) |
| NFRs | Latency (p95 &lt; 3s), accuracy on policy quotes, audit of retrieved snippet |

## Reference implementation

- **Pattern sample:** [`patterns/w01-augmented-llm/code/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/patterns/w01-augmented-llm/code) — minimal isolated demo
- **Acme spine:** `projects/acme-support/` — same pattern with JSON policy corpus

Tests run without cloud credentials.

## AWS mapping

Typical stack:

- **Amazon Bedrock** for generation (pin model IDs per environment).
- **Knowledge Bases** for managed RAG over S3/OpenSearch vectors.
- **Lambda** (or **AgentCore Gateway**) for tool execution with scoped IAM.
- **Bedrock Guardrails** for output filtering.

Flow: API Gateway → Lambda orchestrator → retrieve → `InvokeModel` → optional tool Lambda.

## Azure mapping

Typical stack:

- **Azure OpenAI** or **Foundry** chat models (version deployments).
- **Azure AI Search** for hybrid retrieval.
- **Azure Functions** for tools with managed identity.
- **Content Safety / Prompt Shields** for scanning.

Flow: APIM → Functions orchestrator → search → chat completion → optional tool function.

## Production checklist

Before production, walk the [Production Readiness Checklist](/production-readiness-checklist/): eval golden set, tool permissions, tracing, cost caps, rollback.

## Further reading

- Anthropic — building effective agents (pattern maturity ladder)
- AWS Bedrock and Azure Foundry documentation (verify current service names)

## Disclaimer

Views and examples are my own, for learning purposes, and do not represent my employer.
