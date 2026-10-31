# Agent constitution (Hermes + Cursor)

This file is the single source of truth for agent behavior in the **agentic-ai-architecture** hub. Every Hermes skill and every Cursor agent working in this repo must follow it.

## 1. Mission

- **Learning in public:** weekly enterprise agentic architecture patterns, AWS and Azure mappings, runnable Python samples.
- **Acme spine:** one fictional system (`projects/acme-support/`) grows each week; pattern samples stay isolated under `patterns/`.
- **Ground rules:** no employer material; fictional companies and synthetic data only. See [docs/roadmap/00-ground-rules.md](../docs/roadmap/00-ground-rules.md).

## 2. Voice

- Narrative content (blog intros, LinkedIn opinions): follow [content/voice-guide.md](../content/voice-guide.md).
- **Procedures** (runbooks, checklists, Telegram digests, “how to” sections in blogs): follow **ASD-STE100 profile** below.

## 3. Grounding (anti-hallucination)

- Vendor facts must come from [content/source-corpus/latest.md](../content/source-corpus/latest.md) and/or [hermes/sources/verified-sources.json](sources/verified-sources.json).
- Do not invent service names, pricing, or features.
- If a claim is unsupported, omit it or label **Open question**.

## 4. ASD-STE100 profile

Apply these rules to all **procedural** and **instructional** output (runbooks, setup guides, daily briefs, numbered steps in articles).

| Rule | Requirement |
|------|-------------|
| Words | Use simple, approved-style English. Avoid idioms, slang, and metaphor. |
| Sentences | One instruction per sentence. Target **20 words or fewer** when practical. |
| Steps | Use **imperative** verbs: “Install the package”, not “You should install”. |
| Voice | **Active** voice. Name the actor: Hermes, you, the reader, GitHub Actions. |
| Structure | Number steps for procedures. One topic per paragraph. |
| Headlines | Telegram and daily brief headlines: **12 words or fewer**. |
| Brief items | Daily news items: **50 words or fewer** per item, plus source URL. |

**Exceptions:** LinkedIn Post B and narrative blog sections may use the voice guide tone. Any **Procedure**, **Setup**, or **Runbook** section inside a blog must still use ASD-STE100.

## 5. Skill hierarchy (Hermes)

| Role | Skill folder | Notes |
|------|--------------|--------|
| Orchestrator | `weekly-pack` | Runs end-to-end week pipeline |
| Research | `research-scout`, `source-harvester` | Corpus-backed briefs |
| Architecture | `pattern-architect`, `reviewer-critic` | ADR gate before code/blog |
| Implementation | `code-builder`, `diagram-agent`, `cloud-mapper` | Drafts on `drafts/wNN` |
| Publishing | `blog-writer`, `linkedin-editor` | Voice + constitution |
| Growth | `growth-analyst` | Private metrics only |
| Daily news | `daily-ai-brief` | Separate from weekly-pack |

Model tiers: see [docs/roadmap/04-agent-operations.md](../docs/roadmap/04-agent-operations.md). Prefer Tier 0 for summarization; Tier 1 for tool calling and ADR.

## 6. Git safety

- Hermes on the VPS pushes only to branches matching `drafts/*`.
- **You** merge to `main` from Cursor or GitHub after review and tests.
- Never commit secrets (`.env`, bot tokens, API keys).
- Hermes git identity: `Hermes (drafts)` + GitHub noreply email.

## 7. Cursor agents (this repo)

- Read this constitution before editing content or Hermes skills.
- Match existing code style; minimal diffs.
- Do not edit `.cursor/plans/` unless asked.

## 8. References

| Doc | Purpose |
|-----|---------|
| [AGENTS.md](../AGENTS.md) | Human-readable map of the stack |
| [docs/setup/agent-stack.md](../docs/setup/agent-stack.md) | Setup anatomy |
| [docs/setup/week1-operating-guide.md](../docs/setup/week1-operating-guide.md) | First-week deploy |
