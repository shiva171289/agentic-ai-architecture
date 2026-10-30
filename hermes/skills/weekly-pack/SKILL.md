---
name: weekly-pack
description: Orchestrate full weekly pattern pack onto drafts branch after ADR approval.
---

# WeeklyPack orchestrator

Enforce `_shared/ground-rules.md` across subagents.

## Command

`pack wNN` (Telegram or CLI)

## Workflow

1. **SourceHarvester** if `content/source-corpus/latest.md` missing or older than 7 days (or `sources refresh` on Telegram).
2. **ResearchScout** if `brief.md` missing or stale (>7 days).
3. **PatternArchitect** → pause until human approves ADR on Telegram.
4. Parallel:
   - **CloudMapper**
   - **CodeBuilder** (pattern sample + Acme stage in `projects/acme-support/`)
   - **DiagramAgent**
5. **BlogWriter** (after step 4 completes)
6. **LinkedInEditor**
7. **ReviewerCritic** → fix loop once
8. Git:
   - `git checkout -B drafts/wNN`
   - Commit all files under `patterns/wNN-slug/` **and** changes under `projects/acme-support/` (if any)
   - `git push -u origin drafts/wNN`
9. Telegram checklist with branch link and file list

## Model policy

SourceHarvester script: no LLM. Scout, Diagram, Blog draft, LinkedIn: Tier 0. Architect, CloudMapper, Critic: Tier 1.

Never commit secrets. Never push to `main`.
