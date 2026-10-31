---
name: daily-ai-brief
description: Daily ASD-STE100 AI news digest for Telegram and LinkedIn prep. Tier 0 preferred. Separate from weekly-pack.
---

# DailyAIBrief

Read `_shared/ground-rules.md` and [hermes/CONSTITUTION.md](../../CONSTITUTION.md). Apply **ASD-STE100** to every headline and item body.

## Inputs

- **Corpus:** [content/source-corpus/latest.md](../../../content/source-corpus/latest.md) (must be ≤2 days old; if stale, run SourceHarvester with `--days 2` first)
- **Karpathy feeds:** entries tagged `karpathy-*` in [verified-sources.json](../../sources/verified-sources.json)
- **Window:** last 24–48 hours from feed `pubDate` or corpus `fetched` timestamp

## Tasks

1. Run or confirm fresh harvest (`python3 hermes/tools/harvest_sources.py --days 2`).
2. Scan corpus and Karpathy feeds for new items in the window.
3. Select **5–10** items relevant to enterprise agentic AI (models, agents, RAG, tools, cloud AI, safety). Prefer corpus-backed vendor releases.
4. Write **Karpathy watch** section:
   - If new Karpathy blog or video exists, one ASD-STE100 item with primary URL.
   - If none, state: **No new Karpathy post in window.** Do not invent posts.
5. Write `content/daily-brief/YYYY-MM-DD.md` using [content/daily-brief/TEMPLATE.md](../../../content/daily-brief/TEMPLATE.md).
6. Send Telegram summary: numbered list, each item ≤50 words + URL. Total read time target: under 3 minutes.
7. Do **not** auto-post to LinkedIn. Add one optional **LinkedIn angle** line per item for the human editor.

## Output format (per item)

- **Headline:** 12 words or fewer
- **Body:** 2–3 sentences, 50 words or fewer
- **Source:** single allowlisted URL
- **LinkedIn angle:** one sentence (optional)

## Grounding

- Do not cite URLs outside [verified-sources.json](../../sources/verified-sources.json) allowlist unless the URL appeared in the corpus from an allowlisted feed in the same run.
- No X/Twitter scraping in v1.

## Output files

- `content/daily-brief/YYYY-MM-DD.md`
- Telegram message to allowed user(s) only

## Schedule

Daily 07:00 IST (see [cron.md](../../cron.md)). Manual: Telegram `news today`.

## Model tier

Tier 0 for summarization. Tier 1 only if Tier 0 fails twice.

## Cost

Target **<$0.15/day** paid tokens. If exceeded, reduce to 5 items and Karpathy block only.
