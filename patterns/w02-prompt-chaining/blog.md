---
title: "Prompt chaining: classify first, answer second"
description: "Split support into intent-specific prompts before you add routers or agents."
pubDate: 2026-11-07
patternWeek: w02
level: Foundation
acmeStage: w02
spineLayers: "2"
---

Most teams do not need an agent to fix a mixed-domain support prompt. They need two prompts. When billing and product questions share one system prompt, policy from one domain leaks into the other, and a single eval set hides *which* slice failed. Prompt chaining splits the task so you can **classify first, answer second**.

## Prerequisites

[Week 1 — Augmented LLM](/blog/w01-augmented-llm/). This post assumes the retrieve-then-answer shape from that week.

## Context

**Acme Manufacturing** (fictional) sells hardware online. Its tickets mix billing language (“refund”, “invoice”) with product language (“reset”, “frozen”). One system prompt blends both policies, so a billing answer can inherit product tone and vice versa. Support leads want **per-intent eval slices**: they need to know a *billing* answer failed, not just that “the bot failed.”

The architecture question: how do we separate intents without adding a router or a full agent? **Spine:** this is Layer 2 — wrapping. The control flow is fixed and written by you, not chosen by the model at runtime.

## Pattern

Follow this recipe in a fixed order.

1. Classify the intent. Use keyword rules or a small model.
2. Retrieve the shared context once.
3. Select the intent-specific system prompt.
4. Answer with that prompt and the shared context.
5. Return the intent label with the answer for audit.

Keep the chain shallow. Add a third step only when metrics show the two-step chain is not enough.

## Scenario ladder

| Variant | When you need it | This week |
|---------|------------------|-----------|
| Classify → answer | Distinct intents, shared corpus | **Yes** |
| Router + model tier | Cost / latency tradeoffs (w03) | Later |
| Parallel context gather | Independent data sources (w04) | Later |

Retrieval stays keyword-only through w01–w04 — see the [retrieval ladder](../../content/topics/retrieval-ladder.md).

## When not to use

- One intent dominates (over ~90% of traffic). The classify step only adds latency.
- Compliance requires a single auditable prompt hash. One prompt artifact is easier to pin.
- The end-to-end latency budget is under ~300 ms. A second step will not fit.
- You have no per-intent golden questions yet. Chaining pays off only when you can score each slice.

## Apply it to Acme

Stage **w02** adds `answer_with_chain()` to `projects/acme-support/core/support.py`. It calls `classify_intent()` (rule-based), retrieves a shared policy snippet, then calls `answer_for_intent()` with one of the `INTENT_PROMPTS` entries for `billing`, `product`, or `other`. `answer_faq()` routes through the chain, and a tool call is blocked unless `allow_tools` is true.

Run the tests:

```bash
cd projects/acme-support && uv sync --extra dev && uv run pytest
```

Check out the frozen snapshot: `git fetch --tags && git checkout stage-w02`.

## Architect's notebook

| Field | Notes |
|-------|-------|
| Decision | Rule-based classify + two intent-specific prompts |
| Rejected alternative | Single mega-prompt — one call, but hard to eval per intent |
| Top failure mode | Mis-routed billing question answered with product policy |
| Cost hint | ~2× a single call if the classify step uses a model; rules keep it at 1 call (Acme uses rules) |
| NFRs | Per-intent eval slices; intent label logged for audit |

## Reference implementation

- **Pattern sample:** [`patterns/w02-prompt-chaining/code/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/patterns/w02-prompt-chaining/code) — `classify_intent`, `retrieve`, `run_chain`
- **Acme spine:** [`projects/acme-support/core/support.py`](https://github.com/shiva171289/agentic-ai-architecture/blob/main/projects/acme-support/core/support.py) — `answer_with_chain` against synthetic policy data

Tests run without cloud API keys.

## AWS mapping

Typical services (verify names in current docs):

- **Step Functions Express** (or a Lambda sequence) for the chain, one state per step
- **Bedrock** `InvokeModel` for the classify step — optional, small model
- **Bedrock** `InvokeModel` for the answer step, a separate prompt template per intent

Flow: API Gateway → Lambda → classify → retrieve → `InvokeModel` per intent.

## Azure mapping

Typical services (verify names in current docs):

- **Durable Functions** (or **Logic Apps**) for sequential chain activities
- **Prompt Flow** / **Foundry** prompt templates, versioned per intent
- **Foundry** chat deployment for the answer step

Flow: APIM → Durable Functions → retrieve → chat completion per intent.

## Production checklist

Before production, walk the [Production Readiness Checklist](/production-readiness-checklist/)—golden tests per intent, tracing, cost caps, rollback.

## Further reading

- Anthropic — [building effective agents](https://www.anthropic.com/research/building-effective-agents) (prompt-chaining section)
- LangChain — context engineering for multi-step prompts
- This repo — [patterns/w02-prompt-chaining/adr.md](https://github.com/shiva171289/agentic-ai-architecture/blob/main/patterns/w02-prompt-chaining/adr.md)

## Disclaimer

Views and examples are my own, for learning purposes, and do not represent my employer.
