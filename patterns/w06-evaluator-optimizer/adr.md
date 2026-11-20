# ADR — Evaluator-optimizer

**Status:** accepted
**Week:** w06

## Context

The Acme support flow produces one reply per request. Retrieval runs, then one answer call runs (w01). Prompt chaining splits the answer by intent (w02). Routing picks a model (w03). Parallelization fetches context from several sources at once (w04). Orchestrator-workers decomposes a request into parts at runtime (w05). In every case the number of model calls is fixed at design time, and the reply is whatever the last call returns.

That last call is the whole problem. A single pass makes one attempt at the answer and ships it. It has no step that checks the draft against a named criterion before the customer sees it. When the model misses a policy rule — a return window stated wrongly, a refund offered outside the allowed period — nothing in the pipeline catches it.

Evaluator-optimizer is the first pattern in the ladder that improves an answer by *critique* instead of by more context. One call produces a draft, a second call grades it against criteria you name, and the generator rewrites the draft from that feedback. The loops stops when the criteria pass or a stop rule fires.

Constraints:

- Latency budget: the reply must stay near the existing p95 target. The critique and the rewrite are extra calls on the critical path.
- Cost budget: every iteration is at least two more model calls. The loop must not run when one pass already meets the bar.
- Evaluation: the pattern exists to improve quality, so it must itself be measured. A critic with no baseline is an unverified cost.
- Governance: the critic must be able to check something outside the draft text — the policy store, not just a re-read. Writes stay behind the existing approval gate.
- Trust boundary: the draft can contain customer-supplied text. The critic inherits the prompt-injection problem (w28) one step earlier.

## Decision

We use **evaluator-optimizer** for the Acme support reply. A generator call produces a draft, a critic call grades the draft against explicit policy criteria, and the generator performs one rewrite from the critique.

For w06 the increment is one critic pass and one rewrite — no open-ended loop:

- The **generator** produces the draft reply from the existing retrieved context and answer chain.
- The **critic** receives the draft and the policy criteria, and returns a structured verdict: pass, or a list of specific violations. It is grounded in the policy store, not in a re-read of the draft alone.
- The **rewrite** applies the critique. The reply that leaves the pipeline is the rewrite, or the original draft if the critic passed it.
- The loop cap is **one rewrite** (two generator attempts total). The evaluator's verdict decides whether the rewrite is needed, but the cap bounds the cost.

This is the difference from w02 (prompt chaining): a chain is a fixed order of steps, and its length is known before the request runs. Here the number of *generate→critique→rewrite* cycles is decided at runtime by the critic's verdict, and the cap is the only fixed part.

Design rules we adopt from the corpus:

- **Apply the pattern only under Anthropic's stated precondition.** The evaluator-optimizer workflow applies "when we have clear evaluation criteria, and when iterative refinement provides measurable value." Policy compliance is the clear criterion. Measurable value must be shown before the loop is treated as a default.
- **Ground the critic in a tool, not in its own reading.** CRITIC (2305.11738) reports that "tool-interaction plays a critical role" while "the model's own critiques contribute marginally." The critic must read the policy row or the order lookup, not just the draft.
- **Cap iterations and set a quality threshold before iterating.** The stated practice is to fix a maximum iteration count and a threshold up front, because an unconstrained critic keeps finding minor issues while quality flatlines. For w06 the cap is one rewrite.

## Alternatives considered

| Option | Pros | Cons |
|--------|------|------|
| Single augmented call (w01) | One call; simplest eval; lowest latency | Ships every draft unchecked; no policy gate before the customer |
| Fixed prompt chain with a validation step (w02) | Deterministic order; cheap | Validation is a fixed step, not a verdict; it cannot trigger a rewrite |
| Retrieval-only fix (fetch more policy rows into w01) | No extra model call | More context does not catch a draft that misreads the policy it was given |
| LLM-as-a-judge offline only (w05 eval set) | No production latency cost | Catches regressions after the fact, not the reply the customer is reading now |
| Evaluator-optimizer, capped at one rewrite (this ADR) | Checks and fixes the draft before it ships | Adds at least one critic call and usually one rewrite; the judge is a new failure surface |

## When NOT to use

- **First-attempt quality already meets requirements.** Anthropic's guidance is to find the simplest solution and add complexity only when needed. Run the single augmented draft and count how often a policy rule is actually missed before standing up a critic.
- **The evaluation criteria are subjective.** The pattern needs clear criteria. "Make it friendlier" is not one. "Does the reply state a return window that matches the policy row" is.
- **The critic can only read the draft.** A critic with no external signal is the weakest form of the pattern. Self-Refine's single-model design (2303.17651) shows how easily it collapses into self-agreement; a second re-read from the same witness is not verification.
- **Time or cost outweighs the quality gain.** The loop burns tokens and latency on every reply it runs, pass or fail. Nothing in the sources shows the trade is worth it without a measured baseline.
- **The task is a strict transformation with a deterministic check.** If a linter, a schema, or a unit test can grade the output, use that, not a model critic.

## Consequences

### Positive

- The reply is checked against a named criterion before the customer sees it, not only in offline evals.
- Generation and evaluation are separate calls, so each specializes: the generator on producing content, the critic on applying one consistent policy.
- The critique is inspectable. The verdict and the rewrite are trace entries, so a failed draft has a recorded reason.
- The critic is a natural place for an **online eval hook**: the same verdict that gates the reply can be emitted as a score alongside the trace (CloudWatch Omni) without a second call.

### Negative / risks

- Every reply pays at least one extra model call for the critique; a failing draft pays two.
- The critic is a new failure surface, not a safety net. A judge with position, verbosity, or self-enhancement bias (2306.05685) can pass a bad draft or fail a good one.
- The critic adds latency on the critical path. Inline critique doubles the reply time; async critique means the customer sees the unchecked draft.
- The rewrite is not guaranteed to fix the violation. The generator can rewrite from a correct critique and still miss the criterion.
- An unconstrained loop keeps finding minor issues while quality flatlines, spending tokens for no gain.

## Failure modes

- **Critic without an external signal.** The critic grades the draft against its own reading and reinforces the generator's error. Mitigation: ground the critic in the policy store, the order lookup, or a schema (CRITIC).
- **Judge manipulation by attacker-controlled text.** A note injected into the customer-supplied part of the draft can reverse a correct verdict; the 2026 System-1 study (2611.00505) finds instruction injection flips 17–49% of correct verdicts for nine of fourteen judges. Mitigation: keep the critic blind to attacker-controlled formatting; prefer a non-generative, calibrated judge for closed-ended verdicts (DeepEval 4.2.2 / Jev).
- **Loop plateau.** The critic keeps returning minor issues and the generator keeps rewriting while quality stops improving. Mitigation: cap iterations (one rewrite for w06) and set a quality threshold before iterating.
- **Rewrite regression.** The rewrite fixes the named violation but introduces a new one, or degrades an unrelated criterion. Mitigation: bound the rewrite to the cited violations; carry a regression limit, the way the Spark Optimization Agent keeps the untouched metric within defined limits.
- **Latency blow-out inline.** Critique plus rewrite pushes the reply past the p95 target. Mitigation: decide inline vs async per criterion; critique asynchronously where the reply can ship without the check.
- **Verdict log lost.** The critique is produced but not stored, so a bad reply cannot be explained after the fact. Mitigation: emit the verdict as telemetry beside the trace.

## Security notes

- The draft is untrusted input to the critic. Treat the customer-supplied portion as data, not instructions, to limit prompt injection across the boundary.
- The critic must not gain write permissions. It reads the policy store; writes stay behind the existing approval gate.
- The critic's verdict is a record, not just control flow. Log each version (draft, critique, rewrite) for audit and for offline replay.
- A judge is a shared dependency. If it is a hosted model, it is another data egress path for customer text; review it under the same rules as the generator.
- Prefer a judge whose bias the team has measured. An unmeasured critic is an unverified gate on customer-facing content.

## Cost / latency (order of magnitude)

- One generator call for the draft, one critic call, and one rewrite call on a failing draft — roughly two calls on a pass, three on a fail, versus one for w01.
- Latency is the sum of the calls when the loop runs inline; it grows with each iteration, unlike the concurrent fan-out of w04 or w05.
- Cost grows with the iteration count. Cap the iterations and set a per-request budget; the loop must not run open-ended.
- The break-even is unmeasured. No source gives a number for what fraction of drafts must fail criteria to justify the extra calls. Baseline the single-pass draft first.
- Offline eval sets and online verdicts share the same judge; reuse the critic's criteria as the offline rubric so the two do not drift.

## Decision summary

Adopt evaluator-optimizer for the Acme support reply, capped at one critic pass and one rewrite. Ground the critic in the policy store, not in a re-read of the draft. Emit the verdict as an online eval score beside the trace. Ship the rewrite when the critic cites a violation, the original draft when it passes. Measure the single-pass baseline before adding the loop, and do not run the loop open-ended.

## Open questions

- **What is the break-even?** No source gives a fraction-of-drafts-failing threshold that justifies the extra calls and latency. This is the W06 mapping-focus gap: what the online eval hook does on a low score is undefined.
- **What does an online eval hook do on a low score?** CloudWatch Omni shows evaluation scores flowing next to traces, but no source defines the sampling rate, the alert threshold, or the action (block, escalate, retrain the prompt).
- **Same model or a separate critic?** Self-Refine uses one model for all three roles; enterprise guidance leans toward separating them. No source says whether a cheaper calibrated judge is good enough for policy compliance.
- **Fixed cap or evaluator-decided stop?** Self-Refine caps at four iterations; the white paper cites 2–4 cycles; Anthropic's example lets the evaluator decide. A hard cap is cheaper and more predictable, but the evaluator's verdict is the signal the loop exists for.
- **Inline or async critique?** Inline doubles latency and cost per reply; async ships the un-reviewed draft. The corpus supports both eval-as-telemetry and eval-for-gating but does not choose for a customer-facing reply.
- **How do you detect "good enough" cheaper than another iteration?** No source gives a plateau-detection rule that costs less than the iteration it would skip.
