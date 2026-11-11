---
title: "Routing: fast model for easy tickets, capable model for hard ones"
description: "Heuristic model routing after prompt chaining — before gateways and caching."
pubDate: 2026-11-14
patternWeek: w03
level: Foundation
acmeStage: w03
spineLayers: "1,2"
---

## Prerequisites

[w02 prompt chaining](/blog/w02-prompt-chaining/).

## Pattern

After classify + retrieve, pick **fast** or **capable** mock model using heuristics (length, intent=other, dispute words).

**Spine:** Layers 1 and 2.

## Scenario ladder

Production **model routing & cost** ships w35. This week is heuristic only.

## Apply it to Acme

`route_and_answer()` in `projects/acme-support/core/support.py`.

## Architect's notebook

| Field | Notes |
|-------|-------|
| Decision | Heuristic router |
| Rejected | Premium-only |
| Failure mode | Complex FAQ misclassified as simple |
| Cost hint | Order-of-magnitude 3–10× cheaper fast path |
| NFRs | Latency on simple path |

## Disclaimer

Learning material only.
