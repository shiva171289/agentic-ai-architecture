# Hermes cron schedules

**All times below are UTC.** The VPS runs `Etc/UTC` (`timedatectl` → Etc/UTC, +0000), and
this host's cron is vixie `cron 3.0pl1`, which does **not** honour `CRON_TZ` (verified:
the string is absent from `/usr/sbin/cron`). So a bare `45 6` fires at 06:45 UTC,
not 06:45 IST. IST equivalents are shown in brackets. To move a job, convert it to UTC
and edit the comment in the same commit.

Add via `crontab -e` as user `hermes`. Adjust paths.

```cron
# Pull latest skills and templates (daily 06:00 UTC = 11:30 IST)
0 6 * * * cd ~/work/agentic-ai-architecture && git pull --ff-only origin main >> ~/logs/git-pull.log 2>&1

# SourceHarvester — Thursday 06:30 UTC = 12:00 IST (RSS corpus before scout)
30 6 * * 4 cd ~/work/agentic-ai-architecture && python3 hermes/tools/harvest_sources.py --days 14 >> ~/logs/harvest.log 2>&1

# ResearchScout — Friday 07:00 UTC = 12:30 IST (next week brief)
0 7 * * 5 cd ~/work/agentic-ai-architecture && hermes run skill research-scout --week auto >> ~/logs/scout.log 2>&1

# GrowthAnalyst — Monday 08:00 UTC = 13:30 IST
0 8 * * 1 cd ~/work/agentic-ai-architecture && hermes run skill growth-analyst >> ~/logs/growth.log 2>&1

# News Inshorts — harvest + summarize daily 06:45 UTC (12:15 IST); pulse hourly :05
# --max-per-publisher 4 (was 2): the cap of 2 supplied ~17 items/day against 24 hourly
# pulse slots, so the queue always drained ~4h before the next refill and the pulse
# logged "No summarized unsent items in queue". Cap 4 supplies ~30-35/day.
45 6 * * * cd ~/work/agentic-ai-architecture && python3 hermes/tools/harvest_sources.py --days 3 --json-out ~/.hermes/news-queue/harvest-latest.json >> ~/logs/news-harvest.log 2>&1 && python3 hermes/tools/news_ingest.py --max-per-publisher 4 >> ~/logs/news-ingest.log 2>&1 && python3 hermes/tools/news_summarize.py >> ~/logs/news-summarize.log 2>&1 && python3 hermes/tools/news_cleanup.py >> ~/logs/news-cleanup.log 2>&1

5 * * * * cd ~/work/agentic-ai-architecture && python3 hermes/tools/news_pulse_send.py >> ~/logs/news-pulse.log 2>&1
```

Exact `hermes run` syntax depends on Hermes version — replace with documented CLI or Telegram-triggered jobs if cron integration differs.

Create log dir: `mkdir -p ~/logs`

Enable cron after Week 1 pilot spend check: [docs/setup/cron-enable.md](../docs/setup/cron-enable.md).

Telegram should receive scout digest and Monday nudge when skills are wired.
