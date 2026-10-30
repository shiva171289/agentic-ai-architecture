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
