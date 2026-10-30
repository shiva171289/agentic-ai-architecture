# Brief — w01 augmented-llm

**Topic:** Augmented LLM (retrieval + tools + structured prompts without full agent loop)  
**Date researched:** 2026-10-30

## Summary

The augmented LLM pattern wraps a base model with retrieval, tools, and prompt structure **without** adopting a full autonomous agent loop. It is the default starting point before ReAct or multi-agent designs. Anthropic's "building effective agents" material and cloud vendor guidance both treat augmentation as the first maturity step.

## Sources

| Title | URL | Date accessed |
|-------|-----|---------------|
| Anthropic — Building effective agents | https://www.anthropic.com/research/building-effective-agents | 2026-10-30 |
| AWS Bedrock docs (overview) | https://docs.aws.amazon.com/bedrock/ | 2026-10-30 |
| Azure AI Foundry docs | https://learn.microsoft.com/azure/ai-foundry/ | 2026-10-30 |

## Key concepts

- Retrieval augments context; tools augment actions; neither requires multi-step autonomy
- Explicit prompt contracts beat open-ended "you are an agent" prompts for many enterprise tasks
- Easier to test and observe than full agent graphs

## Contrarian angles

1. **Most "agents" should stay augmented LLMs** — add autonomy only when tasks truly need branching.
2. **RAG is not free** — stale indexes hurt more than no RAG; measure retrieval precision first.
3. **Tool count explosion** — more MCP tools often reduce reliability; curate 3–5 high-value tools.

## Open questions

- When does latency of retrieval + single LLM call exceed simpler search UI?
