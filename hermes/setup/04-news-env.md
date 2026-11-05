# News Inshorts (RSS → queue → Telegram)

Deterministic pipeline. **No Hermes agent** for hourly sends. OpenRouter is used only in `news_summarize.py` (free model).

## 1. Directories

On the VPS as user `hermes`:

```bash
mkdir -p ~/.hermes/news-queue ~/logs
```

Queue state stays under `~/.hermes/news-queue/` (not committed to git).

## 2. Environment (`~/.hermes/.env`)

Add keys (never commit):

```bash
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_NEWS_MODEL=qwen/qwen3-235b-a22b:free
OPENROUTER_NEWS_MODEL_FALLBACK=google/gemma-2-9b-it:free
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

1. Run `chmod 600 ~/.hermes/.env`.
2. Refresh `:free` model slugs monthly on [OpenRouter](https://openrouter.ai/models).
3. News scripts **never** auto-escalate to paid models.

`TELEGRAM_CHAT_ID` is your numeric user id from @userinfobot (same allowlist as the Hermes gateway).

## 3. Cron

Install blocks from [../cron.md](../cron.md):

1. Daily **06:45 IST** — harvest (`--days 3 --json-out`), ingest, summarize, cleanup.
2. Hourly **:05** — `news_pulse_send.py` (one random unsent card).

Remove the old `hermes run skill daily-ai-brief` line if it is still present.

Enable only after pilot spend is acceptable: [../../docs/setup/cron-enable.md](../../docs/setup/cron-enable.md).

## 4. Smoke test (VPS)

Run after `git pull` on the hub clone:

```bash
cd ~/work/agentic-ai-architecture

python3 hermes/tools/harvest_sources.py --days 3 \
  --json-out ~/.hermes/news-queue/harvest-latest.json

python3 hermes/tools/news_ingest.py
python3 hermes/tools/news_summarize.py --limit 3
python3 hermes/tools/news_status.py
python3 hermes/tools/news_pulse_send.py --dry-run
python3 hermes/tools/news_pulse_send.py --force
python3 hermes/tools/news_status.py
```

1. `--dry-run` prints one Inshorts card without Telegram.
2. `--force` sends one live message (same as hourly cron).
3. Confirm one card in Telegram; `news_status.py` shows `ready` count down by one.

## 5. Manual Telegram hooks

Wire in Hermes gateway or shell aliases:

| User message | VPS command |
|--------------|-------------|
| `news today` | `python3 hermes/tools/news_pulse_send.py --force` |
| `news status` | `python3 hermes/tools/news_status.py` |

## 6. Logs

| Log | Job |
|-----|-----|
| `~/logs/news-harvest.log` | RSS harvest |
| `~/logs/news-ingest.log` | Queue upsert |
| `~/logs/news-summarize.log` | OpenRouter batch |
| `~/logs/news-pulse.log` | Hourly Telegram |
| `~/logs/news-cleanup.log` | 3-day retention |

## Related

- Skill: [../skills/news-inshorts/SKILL.md](../skills/news-inshorts/SKILL.md)
- Tools: `hermes/tools/news_*.py`, `harvest_sources.py --json-out`
- Ops: [../../docs/roadmap/04-agent-operations.md](../../docs/roadmap/04-agent-operations.md)
