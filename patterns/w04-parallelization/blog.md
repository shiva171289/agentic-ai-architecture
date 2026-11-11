---
title: "Parallelization: fetch policy and order context together"
description: "Independent I/O in parallel, then one synthesis call — before orchestrator-workers."
pubDate: 2026-11-21
patternWeek: w04
level: Foundation
acmeStage: w04
spineLayers: "2"
---

## Prerequisites

[w03 routing](/blog/w03-routing/).

## Pattern

Run **policy retrieval** and **order snippet** concurrently when neither depends on the other. Merge contexts, then run the w02 answer chain.

Order data is synthetic in `data/orders.json`. Real `get_order_status` tool arrives w10.

## Apply it to Acme

`answer_with_parallel_context()` uses `ThreadPoolExecutor`.

## Architect's notebook

| Field | Notes |
|-------|-------|
| Decision | Two-worker thread pool |
| Rejected | Sequential (higher latency) |
| Failure mode | Race on shared non-thread-safe client |
| Cost hint | Saves wall-clock, not tokens |
| NFRs | Latency |

## Disclaimer

Learning material only.
