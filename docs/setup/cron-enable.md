# Enable Hermes cron (after Week 1 pilot)

Enable scheduled jobs only when OpenRouter spend is acceptable (target **under $3/week** in the pilot). Check spend with Telegram `cost`.

## 1. Create log directory

On the VPS as user `hermes`:

```bash
mkdir -p ~/logs
```

## 2. Install crontab entries

```bash
crontab -e
```

Paste the block from [hermes/cron.md](../../hermes/cron.md):

1. Daily **06:00 IST** — `git pull` on the hub clone.
2. **Thursday 06:30** — SourceHarvester (`--days 14`).
3. **Friday 07:00** — ResearchScout (adjust `hermes run` syntax to your Hermes version).
4. **Monday 08:00** — GrowthAnalyst (optional private repo metrics).
5. **Daily 07:00** — short harvest (`--days 2`) + DailyAIBrief.

## 3. Verify

1. Wait for the next scheduled run or trigger `news today` on Telegram manually.
2. Read `~/logs/harvest-daily.log` and `~/logs/daily-brief.log` for errors.
3. Confirm `content/source-corpus/latest.md` updates on the VPS clone.

## 4. If jobs fail

1. Run `python3 hermes/tools/harvest_sources.py --days 2` by hand.
2. Fix feed errors in [verified-sources.json](../../hermes/sources/verified-sources.json).
3. Reduce cron frequency until spend is stable.

## Related

- [week1-vps-pilot-remainder.md](week1-vps-pilot-remainder.md)
- [04-agent-operations.md](../roadmap/04-agent-operations.md)
