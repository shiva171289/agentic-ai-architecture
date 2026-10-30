# Year 1 learning plan

**Period:** October 2026 – October 2027  
**Primary objective:** Build skills, public portfolio, and architect audience — not revenue.

## How this helps your day job

- Faster evaluation of agentic patterns in design reviews
- Reusable AWS vs Azure comparison for enterprise decisions
- Stronger credibility with engineering leaders and vendors
- Cloud AI certifications you can cite internally and externally

## Technical priorities

Agent architectures, MCP, RAG, knowledge graphs, context engineering, orchestration, memory, tool calling, evaluation, observability, AI security and governance, **AWS and Azure AI services**, cost architecture.

Prioritize **principles and trade-offs** over chasing every new framework release.

## Certifications (stretch)

- AWS: Generative AI or ML specialty (check current catalog)
- Azure: AI Engineer or equivalent (check current catalog)

## Running use-case: Acme Support Platform

One fictional system grows all year in [projects/acme-support/](../../projects/acme-support/). Weekly patterns add a small **Acme stage**; quarterly **releases** replace the old separate flagships for support, multi-agent, finance, and ERP layers.

| Release | Weeks | Split / tag |
|---------|-------|-------------|
| Acme v1 — single-agent support | w01–w13 | End Q1 → `acme-agentic-support` @ `v1` |
| Acme v2 — multi-agent desk | w15–w26 | `@v2` |
| Acme v3 — production hardening | w28–w39 | `@v3` |
| Acme v4 — ERP / back-office | w41–w46 | `@v4` |
| F5 — agent governance (separate lifecycle) | w47–w52 | `agent-governance-registry` |

Details: [07-running-use-case.md](07-running-use-case.md). Reader levels: Foundation → Practitioner → Production → Architect (see [content/ai-architect-skills-map.md](../../content/ai-architect-skills-map.md)).

Each release: GitHub (hub first, then split), diagrams, article, LinkedIn posts, ADRs, synthetic data only.

## Content targets

- ~100 LinkedIn posts (2/week)
- ~48 published patterns (1/week minus buffer weeks)
- Framework v1.0 by year end
- Production Readiness Checklist (newsletter lead magnet)

## End-of-year milestones

- Clear positioning and public portfolio
- Enterprise Agentic AI Architecture Framework v1
- Network of architects and technology leaders
- 1–2 community talks or webinar
- Go / no-go on optional monetization for Year 2

## Quarterly themes

See [content/calendar.md](../../content/calendar.md).

- **Q1:** Single-agent foundations + Acme v1
- **Q2:** Multi-agent orchestration + Acme v2
- **Q3:** Production readiness (managed AWS/Azure services) + Acme v3
- **Q4:** Agentic ERP niche + governance + Acme v4 + F5

## Time budget (~8 h/week)

| Day | Activity | Time |
|-----|----------|------|
| Mon | Research reading | 30 min |
| Tue | LinkedIn Post A | 30 min |
| Thu | LinkedIn Post B | 30 min |
| Fri | Review agent brief (Telegram) | 15 min |
| Sat | ADR approval, Cursor polish, code | 2.5 h |
| Sun | Blog edit, merge, networking | 2.5 h |
| Daily | 5 thoughtful comments on target posts | 15 min |

During crunch at work: keep **one pattern/week** and skip extras.

## What to avoid

Generic freelancing, unrelated side hustles, large SaaS before validation, courses before audience, framework churn without reusable IP. See ground rules.
