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
# News cards go here (group/channel id from @getidsbot or Bot API), not your DM:
TELEGRAM_CHAT_ID=-5144603731
# Hermes gateway (DM / home) — keep your user id here:
# TELEGRAM_HOME_CHANNEL=your_numeric_user_id
# TELEGRAM_ALLOWED_USERS=your_numeric_user_id
```

1. Run `chmod 600 ~/.hermes/.env`.
2. Refresh `:free` model slugs monthly on [OpenRouter](https://openrouter.ai/models).
3. News scripts **never** auto-escalate to paid models.
4. Add the bot to the target group and allow it to post messages.

**Routing:** `news_pulse_send.py` reads env in this order: `TELEGRAM_CHAT_ID`, then `TELEGRAM_HOME_CHANNEL`, then `TELEGRAM_ALLOWED_USERS`. Set **`TELEGRAM_CHAT_ID`** to the **group or channel** id (often negative, e.g. `-5144603731` for group `5144603731`). Do not point news at your personal user id unless you want DMs.

## 3. Cron

Install blocks from [../cron.md](../cron.md):

1. Daily **06:45 UTC** (12:15 IST) — harvest (`--days 7 --json-out`), ingest, summarize, cleanup.
2. Every **2 hours** at :05 — `news_pulse_send.py` (one random unsent card) = 12/day.

**Supply is the binding constraint.** `news_ingest.py` de-duplicates **before** applying
`--max-per-publisher`; doing it the other way round lets already-queued items eat each
publisher's budget and starves new ones (a 7-day run added 6 items instead of 26). Use a
**7-day** harvest window and leave the cap at 4. The pulse must stay below the resulting
supply — at 24/day (hourly) the log showed 61 sent and 34 dry runs. Cards can therefore be
up to a week old; lower the window if you prefer fresher cards and a shallower buffer.

The host runs `Etc/UTC` and its cron ignores `CRON_TZ`, so every time in [../cron.md](../cron.md)
is UTC. Convert before you copy.

Ingest runs with **`--max-per-publisher 4`**. The default of 2 supplied only ~17 items/day
against 24 hourly pulse slots, so the queue drained about 4 hours before the next refill
and the pulse silently logged `No summarized unsent items in queue`. Raise the cap (or add
a second daily run) if you want a deeper buffer; lower it if cards feel repetitive.

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
