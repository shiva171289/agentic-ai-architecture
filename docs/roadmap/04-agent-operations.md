# Agent operations (Hermes + Telegram)

## Architecture

Hermes Agent runs on a **Hostinger Ubuntu VPS**. You interact via **Telegram**. OpenRouter provides models (~**$10/month** cap). Hermes pushes drafts to GitHub branch `drafts/wNN`; you polish in **Cursor** and merge to `main`.

## Model tiers (OpenRouter)

| Tier | Use | Examples |
|------|-----|----------|
| 0 Free | SourceHarvester digest, Scout, drafts, LinkedIn variants | DeepSeek/Qwen/GLM `:free` models (refresh monthly) |
| 1 Cheap paid | ADR, CloudMapper, Critic, tool calling | DeepSeek V3, Qwen3, Gemini Flash |
| 2 Cursor | Final code, diagrams, ADR review | Your Cursor plan |

**Rule:** free → Tier 1 fallback only; never auto-jump to premium on OpenRouter.

Log spend weekly in private `metrics.md`; use Telegram `cost` when wired.

## Setup runbooks

1. [hermes/setup/01-hostinger-vps.md](../../hermes/setup/01-hostinger-vps.md)
2. [hermes/setup/02-hermes-install.md](../../hermes/setup/02-hermes-install.md)
3. [hermes/setup/03-telegram-gateway.md](../../hermes/setup/03-telegram-gateway.md)
4. [hermes/cron.md](../../hermes/cron.md) — scheduled jobs
5. [hermes/PILOT-RUNBOOK.md](../../hermes/PILOT-RUNBOOK.md) — Week 1 validation
6. [docs/setup/week1-operating-guide.md](../setup/week1-operating-guide.md) — day-by-day first week
7. [docs/setup/agent-stack.md](../setup/agent-stack.md) — constitution and skills map

## Constitution

All skills follow [hermes/CONSTITUTION.md](../../hermes/CONSTITUTION.md) (ASD-STE100 for procedures, grounding rules).

## Telegram commands (intended)

| Command | Action |
|---------|--------|
| `sources refresh` / `sources w05` | SourceHarvester → `content/source-corpus/latest.md` |
| `brief w05 orchestrator-workers` | SourceHarvester if stale → ResearchScout → summary |
| `pack w05` | Full weekly pack → `drafts/w05` branch |
| `adr w05 approve` / `adr w05 revise: …` | Gate before code/blog |
| `post w05 A` | LinkedIn Post A text |
| `cost` | OpenRouter spend |
| `status` | Health check |
| `news today` | Daily AI brief → Telegram + `content/daily-brief/YYYY-MM-DD.md` |
| `news karpathy` | Karpathy watch block only (last 7 days) |
| `approve publish wNN` | Dispatch Actions merge `drafts/wNN` → `main` (GitHub Pages deploy) |
| `publish status wNN` | Draft branch + CI summary before approve |

## Publish gate (GitHub Pages)

Skill: [hermes/skills/publish-gate/SKILL.md](../../hermes/skills/publish-gate/SKILL.md).

1. On VPS, set `GITHUB_PAT` in `~/.hermes/.env` (Actions + Contents write).
2. Symlink `publish-gate` skill after `git pull`.
3. Telegram: `approve publish w01` after reviewing the checklist.
4. Workflow: [.github/workflows/publish-approved-week.yml](../../.github/workflows/publish-approved-week.yml).
5. Helper: `python3 hermes/tools/trigger_publish.py w01 w01-augmented-llm`.

If branch protection blocks the default `GITHUB_TOKEN`, add repo secret `PUBLISH_PAT` and update the workflow push step to use it.

## Daily AI brief

Separate from **weekly-pack**. Skill: [hermes/skills/daily-ai-brief/SKILL.md](../../hermes/skills/daily-ai-brief/SKILL.md).

- Cron: daily 07:00 IST (see [hermes/cron.md](../../hermes/cron.md))
- Enable cron **after** Week 1 pilot spend is under ~$3/week
- You pick 1–2 items for LinkedIn; Hermes does not auto-post

## Git workflow on VPS

- Deploy key **write access** to hub repo only
- Hermes identity: `Hermes (drafts)` + GitHub noreply email
- Protect `main`; agents push `drafts/*` only
- Cron: `git pull` in clone before skills run

## Skills location

Repo: `hermes/skills/*/SKILL.md` → symlink to `~/.hermes/skills/` on VPS.

Orchestrator: `hermes/skills/weekly-pack/SKILL.md`.

Daily news: `hermes/skills/daily-ai-brief/SKILL.md`.

## Budget upgrade path

- **$20/mo:** more Tier 1 drafting
- **$40–50/mo:** premium OpenRouter for ADR/blog steps

Increase only after optional revenue or conscious choice.
