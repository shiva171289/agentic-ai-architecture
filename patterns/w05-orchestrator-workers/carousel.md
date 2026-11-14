# LinkedIn carousel — w05 orchestrator-workers

**Slide 1 — The fixed chain has a blind spot**
- A fixed pipeline runs every step for every request.
- Multi-part requests ("where is my order, and what is the return window?") over- or under-fetch.
- The shape of the work is decided at design time — and it is wrong for some requests.

**Slide 2 — Orchestrator decides WHAT; worker does HOW**
- Orchestrator reads the request and emits a short plan: which parts to delegate.
- Each worker runs one bounded retrieval or tool call and returns a structured result.
- The orchestrator merges results, then answers.

**Slide 3 — The difference from parallelization (w04)**
- w04 fans out a **fixed** set of calls decided in code.
- w05 lets the orchestrator choose **how many** workers to spawn, and with what instructions.
- Fan-out width is a runtime decision — not a design-time constant.

**Slide 4 — Keep the deterministic spine, put the model on the edges**
- Ordered, must-run steps go in a workflow engine (Step Functions / Durable Functions).
- Only the variable steps are model-driven.
- The plan is a trace, not hidden control flow — inspect it.

**Slide 5 — The new failure mode**
- A worker can return plausible-but-wrong output.
- The merge step cannot tell it from a correct result, so one bad worker poisons the answer.
- Mitigation: structured worker output + an orchestration-level verifier.

**Slide 6 — Cap it, or it caps you**
- Every worker is another model call and a new latency hop.
- Cap the fan-out width and the per-request budget.
- Measure the merge before celebrating the parallelism.

**Slide 7 — When NOT to use it**
- A single augmented call with retrieval usually meets the bar.
- If the steps are known and fixed, use a workflow engine — not a model-driven orchestrator.
- Add a worker only when the task genuinely branches into parts that run independently and merge.
