# Start Here

Think of this site as a **52-week course** in building AI helpers for a fictional company, **Acme Manufacturing**. They sell gadgets online and need a customer-support assistant that grows from a simple FAQ bot into a governed multi-agent system.

You do not need cloud accounts to follow along. The sample code in the GitHub repo runs on your laptop with tests only.

## Quick vocabulary (with examples)

| Term | Simple idea | Example |
|------|-------------|---------|
| **LLM** | A model that reads text and writes text | “Summarize this return policy in two sentences.” |
| **Token / context window** | The model reads only a limited amount of text at once—like a small desk | A 100-page manual does not fit; you retrieve the right page first. |
| **RAG** (retrieval-augmented generation) | Search your docs, then ask the model using what you found | User asks “What is the warranty?” → find the warranty paragraph → answer from that text. |
| **Tool** | A function the model can call (create ticket, look up order) | “Create ticket #4821” runs code you wrote, not guesswork in chat. |
| **Agent** | The model chooses *which* steps to take (search, call tools, reply) | Like a new hire who decides whether to check the wiki or escalate—useful, but harder to test than a fixed recipe. |
| **Workflow** | A fixed recipe you designed | Always: classify question → search FAQ → answer. Predictable and easy to audit. |
| **MCP** | A standard plug-in port so tools connect the same way across apps | One “order lookup” server can plug into many agent hosts—similar to USB for integrations. |

Each week adds one building block. Small demos live under `patterns/w01-…/code/` on GitHub. The **Acme storyline** in [`projects/acme-support/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/projects/acme-support) reuses those ideas in one codebase that grows week by week.

## The Acme storyline (four chapters)

Imagine Acme’s support desk maturing over a year:

| Chapter | Weeks | What changes |
|---------|-------|----------------|
| **Acme v1** | w01–w13 | One assistant: search policies, answer FAQs, later add tools and memory |
| **Acme v2** | w15–w26 | Several specialists coordinated by a supervisor (routing, handoffs) |
| **Acme v3** | w28–w39 | Production habits: security, tests, tracing, cost controls |
| **Acme v4** | w41–w46 | Back-office tasks (orders, procurement) through controlled APIs |
| **Fleet (F5)** | w47–w52 | Governance for many agents across teams |

Start reading with [Week 1 — Augmented LLM](/blog/w01-augmented-llm/). That pattern is “search docs, then answer”—the gentlest on-ramp before full agents.

Want to run the code? Open the [Acme Support repo folder](https://github.com/shiva171289/agentic-ai-architecture/tree/main/projects/acme-support) and follow the steps in **What to do next** below.

Optional: deploy the **Hermes** agent stack on a VPS (Telegram gateway) using the [Week 1 operating guide](https://github.com/shiva171289/agentic-ai-architecture/blob/main/docs/setup/week1-operating-guide.md) and [agent stack overview](https://github.com/shiva171289/agentic-ai-architecture/blob/main/docs/setup/agent-stack.md).

## How hard is each week?

Posts are tagged so you can match your experience:

| Level | Weeks | You will be able to… |
|-------|-------|----------------------|
| **Foundation** | w01–w14 | Build a single FAQ-style assistant with search and basic tools |
| **Practitioner** | w15–w27 | Design multi-step handoffs between helpers |
| **Production** | w28–w40 | Operate with monitoring, evals, and security guardrails |
| **Architect** | w41–w52 | Connect ERP-style systems and govern a fleet of agents |

Track skills with the [AI Architect skills map](/ai-architect-skills-map/) against the [12-pillar framework on GitHub](https://github.com/shiva171289/agentic-ai-architecture/blob/main/framework/README.md).

## What to do next

Follow these steps on your machine:

1. Skim the [production readiness checklist](/production-readiness-checklist/) (what “ready for real users” looks like).
2. Read [Week 1 — Augmented LLM](/blog/w01-augmented-llm/).
3. Clone [the GitHub repository](https://github.com/shiva171289/agentic-ai-architecture), open `projects/acme-support/`, then run:

```bash
uv sync --extra dev && uv run pytest
```

## Disclaimer

Learning material only. Examples are fictional and do not represent any employer. See [ground rules on GitHub](https://github.com/shiva171289/agentic-ai-architecture/blob/main/docs/roadmap/00-ground-rules.md).
