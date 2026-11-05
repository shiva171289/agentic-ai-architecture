# Hermes cron schedules (IST)

Add via `crontab -e` as user `hermes`. Adjust paths.

```cron
# Pull latest skills and templates (daily 6:00)
0 6 * * * cd ~/work/agentic-ai-architecture && git pull --ff-only origin main >> ~/logs/git-pull.log 2>&1

# SourceHarvester — Thursday 6:30 (RSS corpus before scout)
30 6 * * 4 cd ~/work/agentic-ai-architecture && python3 hermes/tools/harvest_sources.py --days 14 >> ~/logs/harvest.log 2>&1

# ResearchScout — Friday 7:00 (next week brief)
0 7 * * 5 cd ~/work/agentic-ai-architecture && hermes run skill research-scout --week auto >> ~/logs/scout.log 2>&1

# GrowthAnalyst — Monday 8:00
0 8 * * 1 cd ~/work/agentic-ai-architecture && hermes run skill growth-analyst >> ~/logs/growth.log 2>&1

# News Inshorts — harvest + summarize daily 06:45; pulse hourly :05
45 6 * * * cd ~/work/agentic-ai-architecture && python3 hermes/tools/harvest_sources.py --days 3 --json-out ~/.hermes/news-queue/harvest-latest.json >> ~/logs/news-harvest.log 2>&1 && python3 hermes/tools/news_ingest.py >> ~/logs/news-ingest.log 2>&1 && python3 hermes/tools/news_summarize.py >> ~/logs/news-summarize.log 2>&1 && python3 hermes/tools/news_cleanup.py >> ~/logs/news-cleanup.log 2>&1

5 * * * * cd ~/work/agentic-ai-architecture && python3 hermes/tools/news_pulse_send.py >> ~/logs/news-pulse.log 2>&1
```

Exact `hermes run` syntax depends on Hermes version — replace with documented CLI or Telegram-triggered jobs if cron integration differs.

Create log dir: `mkdir -p ~/logs`

Enable cron after Week 1 pilot spend check: [docs/setup/cron-enable.md](../docs/setup/cron-enable.md).

Telegram should receive scout digest and Monday nudge when skills are wired.
