# Agent operations (Hermes + Telegram)

## Architecture

Hermes Agent runs on a **Hostinger Ubuntu VPS**. You interact via **Telegram**. OpenRouter provides models (~**$10/month** cap). Hermes pushes drafts to GitHub branch `drafts/wNN`; you polish in **Cursor** and merge to `main`.

## Model tiers (OpenRouter)

| Tier | Use | Examples |
|------|-----|----------|
| 0 Free | Scout, drafts, LinkedIn variants | DeepSeek/Qwen/GLM `:free` models (refresh monthly) |
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

## Telegram commands (intended)

| Command | Action |
|---------|--------|
| `brief w05 orchestrator-workers` | ResearchScout → summary |
| `pack w05` | Full weekly pack → `drafts/w05` branch |
| `adr w05 approve` / `adr w05 revise: …` | Gate before code/blog |
| `post w05 A` | LinkedIn Post A text |
| `cost` | OpenRouter spend |
| `status` | Health check |

## Git workflow on VPS

- Deploy key **write access** to hub repo only
- Hermes identity: `Hermes (drafts)` + GitHub noreply email
- Protect `main`; agents push `drafts/*` only
- Cron: `git pull` in clone before skills run

## Skills location

Repo: `hermes/skills/*/SKILL.md` → symlink to `~/.hermes/skills/` on VPS.

Orchestrator: `hermes/skills/weekly-pack/SKILL.md`.

## Budget upgrade path

- **$20/mo:** more Tier 1 drafting
- **$40–50/mo:** premium OpenRouter for ADR/blog steps

Increase only after optional revenue or conscious choice.
