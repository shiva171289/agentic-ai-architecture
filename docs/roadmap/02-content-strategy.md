# Content strategy (Year 1)

## Positioning statement

> I document enterprise agentic AI architecture patterns — cloud-agnostic first, then AWS and Azure — as public learning material.

LinkedIn headline suggestion:

> Enterprise Agentic AI Architect | AWS & Azure | Learning in public

## Weekly cadence (pattern of the week)

For each week `wNN-slug` under `patterns/`:

| Asset | Purpose |
|-------|---------|
| `brief.md` | Research + sources (ResearchScout, grounded in source corpus) |
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

## Grounding (anti-hallucination)

**SourceHarvester** (Thursday cron) pulls allowlisted vendor RSS and selected official HTML index pages (AWS, Azure, Microsoft DevBlogs/Foundry, OpenAI, Anthropic News, LangChain) into `content/source-corpus/latest.md`. ResearchScout and ReviewerCritic treat that file plus official doc roots as the vendor fact base. See [hermes/sources/README.md](../../hermes/sources/README.md).

## Content themes

- Architecture patterns and anti-patterns
- **Acme Support Platform** spine — one system, weekly increments ([07-running-use-case.md](07-running-use-case.md))
- Security, identity, least-privilege tools
- AWS and Azure managed agent runtimes
- Enterprise integration and ERP angles (Q4)
- Production readiness: evals, observability, cost

## Reader progression

- **Start Here** on the blog: primer + Acme storyline + level ladder (`/start-here/`)
- **Level tags** on every post: Foundation (Q1), Practitioner (Q2), Production (Q3), Architect (Q4)
- **Prerequisites** link to earlier weeks
- **Architect's notebook** in every blog: decision, rejected alternative, top failure mode, indicative cost per 1k runs, NFRs touched
- **AI Architect skills map:** [content/ai-architect-skills-map.md](../../content/ai-architect-skills-map.md) (newsletter companion)

## Pattern Radar (monthly)

First Friday each month: ResearchScout drafts `content/radar/YYYY-MM.md` — what's new in the corpus and where it plugs into Acme. Short public post; evergreen weekly spine unchanged.

## Quarterly design challenges

Buffer weeks (w14, w27, w40, w52): post an Acme scenario, collect reader answers, publish your reference answer in the retrospective.

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

## Syndication (Medium)

Republish **excerpts** on [Medium](https://medium.com) for reach. Treat **GitHub Pages as canonical**.

| Rule | Action |
|------|--------|
| License | CC BY 4.0 allows reuse with attribution |
| Canonical URL | Set Medium canonical link to `https://shiva171289.github.io/agentic-ai-architecture/blog/<slug>/` |
| Timing | Publish on Medium **7–14 days after** the Sunday blog merge |
| Length | Prefer **800–1200 words** (Post A depth) plus CTA to full pattern, code, and cloud mapping on the site |
| Partner Program | Optional; Year 1 goal is audience, not payout ([06-future-monetization.md](06-future-monetization.md)) |

Record optional `mediumRepublishDate` in blog front matter when you cross-post.

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
