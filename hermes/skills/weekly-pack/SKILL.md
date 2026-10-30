---
name: weekly-pack
description: Orchestrate full weekly pattern pack onto drafts branch after ADR approval.
---

# WeeklyPack orchestrator

Enforce `_shared/ground-rules.md` across subagents.

## Command

`pack wNN` (Telegram or CLI)

## Workflow

1. **ResearchScout** if `brief.md` missing or stale (>7 days).
2. **PatternArchitect** → pause until human approves ADR on Telegram.
3. Parallel:
   - **CloudMapper**
   - **CodeBuilder**
   - **DiagramAgent**
4. **BlogWriter** (after 3 completes)
5. **LinkedInEditor**
6. **ReviewerCritic** → fix loop once
7. Git:
   - `git checkout -B drafts/wNN`
   - Commit all files under `patterns/wNN-slug/`
   - `git push -u origin drafts/wNN`
8. Telegram checklist with branch link and file list

## Model policy

Scout, Diagram, Blog draft, LinkedIn: Tier 0. Architect, CloudMapper, Critic: Tier 1.

Never commit secrets. Never push to `main`.
