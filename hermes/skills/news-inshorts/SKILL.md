---
name: news-inshorts
description: Hourly Inshorts cards from allowlisted RSS via VPS scripts. Summarize with OpenRouter free API only; no full Hermes run per hour.
---

# News Inshorts

Read `_shared/ground-rules.md` and [hermes/CONSTITUTION.md](../../CONSTITUTION.md). Apply **ASD-STE100** to headlines and body text in Telegram cards.

This skill documents the **script pipeline**. Do not run a full Hermes agent for hourly sends.

## Pipeline

1. **Harvest (no AI)** — `python3 hermes/tools/harvest_sources.py --days 3 --json-out ~/.hermes/news-queue/harvest-latest.json`
2. **Ingest** — `python3 hermes/tools/news_ingest.py`
3. **Summarize (OpenRouter free)** — `python3 hermes/tools/news_summarize.py`
4. **Send (no AI)** — `python3 hermes/tools/news_pulse_send.py` (hourly cron or `news today`)
5. **Retention** — `python3 hermes/tools/news_cleanup.py` (3 days)

State: `~/.hermes/news-queue/queue.json` (VPS only).

## Inputs

- Allowlisted feeds: [verified-sources.json](../../sources/verified-sources.json)
- Harvest JSON + markdown corpus under `content/source-corpus/`

## Selection (ingest)

1. Prefer feeds tagged `agents`, `enterprise`, `mcp`, `cloud`, or `karpathy`.
2. Cap **two** new items per publisher per ingest run.
3. Down-rank `aws-main-blog` unless title or excerpt matches agent/LLM keywords.
4. Skip thin HTML-index rows unless title matches agent keywords.

## Telegram card format

```text
📰 {headline}

{body}

🔗 {link}
```

1. Send `sendPhoto` when `image_url` exists in the RSS item (allowlisted host).
2. Otherwise send `sendMessage`.
3. Pick **one random** unsent summarized item per run.

## Grounding

1. Summaries use only title + RSS excerpt in the prompt.
2. Do not fetch full article HTML in v1.
3. Do not cite URLs outside the allowlist.

## Manual commands

| Command | Script |
|---------|--------|
| `news today` | `news_pulse_send.py --force` |
| `news status` | `news_status.py` |

Setup: [hermes/setup/04-news-env.md](../../setup/04-news-env.md).

## Schedule

See [cron.md](../../cron.md): daily 06:45 IST harvest+summarize; hourly :05 pulse.

## Model tier

**Tier 0 API only** in `news_summarize.py`. Default `OPENROUTER_NEWS_MODEL=qwen/qwen3-235b-a22b:free`. Fallback `google/gemma-2-9b-it:free` on 429.

Target: one completion per **new** queue item per day (not per hour).

## Outputs

- Telegram Inshorts cards only (no `content/daily-brief/` files).

## Deprecated

The old **DailyAIBrief** skill (`daily-ai-brief`) is replaced by this pipeline.
