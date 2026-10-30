# Verified vendor sources (grounding corpus)

Hermes agents **must not invent** vendor features, pricing, or service names. They ground claims in:

1. **Harvested RSS corpus** under [`content/source-corpus/`](../../content/source-corpus/) (written by **SourceHarvester**).
2. **Official doc roots** in [`verified-sources.json`](verified-sources.json) (CloudMapper / ReviewerCritic may fetch pages only from these trees or from links found in the corpus).

## Feed coverage

- **RSS:** AWS (main + ML), Azure blog, Microsoft DevBlogs (broad + Foundry), OpenAI blog, LangChain blog
- **HTML index (link-only summaries):** Anthropic News (`/news/` paths)
- **Doc roots (on-demand fetch):** AWS Bedrock, Azure AI Foundry, Azure OpenAI, OpenAI Platform, Anthropic docs

Google Cloud blog has no stable public RSS in this config; use `ai.google.dev` doc roots if you add them later.

## Allowlist maintenance

- Edit `verified-sources.json` when adding a feed or doc root.
- Run harvest locally or on the VPS after changes.
- If a feed 404s, check the vendor’s blog page for a new RSS URL and update `updated`.

## What is excluded on purpose

- Random Medium posts, unverified mirrors, and SEO scraper sites.
- Employer or customer-specific blogs.
- Paywalled content beyond RSS summaries (do not bypass paywalls).

## Related skills

- [`../skills/source-harvester/SKILL.md`](../skills/source-harvester/SKILL.md)
- [`../skills/research-scout/SKILL.md`](../skills/research-scout/SKILL.md)
- [`../skills/reviewer-critic/SKILL.md`](../skills/reviewer-critic/SKILL.md)
