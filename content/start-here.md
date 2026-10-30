# Start Here

Welcome. This site documents **enterprise agentic AI architecture** week by week. If terms like “agent,” “RAG,” or “MCP” are new, read the primer below, then follow the **Acme Support Platform** storyline in `projects/acme-support/` on GitHub.

## Primer (5 minutes)

| Term | Plain meaning |
|------|----------------|
| **Tokens & context window** | Text is split into tokens; the model can only “see” a limited window per call. Long chats need summarization or external memory. |
| **Embeddings** | Numeric vectors that represent meaning; used to search documents by similarity (retrieval). |
| **Structured output** | Asking the model to return JSON or a schema you validate — safer than free-form text for tools and APIs. |
| **Agent vs workflow** | A **workflow** follows a fixed graph you designed. An **agent** chooses steps dynamically (often with tools). Use workflows when predictability matters; agents when the path depends on messy inputs. |

Each weekly post adds one pattern. Runnable samples live under `patterns/wNN-slug/code/`; the **Acme stage** shows the same idea inside one evolving support system.

## The Acme storyline

**Acme Manufacturing** (fictional) sells hardware online. You will watch their support platform grow across four releases:

| Release | Weeks | What you build |
|---------|-------|----------------|
| **Acme v1** | w01–w13 | Single-agent support: augmentation, routing, tools, MCP, agentic RAG, memory |
| **Acme v2** | w15–w26 | Multi-agent desk: supervisor, specialists, sagas, human approval |
| **Acme v3** | w28–w39 | Production hardening: guardrails, identity, evals, tracing, cost |
| **Acme v4** | w41–w46 | Back-office flows: procurement, reconciliation, ERP via MCP |
| **F5** | w47–w52 | Fleet governance registry (separate reusable repo) |

Start with [Week 1 — Augmented LLM](/blog/w01-augmented-llm/) and the mock runnable code in `projects/acme-support/` (no cloud API keys required for tests).

## Level ladder

Posts are tagged by reader level:

| Level | Weeks | You can… |
|-------|-------|----------|
| **Foundation** | w01–w14 | Ship a single-agent FAQ assistant with retrieval and tools |
| **Practitioner** | w15–w27 | Design multi-agent handoffs and compensating transactions |
| **Production** | w28–w40 | Operate agents with evals, observability, and security controls |
| **Architect** | w41–w52 | Integrate ERP/back-office and govern a fleet of agents |

Use the [AI Architect skills map](/ai-architect-skills-map/) to score yourself against the [12-pillar framework](https://github.com/shiva171289/agentic-ai-architecture/blob/main/framework/README.md).

## What to do next

1. Skim the [production readiness checklist](/production-readiness-checklist/).
2. Read [w01 Augmented LLM](/blog/w01-augmented-llm/).
3. Clone the repo and run `uv run pytest` in `projects/acme-support/`.

## Disclaimer

Learning material only. Examples are synthetic and do not represent any employer. See [ground rules](https://github.com/shiva171289/agentic-ai-architecture/blob/main/docs/roadmap/00-ground-rules.md).
