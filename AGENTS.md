# Agents in this repository

Quick map for humans and IDE agents. Full rules: **[hermes/CONSTITUTION.md](hermes/CONSTITUTION.md)**.

## Constitution

- Mission, grounding, ASD-STE100 for procedures, git safety: [hermes/CONSTITUTION.md](hermes/CONSTITUTION.md)
- Cursor rule: [.cursor/rules/agent-constitution.mdc](.cursor/rules/agent-constitution.mdc)

## Hermes (VPS + Telegram)

| Path | Role |
|------|------|
| [hermes/skills/](hermes/skills/) | One folder per agent role (`SKILL.md`) |
| [hermes/skills/_shared/ground-rules.md](hermes/skills/_shared/ground-rules.md) | Block included in every skill |
| [hermes/skills/weekly-pack/](hermes/skills/weekly-pack/) | Orchestrates the weekly pattern pack |
| [hermes/templates/](hermes/templates/) | Output shapes (blog, ADR, LinkedIn) |
| [hermes/setup/](hermes/setup/) | VPS, install, Telegram |
| [hermes/cron.md](hermes/cron.md) | Scheduled jobs (IST) |
| [docs/roadmap/04-agent-operations.md](docs/roadmap/04-agent-operations.md) | Models, commands, budget |

**First deploy:** [docs/setup/week1-operating-guide.md](docs/setup/week1-operating-guide.md)

## Cursor (laptop)

| Path | Role |
|------|------|
| `.cursor/rules/` | Repo-specific agent rules |
| `.cursor/plans/` | Plan artifacts (do not treat as source of truth) |
| User `~/.cursor/skills-cursor/` | Personal skills (outside this repo) |

## Voice and content

- [content/voice-guide.md](content/voice-guide.md) — blog and LinkedIn tone
- Procedures in content must follow ASD-STE100 (see constitution)

## Secrets

- OpenRouter and Telegram: VPS `~/.hermes/.env` only
- Never commit tokens to the hub repo
