---
name: blog-writer
description: Long-form blog from ADR, mapping, and code. Tier 0 draft, Tier 1 optional pass.
---

# BlogWriter

Apply `_shared/ground-rules.md` and [content/voice-guide.md](../../../content/voice-guide.md).

## Tasks

Write `patterns/{week}-{slug}/blog.md`:

- 1,200–1,800 words
- Sections per voice guide (when not to use, AWS, Azure, checklist pointers)
- **Apply it to Acme** — increment in `projects/acme-support/` (see [07-running-use-case.md](../../../docs/roadmap/07-running-use-case.md))
- **Architect's notebook** — table: decision, rejected alternative, top failure mode, cost per 1k runs hint, NFRs
- **Prerequisites** — links to prior weeks from [content/calendar.md](../../../content/calendar.md)
- No employer references

Frontmatter for site sync (at top):

```yaml
---
title: ""
description: ""
pubDate: YYYY-MM-DD
patternWeek: wNN
level: Foundation | Practitioner | Production | Architect
acmeStage: wNN
---
```

Level by quarter: Q1 Foundation, Q2 Practitioner, Q3 Production, Q4 Architect.
