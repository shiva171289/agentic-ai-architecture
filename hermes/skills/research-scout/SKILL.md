---
name: research-scout
description: Weekly research brief for the next agentic architecture pattern. Tier 0 models preferred.
---

# ResearchScout

Read `_shared/ground-rules.md` constraints.

## Inputs

- Week id (e.g. `w05`) and slug from [content/calendar.md](../../../content/calendar.md)
- Prior patterns in `patterns/` to avoid duplication
- **SourceHarvester corpus:** [content/source-corpus/latest.md](../../../content/source-corpus/latest.md) (must be ≤7 days old; if stale, run **SourceHarvester** first)

## Tasks

1. Read `content/source-corpus/latest.md`. Prefer corpus entries for AWS, Azure, Anthropic, OpenAI, and Google Cloud claims.
2. Add arXiv papers and major OSS releases (GitHub releases/changelogs) when relevant — cite primary links only.
3. Do **not** invent vendor features. If the corpus and official docs do not support a claim, omit it or label **Open question** in the brief.
4. Write `patterns/{week}-{slug}/brief.md` using [templates/brief.md](../../templates/brief.md).
5. Include **3 contrarian angles** (when NOT to use hype).
6. Cite URLs with access date. Every vendor blog claim must use a URL from the corpus or [verified-sources.json](../../sources/verified-sources.json) doc roots.

## Output

- `brief.md` committed on branch `drafts/{week}` or reply summary on Telegram.

## Schedule

Friday 07:00 IST (see [cron.md](../../cron.md)).

## Pattern Radar (first Friday of month)

In addition to the weekly brief:

1. Create `content/radar/YYYY-MM.md` using template below.
2. Summarize 3–5 **corpus-backed** items (vendor releases, papers, OSS) from `content/source-corpus/latest.md`.
3. For each item: **Acme plug-in point** (which week/stage would adopt it).
4. Keep under ~600 words; suitable for LinkedIn thread or short blog.
5. Do not replace the evergreen weekly pattern topic.

Template:

```markdown
# Pattern Radar — YYYY-MM

## Highlights

| Item | Source | Acme plug-in |
|------|--------|--------------|
| ... | url | e.g. w35 model routing |

## Skip list

Patterns we are **not** chasing this month (and why).
```
