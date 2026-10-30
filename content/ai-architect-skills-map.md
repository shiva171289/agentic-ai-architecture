# AI Architect skills map (Year 1)

Use this matrix to grow from practitioner to **enterprise agentic AI architect**. Each row maps to calendar weeks and to pillars in the [Enterprise Agentic AI Architecture Framework](../framework/README.md).

**Spine:** follow the [Acme Support Platform](../docs/roadmap/07-running-use-case.md) in `projects/acme-support/` week by week.

| Skill area | What “good” looks like | Framework pillars | Primary weeks |
|------------|------------------------|-------------------|---------------|
| **Design & trade-offs** | Agent vs workflow; when not to use autonomy; ADRs with failure modes | 1, 2 | w01, w09, w14, w27, w40, w52 |
| **RAG & data** | Fresh corpora, hybrid search, agentic retrieval, knowledge graphs | 3, 4 | w01, w04, w12, w25 |
| **Orchestration** | Chains, routing, parallel, supervisor, sagas, events | 2 | w02–w05, w15–w23 |
| **Tools & integration** | Least privilege, MCP, gateways, ERP APIs | 5 | w10, w11, w29, w31, w45 |
| **Security & identity** | Prompt injection, scoped tools, agent identity | 6, 7 | w28–w30 |
| **Evaluation** | Golden sets, online regression, CI gates | 9 | w06, w32, w33, w37 |
| **Observability & cost** | Traces, cost per 1k runs, caching, fallbacks | 10, 11 | w34–w36 |
| **Governance & ops** | Registry, policy, audit, multi-cloud deploy | 8, 12 | w47–w51 |

## Level ladder

| Level | Weeks | Focus |
|-------|-------|--------|
| Foundation | w01–w14 | Single-agent Acme v1 |
| Practitioner | w15–w27 | Multi-agent Acme v2 |
| Production | w28–w40 | Hardening Acme v3 |
| Architect | w41–w52 | ERP + fleet governance (Acme v4 + F5) |

## Self-assessment (monthly)

1. Score each framework pillar 1–5 (see [framework/README.md](../framework/README.md)).
2. Pick the next 2–3 calendar weeks that strengthen your lowest pillars.
3. After each week, update your scores using the **Architect's notebook** section in that blog post.

## Newsletter

This map is a companion to the [Production Readiness Checklist](../framework/production-readiness-checklist.md). Gated signup on the site (Buttondown).

## Disclaimer

Learning material only. See [docs/roadmap/00-ground-rules.md](../docs/roadmap/00-ground-rules.md).
