# Hermes cron schedules (IST)

Add via `crontab -e` as user `hermes`. Adjust paths.

```cron
# Pull latest skills and templates (daily 6:00)
0 6 * * * cd ~/work/agentic-ai-architecture && git pull --ff-only origin main >> ~/logs/git-pull.log 2>&1

# ResearchScout — Friday 7:00 (next week brief)
0 7 * * 5 cd ~/work/agentic-ai-architecture && hermes run skill research-scout --week auto >> ~/logs/scout.log 2>&1

# GrowthAnalyst — Monday 8:00
0 8 * * 1 hermes run skill growth-analyst >> ~/logs/growth.log 2>&1
```

Exact `hermes run` syntax depends on Hermes version — replace with documented CLI or Telegram-triggered jobs if cron integration differs.

Create log dir: `mkdir -p ~/logs`

Telegram should receive scout digest and Monday nudge when skills are wired.
