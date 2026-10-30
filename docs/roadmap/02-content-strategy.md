# Content strategy (Year 1)

## Positioning statement

> I document enterprise agentic AI architecture patterns — cloud-agnostic first, then AWS and Azure — as public learning material.

LinkedIn headline suggestion:

> Enterprise Agentic AI Architect | AWS & Azure | Learning in public

## Weekly cadence (pattern of the week)

For each week `wNN-slug` under `patterns/`:

| Asset | Purpose |
|-------|---------|
| `brief.md` | Research + sources (agent) |
| `adr.md` | Architecture decision + when NOT to use |
| `cloud-mapping.md` | AWS vs Azure services + cost notes |
| `diagram.mmd` | Logical + deployment views |
| `code/` | Runnable Python sample (mock LLM mode) |
| `blog.md` | Long-form article on site |
| `linkedin.md` | Post A (pattern), Post B (opinion), comment starters |

**Publish rhythm**

- Sunday: blog live (after merge to `main`)
- Tuesday: LinkedIn Post A (+ diagram/carousel)
- Thursday: LinkedIn Post B (+ blog link in first comment)

Agents draft; **you** edit voice and post manually.

## Content themes

- Architecture patterns and anti-patterns
- Security, identity, least-privilege tools
- AWS and Azure managed agent runtimes
- Enterprise integration and ERP angles (Q4)
- Production readiness: evals, observability, cost

## Audience funnel (Year 1 = reach, not sales)

```text
LinkedIn posts → Blog / GitHub portfolio → Newsletter (checklist)
      → Conversations with practitioners → Optional Year 2 offers
```

## KPIs (track in private repo `metrics.md`)

Monthly:

- LinkedIn followers, post impressions, profile views
- Newsletter subscribers
- GitHub stars on hub repo
- OpenRouter spend (weekly `cost` on Telegram)
- Patterns shipped vs calendar

Cut the worst-performing post format each month.

## Voice

See [content/voice-guide.md](../../content/voice-guide.md).

## Reach plan (high level)

- **Month 1:** LinkedIn profile + Featured (repo + blog), target list of 30+ architects
- **Month 2:** Framework v0.1 + gated checklist
- **Month 3:** Five practitioner conversations (steer topics)
- **Month 4:** Publish `hermes-content-factory` split repo + behind-the-scenes post
- **Month 6:** Webinar / LinkedIn Live “AWS vs Azure for Production Agents”
- **Months 9–12:** Community talks; consider AWS Community Builders / Microsoft MVP paths

Optional monetization: [06-future-monetization.md](06-future-monetization.md).
