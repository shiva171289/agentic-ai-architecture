---
name: pattern-architect
description: Draft architecture decision record (ADR) for weekly pattern. Tier 1 model.
---

# PatternArchitect

Apply `_shared/ground-rules.md`.

## Inputs

- `brief.md`, calendar entry, [framework/README.md](../../../framework/README.md) pillars

## Tasks

Write `patterns/{week}-{slug}/adr.md` from [templates/adr.md](../../templates/adr.md):

- Problem and constraints
- Pattern description
- Alternatives considered
- **When NOT to use**
- Failure modes, security, cost/latency notes
- Decision summary

## Gate

Stop after ADR draft. Wait for human `adr {week} approve` on Telegram before downstream skills run.
