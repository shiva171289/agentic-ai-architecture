# Scenario ladder — orchestrator-workers

List variants for this pattern family. Implement **only** this week's row; link to future weeks for the rest.

| Variant | When you need it | This week | Ships |
|---------|------------------|-----------|-------|
| Fixed parallel fan-out | Steps known at design time, symmetric | No | w04 |
| Orchestrator + one worker | Request branches into a variable number of independent parts | **Yes** | w05 |
| Deep orchestrator → specialists | Nested sub-teams, a second level of delegation | No | w15 (supervisor), w16 (hierarchical) |
| Async / durable background workers | Work outlives the request; orchestrator stays reachable | No | w19 (long-running background agents) |

## Open questions

- **Orchestrator-workers vs parallelization (w04).** Both fan out. No source measures the break-even point where runtime delegation beats a hard-coded parallel fan-out.
- **Step Functions vs Durable Functions for agent workers.** Both ship durable replay; no primary comparison exists.
- **Does the orchestrator's context become the ceiling?** Published case studies describe an orchestrator holding the plan and results, but none quantifies how its context scales with worker count.
- **Minimum eval set for a variable-width fan-out.** VMAO answers with an orchestration-level verifier, but the minimum set is unresolved.

## Reference

- Topic ladder: [content/topics/](../../content/topics/README.md)
- Acme stage: [07-running-use-case.md](../../docs/roadmap/07-running-use-case.md)
