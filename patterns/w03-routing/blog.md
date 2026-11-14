---
title: "Routing: fast model for easy tickets, capable model for hard ones"
description: "Heuristic model routing after prompt chaining — before gateways and caching."
pubDate: 2026-11-14
patternWeek: w03
level: Foundation
acmeStage: w03
spineLayers: "1,2"
---

When the w02 chain works, the next question is cost: should every ticket pay for the most capable model? Usually not. Routing sends the easy majority to a cheap, fast model and reserves the expensive one for cases that need it—after prompt chaining, not before.

## Prerequisites

[w02 prompt chaining](/blog/w02-prompt-chaining/). The chain must classify intent and retrieve context first.

## Context

**Acme Manufacturing** (fictional) now classifies each ticket (billing, product, other) and answers from a retrieved policy snippet. Most tickets are short FAQs; a minority are long, ambiguous, or dispute-related, and those are where a stronger model earns its cost. The question: can Acme serve the easy majority with a smaller model and spend the capable model only where it matters? This stage sits on spine **layers 1 and 2**.

## Pattern

Route after classify and retrieve, not before. The intent label is a free signal.

1. Classify the ticket intent. Call `classify_intent()`.
2. Retrieve the policy snippet.
3. Score the ticket for complexity. Use cheap heuristics only.
4. Select the model. Use the fast model when the score is low. Use the capable model when the score is high.
5. Answer with the intent prompt and the retrieved context.
6. Log the chosen route. Track quality per path before you trust the split.

The heuristics stay small. The isolated sample (`patterns/w03-routing/code/core/pattern.py`) uses `is_complex()`: True when the question is longer than 15 words or contains "dispute". The Acme spine (`projects/acme-support/core/support.py`) uses `_is_complex(question, intent)`: True when intent is `"other"`, when the question is longer than 18 words, or when it contains "dispute" or "exception". The thresholds differ on purpose—the spine sees an intent label, the sample does not.

## Scenario ladder

This week ships the heuristic router; a learned router or gateway and a fast→capable cascade ship in w35. Single-model serving (w01–w02) stays valid at low volume.

| Variant | When you need it | Week |
|---------|------------------|------|
| Heuristic router | Predictable FAQ vs hard cases | w03 (now) |
| Learned router / gateway | Production traffic | w35 |
| Cascade (fast → capable) | Cost at scale | w35 |

## When not to use

- You cannot measure answer quality per path. Routing on vibes hides fast-path regressions.
- Volume is low. Premium-everywhere is cheaper than the engineering time to tune heuristics.
- Compliance pins one model version for every request.

## Apply it to Acme

Stage w03 adds `route_and_answer()` to `projects/acme-support/core/support.py`. It classifies intent, retrieves context, then `_is_complex(question, intent)` selects `CapableMockLLM` or `FastMockLLM` before `answer_for_intent()` runs. The tool-blocking rule carries over from w02.

Run the tests:

```bash
cd projects/acme-support && uv sync --extra dev && uv run pytest
```

Check out the frozen snapshot: `git fetch --tags && git checkout stage-w03`.

## Architect's notebook

| Field | Notes |
|-------|-------|
| Decision | Route simple FAQs to the fast mock model; route long, ambiguous, or dispute tickets to the capable model |
| Rejected alternative | Premium model for every ticket—fine at low volume, wasteful at scale |
| Top failure mode | A complex question scores as simple and gets a weak answer, silently |
| Cost hint | Order-of-magnitude 3–10× cheaper on the fast path |
| NFRs | p95 latency on the simple path; per-path quality tracking; log the chosen route |

## Reference implementation

- **Pattern sample:** [`patterns/w03-routing/code/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/patterns/w03-routing/code) — `is_complex()` and `route_and_complete()`, with two mock models
- **Acme spine:** [`projects/acme-support/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/projects/acme-support) — the same idea after the w02 chain

Tests run without cloud API keys.

## AWS mapping

Typical services (verify names in current docs):

- **Amazon Bedrock** for generation—a cheap model id on the fast route, a stronger id on the capable route
- **Lambda** for the router rules that run after the chain
- **API Gateway** for separate quotas per route

Flow: API Gateway → orchestrator Lambda → classify/retrieve → route → `InvokeModel`.

## Azure mapping

Typical services (verify names in current docs):

- **Azure OpenAI** or **Foundry** with two deployments: one fast, one capable
- **APIM** policy routes by header or by the classifier output
- **Azure Functions** for the router rules

Flow: APIM → router function → select deployment → chat completion.

## Production checklist

Before production, walk the [Production Readiness Checklist](/production-readiness-checklist/)—golden tests per path, cost caps, tracing, rollback.

## Further reading

- [w02 prompt chaining](/blog/w02-prompt-chaining/) — the chain this pattern routes on
- Anthropic — building effective agents (pattern maturity ladder)
- AWS Bedrock and Azure Foundry documentation (verify current service names)

## Disclaimer

Views and examples are my own, for learning purposes, and do not represent my employer.
