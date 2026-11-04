# Week 1 pilot — VPS remainder (after hub repo update)

Run these on the Hostinger VPS as user `hermes` after you `git pull` the hub repo (extended news sources and publish-gate skill).

## 1. Sync repo and skills

```bash
cd ~/work/agentic-ai-architecture
git pull --ff-only origin main
for d in ~/work/agentic-ai-architecture/hermes/skills/*/; do
  ln -sf "$d" ~/.hermes/skills/"$(basename "$d")"
done
```

## 2. Harvest and daily news

```bash
python3 hermes/tools/harvest_sources.py --days 30 --keywords "llm,augmented,bedrock,adk,agent"
```

From Telegram:

```text
news today
```

## 3. Week 1 draft pack

```text
brief w01 augmented-llm
pack w01
```

When the pack pauses for ADR:

```text
adr w01 approve
```

## 4. Cost check

```text
cost
```

Target **under $3/week** paid OpenRouter tokens before enabling cron ([hermes/cron.md](../../hermes/cron.md)).

## 5. Laptop polish

On your laptop:

1. `git fetch origin && git checkout drafts/w01`
2. Polish in Cursor; run `uv run pytest` under `patterns/w01-augmented-llm/code`
3. Push updates to `drafts/w01` if needed

## 6. Publish to GitHub Pages

**Option A — Telegram (after `publish-gate` skill and GitHub secrets):**

```text
approve publish w01
```

**Option B — Manual merge:**

```bash
git checkout main
git merge drafts/w01
git push origin main
```

Confirm GitHub Actions: **Test pattern code** and **Deploy site to GitHub Pages**.

## 7. LinkedIn

1. Edit [patterns/w01-augmented-llm/linkedin.md](../../patterns/w01-augmented-llm/linkedin.md) for voice.
2. Post manually (see [content/linkedin-pillars.md](../../content/linkedin-pillars.md)).
3. Update Featured: [linkedin-featured-checklist.md](linkedin-featured-checklist.md).

## Related

- [hermes/PILOT-RUNBOOK.md](../../hermes/PILOT-RUNBOOK.md)
- [week1-operating-guide.md](week1-operating-guide.md)
