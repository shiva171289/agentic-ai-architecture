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
5. **Daily 06:45 IST** — news harvest + ingest + summarize + cleanup (see [04-news-env.md](../../hermes/setup/04-news-env.md)).
6. **Hourly :05** — one Inshorts Telegram card.

Configure `~/.hermes/.env` before enabling news cron: [hermes/setup/04-news-env.md](../../hermes/setup/04-news-env.md).

## 3. Verify

1. Wait for the next scheduled run or trigger `news today` on Telegram manually.
2. Read `~/logs/news-harvest.log`, `~/logs/news-summarize.log`, and `~/logs/news-pulse.log` for errors.
3. Run `python3 hermes/tools/news_status.py` on the VPS.
4. Confirm `content/source-corpus/latest.md` updates on the VPS clone after harvest.

## 4. If jobs fail

1. Run the smoke steps in [hermes/setup/04-news-env.md](../../hermes/setup/04-news-env.md) by hand.
2. Fix feed errors in [verified-sources.json](../../hermes/sources/verified-sources.json).
3. Reduce summarize batch size with `news_summarize.py --limit 10` until OpenRouter free limits stabilize.

## Related

- [week1-vps-pilot-remainder.md](week1-vps-pilot-remainder.md)
- [04-agent-operations.md](../roadmap/04-agent-operations.md)
