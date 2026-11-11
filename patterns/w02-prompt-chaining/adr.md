# ADR — Prompt chaining

**Status:** accepted  
**Week:** w02

## Context

Acme FAQs mix billing and product questions. A single system prompt mixes tone and policy emphasis. Support leads want per-intent eval slices.

## Decision

Use a **two-step chain**: classify intent → answer with intent-specific system prompt. Keep retrieval shared before the answer step.

## Alternatives considered

| Option | Pros | Cons |
|--------|------|------|
| Single mega-prompt | One call | Harder to eval per intent |
| Full router (w03) | Cost savings | Premature before baseline metrics |
| ReAct agent | Flexible | Variable cost |

## When NOT to use

- One dominant intent (>90%)
- Strict requirement for single prompt artifact
- Latency budget under ~300ms end-to-end

## Consequences

### Positive

- Per-intent golden sets
- Clear failure = mis-route

### Negative / risks

- Mis-classification propagates
- Extra model call if classify uses LLM (Acme uses rules in w02)
