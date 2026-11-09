# Hermes cron schedules

**All times below are UTC.** The VPS runs `Etc/UTC` (`timedatectl` → Etc/UTC, +0000), and
this host's cron is vixie `cron 3.0pl1`, which does **not** honour `CRON_TZ` (verified:
the string is absent from `/usr/sbin/cron`). So a bare `45 6` fires at 06:45 UTC,
not 06:45 IST. IST equivalents are shown in brackets. To move a job, convert it to UTC
and edit the comment in the same commit.

Add via `crontab -e` as user `hermes`. Adjust paths.

```cron
# cron runs with PATH=/usr/bin:/bin, which does NOT contain ~/.local/bin.
# Without this line every `hermes` job dies with "/bin/sh: 1: hermes: not found".
PATH=/home/hermes/.local/bin:/usr/local/bin:/usr/bin:/bin

# Pull latest skills and templates (daily 06:00 UTC = 11:30 IST)
0 6 * * * cd ~/work/agentic-ai-architecture && git pull --ff-only origin main >> ~/logs/git-pull.log 2>&1

# SourceHarvester — Thursday 06:30 UTC = 12:00 IST (RSS corpus before scout)
30 6 * * 4 cd ~/work/agentic-ai-architecture && python3 hermes/tools/harvest_sources.py --days 14 >> ~/logs/harvest.log 2>&1

# ResearchScout — Friday 07:00 UTC = 12:30 IST (next week brief)
# NOTE: `hermes run skill X` does not exist (v0.22.6 rejects `run`). Use chat -q with -s.
0 7 * * 5 cd ~/work/agentic-ai-architecture && hermes chat -q "Run the research-scout skill: write the weekly research brief for the next pattern week per content/calendar.md." -s research-scout --oneshot >> ~/logs/scout.log 2>&1

# GrowthAnalyst — Monday 08:00 UTC = 13:30 IST
0 8 * * 1 cd ~/work/agentic-ai-architecture && hermes chat -q "Run the growth-analyst skill: produce this week's KPI nudge and topic steering." -s growth-analyst --oneshot >> ~/logs/growth.log 2>&1

# News Inshorts — harvest + summarize daily 06:45 UTC (12:15 IST)
# --max-per-publisher 4 (was 2): cap 2 let only ~17 items/day through.
# Pulse every 2 hours, NOT hourly: the allowlisted feeds yield only ~15-20
# qualifying new items/day, so an hourly pulse (24/day) outran the supply and
# went dry 34 times out of 95 runs. 12/day is sustainable.
45 6 * * * cd ~/work/agentic-ai-architecture && python3 hermes/tools/harvest_sources.py --days 3 --json-out ~/.hermes/news-queue/harvest-latest.json >> ~/logs/news-harvest.log 2>&1 && python3 hermes/tools/news_ingest.py --max-per-publisher 4 >> ~/logs/news-ingest.log 2>&1 && python3 hermes/tools/news_summarize.py >> ~/logs/news-summarize.log 2>&1 && python3 hermes/tools/news_cleanup.py >> ~/logs/news-cleanup.log 2>&1

5 */2 * * * cd ~/work/agentic-ai-architecture && python3 hermes/tools/news_pulse_send.py >> ~/logs/news-pulse.log 2>&1
```

Exact `hermes run` syntax depends on Hermes version — replace with documented CLI or Telegram-triggered jobs if cron integration differs.

Create log dir: `mkdir -p ~/logs`

Enable cron after Week 1 pilot spend check: [docs/setup/cron-enable.md](../docs/setup/cron-enable.md).

Telegram should receive scout digest and Monday nudge when skills are wired.
