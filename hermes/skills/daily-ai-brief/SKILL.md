---
name: daily-ai-brief
description: DEPRECATED — replaced by news-inshorts script pipeline (hourly Telegram Inshorts).
---

# DailyAIBrief (deprecated)

**Do not use** for new cron jobs.

Use [news-inshorts](../news-inshorts/SKILL.md) and the VPS tools in [hermes/setup/04-news-env.md](../../setup/04-news-env.md):

1. `harvest_sources.py --json-out`
2. `news_ingest.py`
3. `news_summarize.py`
4. `news_pulse_send.py`

Manual Telegram `news today` maps to `news_pulse_send.py --force`.

Historical brief files under `content/daily-brief/` are archive only; do not create new dated briefs.
