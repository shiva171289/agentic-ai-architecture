# Agentic AI Architecture (learning in public)

[![Deploy site](https://github.com/shiva171289/agentic-ai-architecture/actions/workflows/deploy-site.yml/badge.svg)](https://github.com/shiva171289/agentic-ai-architecture/actions/workflows/deploy-site.yml)
[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-green.svg)](LICENSE-content)

**Live site:** [shiva171289.github.io/agentic-ai-architecture](https://shiva171289.github.io/agentic-ai-architecture/)

Weekly **enterprise agentic architecture patterns** — cloud-agnostic Python samples, **AWS and Azure** mappings, ADRs, and diagrams. One running storyline: the **Acme Support Platform** grows from FAQ bot to governed multi-agent architecture.

Built by [Shivashanmugam Mohan](https://www.linkedin.com/in/shivashanmugam-mohan/) as public learning material (not employer representations).

![Agentic AI Architecture](site/public/og-default.svg)

## Quick links

| Resource | Path |
|----------|------|
| **Week 1 deploy (Hermes + Telegram)** | [docs/setup/week1-operating-guide.md](docs/setup/week1-operating-guide.md) |
| **Agent stack (constitution, skills, rules)** | [docs/setup/agent-stack.md](docs/setup/agent-stack.md) · [AGENTS.md](AGENTS.md) |
| Roadmap overview | [roadmap.md](roadmap.md) |
| 52-week calendar | [content/calendar.md](content/calendar.md) |
| Framework v0.1 | [framework/README.md](framework/README.md) |
| Production checklist | [framework/production-readiness-checklist.md](framework/production-readiness-checklist.md) |
| Hermes agent skills | [hermes/skills/](hermes/skills/) · [CONSTITUTION](hermes/CONSTITUTION.md) |
| Vendor source corpus | [content/source-corpus/](content/source-corpus/) · [allowlist](hermes/sources/verified-sources.json) |
| Blog (source) | [site/](site/) · GitHub Pages via Actions |
| Week 0 setup | [docs/setup/week0-accounts-checklist.md](docs/setup/week0-accounts-checklist.md) |

## Repository layout

```text
patterns/wNN-slug/   # weekly pattern packs
projects/acme-support/  # running use-case spine
framework/           # 12-pillar architecture framework
hermes/              # agent skills, constitution, VPS setup runbooks
site/                # Astro blog
infra/templates/     # shared Terraform / Bicep stubs
docs/roadmap/        # structured roadmap
```

## Ground rules

No employer use cases or confidential material. Fictional companies and synthetic data only. See [docs/roadmap/00-ground-rules.md](docs/roadmap/00-ground-rules.md).

## Disclaimer

Views and examples are my own, for learning purposes, and do not represent my employer.

## License

Code: MIT · Written content: CC BY 4.0
