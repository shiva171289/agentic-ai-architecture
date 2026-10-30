# ADR — Augmented LLM

**Status:** accepted  
**Week:** w01

## Context

Acme Manufacturing wants employees to ask natural-language questions about **public** product documentation and open support tickets. They need something shippable in weeks, auditable, and cost-predictable. Full autonomous agents are tempting but hard to evaluate.

## Decision

Use an **augmented LLM**: one primary model call (or fixed small chain) with **retrieval** over approved docs and **one tool** (create ticket) behind approval for high-severity categories.

## Alternatives considered

| Option | Pros | Cons |
|--------|------|------|
| Pure chat (no RAG) | Simple | Hallucinates product facts |
| Full ReAct agent | Flexible | Harder eval, variable cost |
| Classic search UI | Cheapest | No NL summarization |

## When NOT to use

- Tasks requiring many branching tool calls or long-horizon planning
- Strict deterministic compliance workflows with zero model variance
- When retrieval corpus is unmaintained or unlabeled

## Consequences

### Positive

- Predictable latency (1–2 model calls)
- Straightforward golden-set evaluation
- Clear path to add agent loop later if metrics justify

### Negative / risks

- Retrieval quality ceiling caps answer quality
- Tool misuse if permissions too broad

## Failure modes

- Retrieval returns wrong chunk → confident wrong answer
- Tool called with PII in arguments
- Model drift after vendor update without regression tests

## Security notes

- Separate read (RAG) vs write (ticket tool) credentials
- Input sanitization; output filtering for secrets

## Cost / latency (order of magnitude)

- ~1–3s p95 with one retrieval + one generation on mid-tier model
- ~$0.002–0.02 per query at small context sizes (varies by model)
