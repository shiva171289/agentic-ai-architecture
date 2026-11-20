# Scenario ladder — evaluator-optimizer

List variants for this pattern family. Implement **only** this week's row; link to future weeks for the rest.

| Variant | When you need it | This week | Ships |
|---------|------------------|-----------|-------|
| Single-pass draft (baseline) | Criteria are unclear, or first-attempt quality already meets the bar | No — the thing to measure against | w01 |
| Draft → critic → one bounded rewrite | Criteria are explicit and one named failure is likely | **Yes** | w06 |
| Multi-iteration loop with a plateau rule | Refinement keeps paying off past one pass | No | w33 (online evals) |
| Several specialised critics | Independent criteria (policy, tone, safety) graded separately | No | w32 (offline evals) |
| Deterministic grader instead of a model | A linter, schema, or unit test can decide pass/fail | No | w37 (agent CI/CD) |
| Async critique (ship first, grade after) | Latency budget forbids an inline critic | No | w33 (online evals) |

## Open questions

- **What is the break-even?** No source gives the failure rate at which the extra critic call pays for itself. Measure the single-pass baseline first.
- **Fixed cap or evaluator-decided stop?** Self-Refine caps at four; the white paper cites 2–4 cycles; Anthropic's example lets the evaluator decide. A hard cap is cheaper and predictable; the verdict is the signal the loop exists for.
- **Same model or a separate critic?** Self-Refine uses one model for all three roles; enterprise guidance leans toward separating them. Whether a cheaper calibrated judge is good enough for policy compliance is unresolved.
- **Inline or async?** Inline doubles latency and cost; async ships the unchecked draft. The corpus supports eval-as-telemetry and eval-for-gating but does not choose for a customer-facing reply.
- **What does an online eval hook do on a low score?** No source defines the sampling rate, the alert threshold, or the action (block, escalate, retrain the prompt). This is the W06 mapping-focus gap.

## Reference

- Topic ladder: [content/topics/](../../content/topics/README.md)
- Acme stage: [07-running-use-case.md](../../docs/roadmap/07-running-use-case.md)
