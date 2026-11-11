# Retrieval ladder (Acme Support)

Name every retrieval variant up front. Implement on the [calendar](../calendar.md) schedule. Vendor claims stay in [patterns](../source-corpus/latest.md) and ADRs — this page is pedagogy only.

## Scenario matrix

| Variant | When you need it | Ships (week) | Acme / pattern code |
|---------|------------------|--------------|---------------------|
| Keyword / contains | Tiny FAQ, exact tokens, demo | **w01** | `projects/acme-support/core/retrieval/keyword.py` |
| Dense / embedding | Paraphrase, short questions | w12 | same package |
| BM25 / sparse | Order IDs, SKUs, error codes | w12 | parametrized pytest |
| Hybrid + rerank | Production chat at scale | w12–w25 | ladder tests |
| Knowledge graph | Symptom → product → policy | w25 | `kg-rag` pattern |
| Agentic retrieval | Model picks search vs memory | w12 | `agentic-rag` pattern |

## Assumptions (Problem-First)

- **Corpus:** Hundreds of semi-structured policy articles, updated monthly.
- **Queries:** Short; many carry exact tokens (order id, SKU).
- **Answers:** Often one section suffices; multi-hop comes later.

When an assumption changes, change the variant — do not bolt one index onto every problem.

## Related

- Week posts: [w01-augmented-llm](../../patterns/w01-augmented-llm/blog.md)
- External depth (pedagogy): hybrid retrieval discussion in the local [awesome-generative-ai-guide](../../sample-repo/awesome-generative-ai-guide/interview_prep/system-design/customer-support-agent/README.md) case study.
