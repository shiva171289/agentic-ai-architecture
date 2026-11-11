# Five-layer spine (Acme-colored)

Adapted from problem-first system design pedagogy (see local [awesome-generative-ai-guide](../sample-repo/awesome-generative-ai-guide/interview_prep/system-design/README.md)). Use this spine in weekly ADRs and blogs.

| Layer | Question | Typical Acme weeks |
|-------|----------|--------------------|
| 1 Model | Which model path, and how do you handle non-determinism? | w03 routing, w35 cost routing |
| 2 Wrapping | Retrieval, tools, memory, chains | w01–w04, w07–w13 |
| 3 Evals and guardrails | How do you know it works? How do you stop bad actions? | w06, w28–w33 |
| 4 Production and ops | Latency, scale, cost, observability, rollback | w34–w38 |
| 5 Optimization | Routing, caching, advanced retrieval, multi-agent | w12+, w15+, w35 |

System design is composing these layers for one measurable outcome — not picking a vector database first.

## Layer diagram

```
                  +-------------+
                  |  1  MODEL   |
                  +------+------+
                         |
      +-------- 2  WRAPPING (RAG, tools, memory) --------+
      |                                                |
      +------------------+-----------------------------+
                         |
            3  EVALS          4  PRODUCTION
                         |
                  5  OPTIMIZATION
```

## Weekly mapping

In each `patterns/wNN-*/blog.md`, add frontmatter or a short line:

`spineLayers: "2"` or `spineLayers: "1,2"` — which layers the week primarily teaches.
