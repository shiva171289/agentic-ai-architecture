# Qwen and model tiers for the weekly pipeline

OpenRouter **paid Qwen** slugs are the default cheap workhorse (news summarization already uses them). Free `:free` Qwen slugs often return 404 — see [hermes/tools/job_status.py](../../hermes/tools/job_status.py).

Set on the VPS in `~/.hermes/.env`:

```bash
OPENROUTER_NEWS_MODEL=qwen/qwen3-235b-a22b-2507
OPENROUTER_PACK_MODEL=qwen/qwen3-235b-a22b-2507
OPENROUTER_ADR_MODEL=qwen/qwen3-235b-a22b-2507
```

Mirror the same slugs in `~/.hermes/config.yaml` for Hermes Tier 0 auxiliary tasks where supported.

## Weekly pipeline mapping

| Step | Skill | Suggested model |
|------|--------|-----------------|
| Corpus harvest | script | No LLM |
| Brief | research-scout | Tier 0 / `OPENROUTER_PACK_MODEL` (Qwen) |
| ADR draft | pattern-architect | `OPENROUTER_ADR_MODEL` (Qwen) |
| Cloud map | cloud-mapper | Qwen or Tier 1 if tool errors |
| Code / diagram | code-builder, diagram-agent | Qwen |
| Blog / LinkedIn | blog-writer, linkedin-editor | Qwen |
| Critic | reviewer-critic | Qwen; escalate to Tier 1 only on retry |
| Full pack | weekly-pack | Inherits per sub-skill |
| Publish | trigger_publish.py | No LLM |

**Rule:** One Tier 1 fallback for ADR or critic if Qwen drops tool calls — never auto-premium.

## Related

- [04-agent-operations.md](../roadmap/04-agent-operations.md)
- [04-news-env.md](../../hermes/setup/04-news-env.md)
