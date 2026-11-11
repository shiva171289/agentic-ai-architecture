# Scenario ladder — prompt flow

| Variant | When you need it | This week | Ships |
|---------|------------------|-----------|-------|
| Single mega-prompt | Tiny domain, few intents | No | — |
| Classify → answer chain | Distinct intents, shared corpus | **Yes** | w02 |
| Router + model tier | Cost/latency tradeoffs | No | w03 |
| Parallel context gather | Independent data sources | No | w04 |

## Open questions

- When does mis-routing cost more than a capable single call?
