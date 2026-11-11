# Brief — w02 prompt-chaining

**Topic:** Prompt chaining (classify → specialized answer)
**Date researched:** 2026-11-11
**Corpus:** `content/source-corpus/latest.md`

## Summary

Prompt chaining splits one support task into fixed steps with different system instructions. Acme separates billing from product troubleshooting before retrieval and generation. The pattern trades one extra model call for clearer eval boundaries and smaller prompts per intent.

## Sources

| Title | URL | Date accessed |
|-------|-----|---------------|
| Anthropic — Building effective agents | https://www.anthropic.com/research/building-effective-agents | 2026-11-11 |
| LangChain — Context engineering challenges | https://www.langchain.com/blog/context-engineering-challenges-late-2026 | 2026-11-11 |

## Key concepts

- **Intent gate** before answer prompt reduces policy bleed across domains.
- **Deterministic classify** is acceptable for MVP; model classify comes later.
- **Chain depth** should stay shallow until metrics justify ReAct.

## Contrarian angles

- Do not chain when intent is always the same (waste of latency).
- Do not chain for compliance flows that require a single auditable prompt hash.
- Do not chain before you have per-intent golden questions.
