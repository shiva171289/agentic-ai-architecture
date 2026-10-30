# Flagship split schedule

Track when hub code moves to standalone repositories. See [docs/roadmap/05-repo-strategy.md](../docs/roadmap/05-repo-strategy.md) and [07-running-use-case.md](../docs/roadmap/07-running-use-case.md).

| Target date | Repository | Source in hub | Status |
|-------------|------------|---------------|--------|
| End Q1 (W13) | `acme-agentic-support` | `projects/acme-support/` tag `v1` | planned |
| ~Month 3 | `hermes-content-factory` | `hermes/skills/`, setup docs | planned |
| End Q2 (W26) | `acme-agentic-support` | same repo, tag `v2` | planned |
| End Q3 (W39) | `acme-agentic-support` | same repo, tag `v3` | planned |
| End Q4 (W46) | `acme-agentic-support` | same repo, tag `v4` | planned |
| Q4 (W52) | `agent-governance-registry` | F5 patterns + governance code | planned |

## Hub directory

- **`projects/acme-support/`** — running use-case (all Acme v1–v4 stages)
- `projects/f1-customer-support/` — pointer only (superseded by Acme spine)

Split checklist: create repo → copy code → CI + destroy docs → link from hub README → trim hub copy to pointer.
