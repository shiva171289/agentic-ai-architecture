# Brief — w01 augmented-llm

**Topic:** Augmented LLM (retrieval + tools + structured prompts without a full agent loop)
**Date researched:** 2026-11-03
**Corpus:** `content/source-corpus/latest.md` (44 entries, window 2 days, generated 2026-11-03)

## Summary

The augmented LLM pattern wraps a base model with retrieval, tools, and a structured prompt. It does not adopt a full autonomous loop. It stays the default starting point before ReAct, orchestrator-workers, or multi-agent designs. This week's corpus shows the pattern moving toward production concerns: retrieval preparation, context budget, and the cost of tool loops. Vendor posts now treat augmentation as an engineering discipline, not a prompt trick.

## Sources

| Title | URL | Date accessed |
|-------|-----|---------------|
| AWS — Prepare web content for Bedrock Knowledge Bases with Crawl4AI | https://aws.amazon.com/blogs/machine-learning/prepare-web-content-for-amazon-bedrock-knowledge-bases-with-crawl4ai/ | 2026-11-03 |
| AWS — Build efficient agents with knowledge distillation on SageMaker AI | https://aws.amazon.com/blogs/machine-learning/build-efficient-agents-with-knowledge-distillation-on-amazon-sagemaker-ai/ | 2026-11-03 |
| LangChain — New context engineering challenges in late 2026 | https://www.langchain.com/blog/context-engineering-challenges-late-2026 | 2026-11-03 |
| AWS — Weekly roundup: Step Functions as agent tools | https://aws.amazon.com/blogs/aws/aws-weekly-roundup-gpt-6-1-terra-on-bedrock-step-functions-as-agent-tools-and-more-november-2-2026/ | 2026-11-03 |
| Anthropic — Building effective agents | https://www.anthropic.com/research/building-effective-agents | 2026-11-03 |
| AWS — Amazon Bedrock docs (doc root) | https://docs.aws.amazon.com/bedrock/ | 2026-11-03 |
| Microsoft — Azure AI Foundry docs (doc root) | https://learn.microsoft.com/en-us/azure/ai-foundry/ | 2026-11-03 |

## Key concepts

- **Three augmentations, one call.** Retrieval adds context. Tools add actions. A prompt contract adds structure. None of these needs a multi-step loop.
- **Retrieval quality starts before the index.** The Crawl4AI post puts JavaScript rendering, selective extraction, and metadata enrichment in a preparation layer before content reaches an S3 data source. Bad input defeats a good retriever.
- **Context is a budget, not a bucket.** LangChain frames context engineering as the main harness problem for proactive agents. The same limit applies to a single augmented call.
- **Tool loops carry a price.** AWS notes that frontier prices on every step of a tool loop are hard to sustain. Distillation is one answer. Fewer, better tools is another.
- **Reach beats capability.** AWS hands Step Functions, which already orchestrates 220+ services, to an agent as a tool. Existing workflows become callable without a rewrite.
- **Testability is the real win.** A single augmented call has one input, one output, and a fixed tool set. You can evaluate it with a golden set. Agent graphs are harder to pin down.

## Contrarian angles

1. **Most "agents" should stay augmented LLMs.** Add autonomy only when the task truly branches. A retrieval call plus one tool call covers a large share of enterprise support work.
2. **RAG is not free.** A stale or badly crawled index hurts more than no retrieval. Measure retrieval precision before you add a vector store.
3. **Tool count explosion.** More tools usually lower reliability. Curate 3–5 high-value tools and keep the schema small.

## Open questions

- When does retrieval plus one LLM call exceed the latency of a plain search UI?
- Which context-engineering techniques from the LangChain post apply to a single call, and which need a loop?
- Does distillation preserve tool-selection accuracy, or only answer quality? The AWS post does not separate the two.
- What is the minimum eval set that proves an augmented LLM beats a keyword search baseline?
