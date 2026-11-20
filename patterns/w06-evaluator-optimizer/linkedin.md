# LinkedIn — w06 evaluator-optimizer

## Post A — Pattern

Your support agent ships the first draft it writes.

Every pattern so far makes a fixed number of model calls and returns whatever the last one says. Nothing asks whether the reply matches the policy it was handed.

Evaluator-optimizer adds the missing step:

- A critic call grades the draft against the policy store — it reads the policy row, it does not re-read the draft for confidence.
- The cap lives in code (`MAX_REWRITES = 1`), not in a prompt. A cap the model can talk itself past is not a cap.
- Pass: two model calls, ship the draft. Fail: one rewrite, ship the rewrite.
- Every verdict is emitted as an evaluation score beside the trace, so a saved draft is still a recorded near-miss.
- The critic gets read-only policy access and no write scope.

Diagram: request + context → generator → critic → policy store → verdict → pass: ship / fail: one bounded rewrite → ship.

Full write-up in the first comment.

## Post B — Opinion

Most support flows do not need a rewrite loop — and adding a judge introduces a new failure surface.

You can build the same shape on both clouds. Step Functions holds the loop cap as a state-machine constant; Durable Functions checkpoints the verdict and the iteration count, so a restart resumes at the same decision instead of re-critiquing. In both cases the policy read is a separate call from the generation call.

The judge is the part people under-rate. LLM-as-judge carries position, verbosity and self-enhancement biases. A 2026 study of fourteen System-1 judges found instruction injection reverses 17–49% of correct verdicts for nine of them — and in a support flow the draft contains customer text, so the critic inherits the prompt-injection problem a week early.

And nobody has defined what the online eval hook should do when the score is low: sample harder, alert, block, or retrain the prompt. The telemetry exists; the playbook does not.

Measure the single-pass baseline before you stand up a critic.

What does your eval hook actually do on a low score?

/blog/w06-evaluator-optimizer/

## Comment starters

1. "Where do you draw the line between iterative refinement and unnecessary complexity?"
2. "How do you monitor a judge for drift, or for injection through the draft it grades?"
3. "Should a low eval score block the reply, or only alert? What has worked for you?"
