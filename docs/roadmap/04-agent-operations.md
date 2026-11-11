# Agent operations (Hermes + Telegram)

## Architecture

Hermes Agent runs on a **Hostinger Ubuntu VPS**. You interact via **Telegram**. OpenRouter provides models (~**$10/month** cap). Hermes pushes drafts to GitHub branch `drafts/wNN`; you polish in **Cursor** and merge to `main`.

## Model tiers (OpenRouter)

| Tier | Use | Examples |
|------|-----|----------|
| 0 Free | SourceHarvester, **news summarize**, Scout, drafts, LinkedIn variants | DeepSeek/Qwen/GLM `:free` models (refresh monthly) |
| 1 Cheap paid | ADR, CloudMapper, Critic, tool calling | DeepSeek V3, Qwen3, Gemini Flash |
| 2 Cursor | Final code, diagrams, ADR review | Your Cursor plan |

**Rule:** free → Tier 1 fallback only; never auto-jump to premium on OpenRouter.

Log spend weekly in private `metrics.md`; use Telegram `cost` when wired.

## Setup runbooks

1. [hermes/setup/01-hostinger-vps.md](../../hermes/setup/01-hostinger-vps.md)
2. [hermes/setup/02-hermes-install.md](../../hermes/setup/02-hermes-install.md)
3. [hermes/setup/03-telegram-gateway.md](../../hermes/setup/03-telegram-gateway.md)
4. [hermes/setup/04-news-env.md](../../hermes/setup/04-news-env.md) — Inshorts RSS pipeline
5. [hermes/cron.md](../../hermes/cron.md) — scheduled jobs
6. [hermes/PILOT-RUNBOOK.md](../../hermes/PILOT-RUNBOOK.md) — Week 1 validation
7. [docs/setup/week1-operating-guide.md](../setup/week1-operating-guide.md) — day-by-day first week
8. [docs/setup/agent-stack.md](../setup/agent-stack.md) — constitution and skills map

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
| (VPS) `python3 hermes/tools/job_status.py` | Cron log ages, news queue — no LLM |
| (VPS) `python3 hermes/tools/calendar_week.py` | Current publishing `wNN` + slug |
| (VPS) `python3 hermes/tools/weekly_reminder.py` | Monday nudge text for brief/pack |
| `news today` | Send next Inshorts card → `news_pulse_send.py --force` |
| `news status` | Queue counts → `news_status.py` |
| `news karpathy` | Karpathy-tagged items in queue (manual filter) |
| `approve publish wNN` | Test `drafts/wNN` in CI, then merge it to `main` through a pull request (GitHub Pages deploy) |
| `publish status wNN` | Draft branch + CI summary before approve |

## Publish gate (GitHub Pages)

Skill: [hermes/skills/publish-gate/SKILL.md](../../hermes/skills/publish-gate/SKILL.md).

1. On VPS, set `GITHUB_PAT` in `~/.hermes/.env` (Actions + Contents + Pull requests, read and write). The key name must be exactly `GITHUB_PAT` or `GH_TOKEN`.
2. Symlink `publish-gate` skill after `git pull`.
3. Telegram: `approve publish w01` after reviewing the checklist.
4. Workflow: [.github/workflows/publish-approved-week.yml](../../.github/workflows/publish-approved-week.yml). It **only tests** the draft branch.
5. Helper: `python3 hermes/tools/trigger_publish.py w01 w01-augmented-llm`. The helper runs the CI gate, then opens and merges the pull request.
6. Verify before you report success: `GET /repos/<owner>/<repo>/commits/main` shows the merge, and `https://shiva171289.github.io/agentic-ai-architecture/blog/wNN-slug/` returns HTTP 200.

The `main` ruleset requires changes to arrive through a pull request, so a direct
push from Actions is always rejected with
`GH013: Repository rule violations found for refs/heads/main`. Do not add a
ruleset bypass actor to work around it — merge through a pull request instead,
which is what the helper does.

## News Inshorts (hourly Telegram)

Separate from **weekly-pack**. Skill: [hermes/skills/news-inshorts/SKILL.md](../../hermes/skills/news-inshorts/SKILL.md).

1. RSS harvest is **stdlib only** (no AI): [hermes/tools/harvest_sources.py](../../hermes/tools/harvest_sources.py).
2. Summarize new queue items once daily with **OpenRouter free** model (`OPENROUTER_NEWS_MODEL`, see [hermes/setup/04-news-env.md](../../hermes/setup/04-news-env.md)).
3. Cron: daily 06:45 IST ingest+summarize; hourly :05 one random unsent card ([hermes/cron.md](../../hermes/cron.md)).
4. Enable cron **after** Week 1 pilot spend is under ~$3/week.
5. Retention: 3 days on VPS queue + dated corpus files.
6. You pick 1–2 sent cards for LinkedIn; Hermes does not auto-post.

## Cron vs weekly pack

**Medium automation:** Friday `weekly_pipeline.py friday-adr` (brief + ADR + Telegram card). ADR **Approve** runs pack; publish **Approve** runs `trigger_publish.py`. See [weekly-automation.md](../setup/weekly-automation.md) and [model-tiers-qwen.md](../setup/model-tiers-qwen.md).

Next pack week comes from [content/publish-progress.json](../../content/publish-progress.json) (`calendar_week.py --next`), not the calendar date alone.

## Cron vs weekly pack (manual fallback)

You can still send `pack wNN` by hand. See [cron-enable.md](../setup/cron-enable.md).

## Git workflow on VPS

- Deploy key **write access** to hub repo only
- Hermes identity: `Hermes (drafts)` + GitHub noreply email
- Protect `main`; agents push `drafts/*` only
- Cron: `git pull` in clone before skills run

## Skills location

Repo: `hermes/skills/*/SKILL.md` → symlink to `~/.hermes/skills/` on VPS.

Orchestrator: `hermes/skills/weekly-pack/SKILL.md`.

Daily news: `hermes/skills/news-inshorts/SKILL.md`.

## Budget upgrade path

- **$20/mo:** more Tier 1 drafting
- **$40–50/mo:** premium OpenRouter for ADR/blog steps

Increase only after optional revenue or conscious choice.
