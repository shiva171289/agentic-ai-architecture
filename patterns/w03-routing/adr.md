# ADR — Routing

**Status:** accepted  
**Week:** w03

## Decision

Route with **heuristics** (intent, length, dispute keywords) to `FastMockLLM` vs `CapableMockLLM` after w02 chain.

## When NOT to use

- No quality metrics per path
- Compliance requires single pinned model version
