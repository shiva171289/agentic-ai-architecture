# Repository strategy

## Hub (this repo)

**`git@github.com-personal:shiva171289/agentic-ai-architecture.git`**

Contains roadmap, content calendar, weekly patterns (small samples), **Acme Support Platform** (`projects/acme-support/`), framework, Hermes skills, blog site, shared IaC templates.

## Private repo

**`shiva171289/agentic-ai-private`** — metrics, contacts, draft opinions, future offer docs. See [docs/private-repo/SETUP.md](../private-repo/SETUP.md).

## When to create a new public repo

Split when **any** of:

- Flagship with multi-service deploy, >~1,500 LOC, or own infra lifecycle
- Clone-and-run demo you'd link standalone from LinkedIn
- Reusable tooling (e.g. Hermes content factory)

Weekly pattern samples **stay in hub** until split criteria met.

## Planned split schedule

| When | Repository | Notes |
|------|------------|-------|
| End Q1 (W13) | `acme-agentic-support` | Acme v1 — evolving year-long use-case ([07-running-use-case.md](07-running-use-case.md)) |
| ~Month 3 | `hermes-content-factory` | Skills + setup; blog post topic |
| End Q2 (W26) | *(same)* `acme-agentic-support` | Tag `v2` — multi-agent desk |
| End Q3 (W39) | *(same)* `acme-agentic-support` | Tag `v3` — production hardening |
| End Q4 (W46) | *(same)* `acme-agentic-support` | Tag `v4` — ERP / back-office |
| Q4 (W52) | `agent-governance-registry` | F5 — fleet governance (separate lifecycle from Acme app) |
| Optional 20+ patterns | `agentic-patterns-python` | Pip-installable catalog |

Git tags on Acme repo: `stage-wNN` weekly, `v1`–`v4` at release weeks. Changelog: `projects/acme-support/STAGES.md`.

## Flagship repo template

- README + architecture diagram
- `docs/adr/`, `src/` or `code/`
- `infra/aws` (Terraform), `infra/azure` (Bicep)
- `make deploy-aws`, `make deploy-azure`, `make destroy`
- Mock mode + CI + MIT license
- Link back to hub pattern pages

## Split procedure (checklist)

1. Create empty repo under `shiva171289`
2. Copy flagship code from `projects/acme-support/` (or F5 from `patterns/`)
3. Add CI, README, infra destroy docs
4. Hub README + pattern page link to new repo
5. Archive heavy code in hub (replace with submodule link or pointer)

Track upcoming splits in [projects/SPLIT-SCHEDULE.md](../../projects/SPLIT-SCHEDULE.md).
