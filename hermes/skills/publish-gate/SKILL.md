---
name: publish-gate
description: After human Telegram approval, dispatch GitHub Actions to merge drafts/wNN to main and deploy Pages.
---

# PublishGate

Read `_shared/ground-rules.md` and [hermes/CONSTITUTION.md](../../CONSTITUTION.md).

## Command

`approve publish wNN` (Telegram)

Optional: `publish status wNN` — summarize whether `drafts/wNN` exists and last CI state (if Checks API available).

## Preconditions

1. Branch `drafts/wNN` exists on `origin` with the full weekly pack.
2. Human already polished code on laptop (recommended) or accepts agent draft quality.
3. VPS `~/.hermes/.env` contains `GITHUB_PAT` with **Actions** and **Contents** write on the hub repo.
4. GitHub repo has workflow [publish-approved-week.yml](../../../.github/workflows/publish-approved-week.yml).
5. If `main` is branch-protected, allow GitHub Actions to push or store `PUBLISH_PAT` secret for the workflow push step (see [04-agent-operations.md](../../../docs/roadmap/04-agent-operations.md)).

## Workflow

1. Load `patterns/wNN-slug/` from the local clone (`git fetch origin drafts/wNN`).
2. Send Telegram **approval checklist** before dispatch:
   - Blog title (from `blog.md` H1)
   - First ~200 words of blog body
   - LinkedIn Post A and Post B headers from `linkedin.md`
   - Branch link on GitHub
   - Text: **Reply `approve publish wNN` to merge to main and deploy GitHub Pages.**
3. On explicit `approve publish wNN`:
   - Resolve slug from [content/calendar.md](../../../content/calendar.md) (e.g. `w01` → `w01-augmented-llm`).
   - Run:
     ```bash
     cd ~/work/agentic-ai-architecture
     python3 hermes/tools/trigger_publish.py wNN wNN-slug
     ```
4. Reply with Actions URL and expected Pages path: `/blog/wNN-slug/`.
5. Paste LinkedIn Post A/B bodies from `linkedin.md` for **manual** posting (agents never post to LinkedIn).

## Failure handling

1. If dispatch fails, print API error; do not push to `main` from the VPS with the deploy key.
2. If Actions merge fails, human merges on laptop per [week1-vps-pilot-remainder.md](../../../docs/setup/week1-vps-pilot-remainder.md).

## Security

- Never commit `GITHUB_PAT`.
- Log approval date and week in private `metrics.md`.

## Related

- [weekly-pack/SKILL.md](../weekly-pack/SKILL.md)
- [trigger_publish.py](../../tools/trigger_publish.py)
