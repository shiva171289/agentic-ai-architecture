# AI Architect skills map (Year 1)

This page is a **progress chart**, not a test. It maps what you practice each week to the skills an enterprise agentic AI architect needs. If a row feels dense, ignore the jargon until you reach those weeks—the blog posts explain each idea in context.

The [12-pillar framework on GitHub](https://github.com/shiva171289/agentic-ai-architecture/blob/main/framework/README.md) is the scorecard. Pillars are topics like security, evaluation, and cost—questions you should answer before production.

**Main project:** follow the [Acme Support Platform roadmap](https://github.com/shiva171289/agentic-ai-architecture/blob/main/docs/roadmap/07-running-use-case.md) in [`projects/acme-support/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/projects/acme-support) on GitHub.

| Skill area | What “good” looks like | Framework pillars | Primary weeks |
|------------|------------------------|-------------------|---------------|
| **Design & trade-offs** | Know when a fixed workflow beats an agent; write short decision notes with failure modes | 1, 2 | w01, w09, w14, w27, w40, w52 |
| **RAG & data** | Keep docs fresh; combine keyword + semantic search when needed | 3, 4 | w01, w04, w12, w25 |
| **Orchestration** | Chain steps, route to the right helper, recover when a step fails | 2 | w02–w05, w15–w23 |
| **Tools & integration** | Give each tool minimal permissions; connect ERP/APIs safely | 5 | w10, w11, w29, w31, w45 |
| **Security & identity** | Treat user input as untrusted; separate “who is the user” from “who is the agent” | 6, 7 | w28–w30 |
| **Evaluation** | Maintain golden test questions; catch regressions in CI | 9 | w06, w32, w33, w37 |
| **Observability & cost** | Trace requests end-to-end; know cost per 1k runs | 10, 11 | w34–w36 |
| **Governance & ops** | Register agents, policies, and audit trails | 8, 12 | w47–w51 |

## Level ladder

| Level | Weeks | Focus |
|-------|-------|--------|
| Foundation | w01–w14 | Single-agent Acme v1 |
| Practitioner | w15–w27 | Multi-agent Acme v2 |
| Production | w28–w40 | Hardening Acme v3 |
| Architect | w41–w52 | ERP + fleet governance (Acme v4 + F5) |

## Self-assessment (monthly)

Use these steps once a month:

1. Open the [framework README](https://github.com/shiva171289/agentic-ai-architecture/blob/main/framework/README.md) and score each pillar from 1 (new) to 5 (confident).
2. Pick the next two or three calendar weeks that target your lowest scores.
3. After each week, update your scores using the **Architect's notebook** section in that blog post.

## Newsletter

This map pairs with the [production readiness checklist](/production-readiness-checklist/) on this site. Email signup (Buttondown) will live on the home page when configured.

## Disclaimer

Learning material only. See [ground rules on GitHub](https://github.com/shiva171289/agentic-ai-architecture/blob/main/docs/roadmap/00-ground-rules.md).
