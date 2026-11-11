---
title: "Prompt chaining: classify first, answer second"
description: "Split support into intent-specific prompts before you add routers or agents."
pubDate: 2026-11-07
patternWeek: w02
level: Foundation
acmeStage: w02
spineLayers: "2"
---

## Prerequisites

[Week 1 — Augmented LLM](/blog/w01-augmented-llm/).

## Context

Acme tickets mix billing and product language. One system prompt blends policies. Chaining gives you **per-intent eval slices** without a full agent.

**Spine:** Layer 2 — wrapping (fixed control flow, not model-chosen).

## Pattern

1. Classify intent (rules or small model).
2. Retrieve shared context.
3. Call answer step with **intent-specific** system prompt.

## Scenario ladder

| Variant | This week |
|---------|-----------|
| Classify → answer | **Yes** |
| Model routing (w03) | Later |
| Parallel gather (w04) | Later |

See [retrieval ladder](../../content/topics/retrieval-ladder.md) — retrieval stays keyword in w01–w04.

## When not to use

Skip chaining when intent is uniform or latency budget forbids two steps.

## Apply it to Acme

`projects/acme-support/core/support.py` adds `classify_intent`, `answer_with_chain`, and billing vs product system prompts.

## Architect's notebook

| Field | Notes |
|-------|-------|
| Decision | Rule-based classify + two prompts |
| Rejected | Single mega-prompt |
| Top failure mode | Mis-routed billing → product policy |
| Cost hint | ~2× single call if classify uses LLM; rules = 1 call |
| NFRs | Auditability of intent label |

## Reference code

- `patterns/w02-prompt-chaining/code/`
- Acme: `answer_with_chain`

## Disclaimer

Learning material only. Fictional Acme data.
