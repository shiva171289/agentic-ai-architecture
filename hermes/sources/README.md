# Verified vendor sources (grounding corpus)

Hermes agents **must not invent** vendor features, pricing, or service names. They ground claims in:

1. **Harvested RSS corpus** under [`content/source-corpus/`](../../content/source-corpus/) (written by **SourceHarvester**).
2. **Official doc roots** in [`verified-sources.json`](verified-sources.json) (CloudMapper / ReviewerCritic may fetch pages only from these trees or from links found in the corpus).

## Feed coverage

### RSS (harvested)

| Publisher | Feed id | Tags (optional) |
|-----------|---------|-----------------|
| AWS | `aws-ml-blog`, `aws-main-blog` | cloud, enterprise |
| Microsoft Azure | `azure-blog` | cloud, enterprise |
| Microsoft | `microsoft-devblogs`, `microsoft-foundry-devblog` | agents, cloud |
| OpenAI | `openai-blog` → `openai.com/news/rss.xml` | models, openai, agents |
| LangChain | `langchain-blog` | agents |
| Hugging Face | `huggingface-blog` | models |
| Import AI | `import-ai` | research |
| Karpathy | `karpathy-blog`, `karpathy-youtube` | karpathy |
| Palantir | `palantir-blog` | enterprise, agents |
| Google | `google-developers-blog`, `google-cloud-blog`, `google-deepmind-blog`, `google-research-blog` | google, cloud, research |
| NVIDIA | `nvidia-developer-blog` | agents, inference |
| Meta | `meta-ai-research` | research, open-models |
| Cohere | `cohere-blog` (`txt.cohere.com`) | enterprise, rag |
| Databricks | `databricks-blog` | enterprise, ml-platform |

### HTML index (link-only summaries)

| Publisher | Page id | Path prefix |
|-----------|---------|-------------|
| Anthropic | `anthropic-news` | `/news/` |
| Mistral | `mistral-news` | `/news/` |
| MCP | `mcp-blog` | `/posts/` |

### Doc roots (on-demand fetch)

AWS Bedrock, Azure AI Foundry, Azure OpenAI, OpenAI Platform, Anthropic docs, **Google AI (`ai.google.dev`)**.

## Daily brief selection

**SourceHarvester** writes all feeds into the corpus. **News Inshorts** ingest ([`news_ingest.py`](../tools/news_ingest.py)) prefers feeds tagged `agents`, `enterprise`, `mcp`, or `cloud`. Cap at **two items per publisher** per ingest run. Down-rank `aws-main-blog` unless the title matches agent/LLM keywords.

## Allowlist maintenance

- Edit `verified-sources.json` when adding a feed or doc root.
- Run harvest locally or on the VPS after changes.
- Re-verify RSS URLs monthly; update `updated` when URLs change.
- If Microsoft Research RSS returns 403 from the VPS, skip that feed until a working official URL exists.

## What is excluded on purpose

- Random Medium posts, unverified mirrors, and SEO scraper sites (Palantir’s **official** Medium publication is allowlisted via `blog.palantir.com/feed`).
- Third-party RSS aggregators (Olshansk, RSS.app, Alan Turing scraped feeds).
- Employer or customer-specific blogs.
- Paywalled content beyond RSS summaries (do not bypass paywalls).

## Related skills

- [`../skills/source-harvester/SKILL.md`](../skills/source-harvester/SKILL.md)
- [`../skills/news-inshorts/SKILL.md`](../skills/news-inshorts/SKILL.md)
- [`../skills/research-scout/SKILL.md`](../skills/research-scout/SKILL.md)
- [`../skills/reviewer-critic/SKILL.md`](../skills/reviewer-critic/SKILL.md)
