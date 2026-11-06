---
name: source-harvester
description: Pull allowlisted vendor blog RSS into a dated grounding corpus. Tier 0; no LLM required for harvest script.
---

# SourceHarvester

Read `_shared/ground-rules.md`. This agent **collects facts**; it does not write opinion or pattern content.

## Purpose

Ground ResearchScout, CloudMapper, BlogWriter, and ReviewerCritic in **verified vendor sources** (AWS, Azure, Anthropic, OpenAI, Google Cloud AI, LangChain official blogs, plus official doc roots). Reduces hallucinated service names and feature claims.

## Allowlist (mandatory)

- Config: [hermes/sources/verified-sources.json](../../sources/verified-sources.json)
- Human notes: [hermes/sources/README.md](../../sources/README.md)

Never fetch or cite URLs outside `allowed_link_hosts` and `doc_roots` unless the URL appeared in today's harvested corpus entry.

## Inputs

- Optional week id `wNN` and slug (for keyword filter from [content/calendar.md](../../../content/calendar.md))
- Optional `--days` (default 14) and `--keywords` for the harvest script

## Tasks

1. **Run the harvest script** (preferred — deterministic, cheap):

   ```bash
   cd ~/work/agentic-ai-architecture
   python3 hermes/tools/harvest_sources.py --days 14
   ```

   If `pack wNN` or `brief wNN` includes a topic, derive 3–8 keywords from the calendar title and pattern slug, then:

   ```bash
   python3 hermes/tools/harvest_sources.py --days 30 --keywords "agent,orchestrator,bedrock,foundry"
   ```

2. Confirm outputs exist:
   - `content/source-corpus/YYYY-MM-DD.md`
   - `content/source-corpus/latest.md` (pointer copy for agents)

3. If a feed fails, log the error, **do not substitute** random web search results. Update `verified-sources.json` in a human-reviewed commit if RSS URLs moved.

   Known-good Karpathy source (verified 2026-11-04, YouTube dropped 2026-11-06):
   - Blog RSS: `https://karpathy.github.io/feed.xml` (Jekyll, low cadence).
   - **YouTube: removed.** `youtube.com/feeds/videos.xml` now fails from the VPS for
     both the correct channel ID (`UCXUPKJO5MZQN11PqgIvyuvQ`) and the old one — first
     404, then 500, with a Google error page for any User-Agent. Treat the endpoint as
     blocked from this host; do not re-add it without re-testing.
   - When a feed returns 404 or 500, confirm the failure is the endpoint and not your
     config: test the URL directly with two different channel IDs before editing config.
   - X/Twitter (`@karpathy`) has **no official RSS feed**. Do not scrape X in v1. Use the X API only if a human approves credentials.

   The harvest script rewrites `latest.md` on **every** run, including `--out` runs. To probe a wide window without clobbering the shared corpus, pass `--days N --out` to a scratch path first, then re-run the intended window to restore `latest.md`.

4. Optional (Tier 0 LLM): append a **10-line digest** at the bottom of today's corpus file — only bullet summaries of entries already in the file, with the same URLs.

## Outputs

- Dated corpus markdown under `content/source-corpus/`
- Telegram summary: entry count, feeds that failed, path to `latest.md`

## Downstream rules

- **ResearchScout** must cite primarily from `content/source-corpus/latest.md` plus arXiv/OSS releases.
- **ReviewerCritic** rejects vendor-specific claims whose URLs are not in the corpus, `brief.md` sources table, or official doc roots.

## Schedule

Thursday 06:30 IST (see [cron.md](../../cron.md)) — before Friday ResearchScout.

## Telegram

- `sources refresh` — full harvest (14 days)
- `sources w05` — harvest with keywords from week 05 calendar entry
