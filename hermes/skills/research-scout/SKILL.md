---
name: research-scout
description: Weekly research brief for the next agentic architecture pattern. Tier 0 models preferred.
---

# ResearchScout

Read `_shared/ground-rules.md` constraints.

## Inputs

- Week id (e.g. `w05`) and slug from [content/calendar.md](../../../content/calendar.md)
- Prior patterns in `patterns/` to avoid duplication

## Tasks

1. Search recent papers, OSS releases, AWS and Azure AI blog posts (last 30 days relevant to topic).
2. Write `patterns/{week}-{slug}/brief.md` using [templates/brief.md](../../templates/brief.md).
3. Include **3 contrarian angles** (when NOT to use hype).
4. Cite URLs with access date.

## Output

- `brief.md` committed on branch `drafts/{week}` or reply summary on Telegram.

## Schedule

Friday 07:00 IST (see [cron.md](../../cron.md)).
