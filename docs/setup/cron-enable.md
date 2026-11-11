# Enable Hermes cron (after Week 1 pilot)

Enable scheduled jobs only when OpenRouter spend is acceptable (target **under $3/week** in the pilot). Check spend with Telegram `cost`.

The VPS runs **UTC** (`Etc/UTC`). [hermes/cron.md](../../hermes/cron.md) lists **UTC** minute/hour fields. Ist equivalents appear in comments there.

## 1. Create log directory

On the VPS as user `hermes`:

```bash
mkdir -p ~/logs
```

## 2. Install crontab entries

```bash
crontab -e
```

Paste the full block from [hermes/cron.md](../../hermes/cron.md).

**You must keep the PATH line** as the first job line. Without it, `hermes` is not found.

| Job | UTC schedule | IST (approx.) | Action |
|-----|--------------|-----------------|--------|
| git pull | `0 6 * * *` | 11:30 | Sync hub clone |
| SourceHarvester | `30 6 * * 4` | Thu 12:00 | RSS corpus |
| Weekly pipeline | `5 7 * * 5` | Fri 12:35 | ADR draft + Telegram approve card (`--next` week) |
| Telegram poll | `*/2 * * * *` | Every 2 min | Inline Approve/Reject (optional) |
| GrowthAnalyst | `0 8 * * 1` | Mon 13:30 | KPI nudge |
| Weekly reminder | `15 8 * * 1` | Mon 13:45 | Deterministic pack nudge (no LLM) |
| News pipeline | `45 6 * * *` | 12:15 | Harvest, ingest, summarize |
| News pulse | `5 */2 * * *` | Every 2h | One Inshorts card |

ResearchScout uses [calendar_week.py](../../hermes/tools/calendar_week.py) so the target week matches [content/calendar.md](../../content/calendar.md).

**Cron does not run `pack wNN`.** After Friday scout or Monday reminder, send `brief wNN slug` and `pack wNN` on Telegram.

Configure `~/.hermes/.env` before enabling news cron: [hermes/setup/04-news-env.md](../../hermes/setup/04-news-env.md).

## 3. Verify

1. Run `python3 hermes/tools/job_status.py` on the VPS.
2. Run `python3 hermes/tools/calendar_week.py --json`.
3. Run `python3 hermes/tools/weekly_reminder.py`.
4. Trigger `news today` on Telegram or wait for the next news cron.
5. Read `~/logs/scout.log`, `~/logs/growth.log`, and `~/logs/news-harvest.log` for errors.
6. Confirm `content/source-corpus/latest.md` updates after harvest.

## 4. If jobs fail

1. Run the smoke steps in [hermes/setup/04-news-env.md](../../hermes/setup/04-news-env.md) by hand.
2. Fix feed errors in [verified-sources.json](../../hermes/sources/verified-sources.json).
3. Reduce summarize batch size with `news_summarize.py --limit 10` until OpenRouter free limits stabilize.
4. Re-check crontab PATH and `which hermes` as user `hermes`.

## Related

- [week1-vps-pilot-remainder.md](week1-vps-pilot-remainder.md)
- [04-agent-operations.md](../roadmap/04-agent-operations.md)
