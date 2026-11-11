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

# Friday weekly pipeline — 07:05 UTC: scout + ADR + Telegram ADR card (--next from publish-progress)
5 7 * * 5 cd ~/work/agentic-ai-architecture && python3 hermes/tools/weekly_pipeline.py friday-adr >> ~/logs/weekly-pipeline.log 2>&1

# Legacy single scout only (optional if not using weekly_pipeline):
# 0 7 * * 5 ... hermes chat ... calendar_week.py --next --brief-prompt ...

# Telegram inline approvals — every 2 min (skip if Hermes owns getUpdates; use text adr approve wNN)
*/2 * * * * cd ~/work/agentic-ai-architecture && python3 hermes/tools/telegram_poll_approvals.py --once >> ~/logs/telegram-approvals.log 2>&1

# GrowthAnalyst — Monday 08:00 UTC = 13:30 IST
0 8 * * 1 cd ~/work/agentic-ai-architecture && hermes chat -q "Run the growth-analyst skill: produce this week's KPI nudge and topic steering." -s growth-analyst --oneshot >> ~/logs/growth.log 2>&1

# Weekly reminder — Monday 08:15 UTC = 13:45 IST (no LLM; nudges brief/pack on Telegram path)
15 8 * * 1 cd ~/work/agentic-ai-architecture && python3 hermes/tools/weekly_reminder.py >> ~/logs/weekly-reminder.log 2>&1

# News Inshorts — harvest + summarize daily 06:45 UTC (12:15 IST)
# --days 7 (was 3): the 3-day window plus cap-before-dedupe left only ~1-6 new
# items/day. Wider window + dedupe-then-cap gives ~26 new items per run.
# Pulse every 2 hours, NOT hourly: an hourly pulse (24/day) outran the supply and
# went dry 34 times out of 95 runs. 12/day is sustainable.
45 6 * * * cd ~/work/agentic-ai-architecture && python3 hermes/tools/harvest_sources.py --days 7 --json-out ~/.hermes/news-queue/harvest-latest.json >> ~/logs/news-harvest.log 2>&1 && python3 hermes/tools/news_ingest.py --max-per-publisher 4 >> ~/logs/news-ingest.log 2>&1 && python3 hermes/tools/news_summarize.py >> ~/logs/news-summarize.log 2>&1 && python3 hermes/tools/news_cleanup.py >> ~/logs/news-cleanup.log 2>&1

5 */2 * * * cd ~/work/agentic-ai-architecture && python3 hermes/tools/news_pulse_send.py >> ~/logs/news-pulse.log 2>&1
```

Exact `hermes run` syntax depends on Hermes version — replace with documented CLI or Telegram-triggered jobs if cron integration differs.

Create log dir: `mkdir -p ~/logs`

Enable cron after Week 1 pilot spend check: [docs/setup/cron-enable.md](../docs/setup/cron-enable.md).

Telegram should receive scout digest and Monday nudge when skills are wired.
