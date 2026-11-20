# LinkedIn carousel — w06 evaluator-optimizer

**Slide 1 — A single pass ships an unchecked draft**
- Every pattern so far fixes the number of model calls and returns the last one.
- Nothing checks the reply against the policy row before the customer sees it.
- Misread policy — a return window, a refund rule — ships silently.

**Slide 2 — Three roles: generator, critic, optimizer**
- Generator drafts the reply from the context the earlier patterns fetched.
- Critic grades the draft against named criteria and returns a structured verdict.
- Optimizer is the generator again, rewriting only what the critique cited.

**Slide 3 — Runtime loop, not a fixed chain**
- w02 prompt chaining has a fixed number of steps, known before the request runs.
- Here the verdict decides whether a rewrite happens; only the cap is fixed.

**Slide 4 — The critic must read a tool, not the draft**
- CRITIC: tool interaction plays a critical role; the model's own critiques contribute marginally.
- A critic that re-reads the draft is a second opinion from the same witness.
- Evidence in, verdict out: pass, or a list of specific violations.

**Slide 5 — Cap it in code**
- One rewrite for this pattern; two generator attempts maximum.
- The cap is a code constant, a Step Functions constant, or a Durable Functions loop bound — never a prompt instruction.
- Pass: two model calls. Fail: three. w01 was one.

**Slide 6 — The judge is a new failure surface**
- LLM-as-judge carries position, verbosity and self-enhancement biases.
- Instruction injection reverses 17–49% of correct verdicts for nine of fourteen System-1 judges studied.
- Keep the critic blind to attacker-controlled formatting; prefer a calibrated, non-generative judge for closed verdicts.

**Slide 7 — When NOT to use it**
- First-attempt quality already meets the bar, and the loop is unmeasured.
- Criteria are subjective, or only the draft is available to grade.
- A linter, schema or unit test can decide — use that instead.
- Open gap: no source defines the sampling rate, threshold, or action for a low online eval score.
