---
title: "Evaluator-optimizer: grade the draft before the customer sees it"
description: "One call drafts, a second call grades the draft against the policy store, and the generator rewrites once. After that, the cap decides."
pubDate: 2026-12-05
patternWeek: w06
level: Foundation
acmeStage: w06
spineLayers: "3"
---

Every pattern so far makes a fixed number of model calls and ships whatever the last one returns. This week adds the step that was missing: a second call whose only job is to grade the draft against a named criterion, and a generator that rewrites from that critique.

## Prerequisites

[w01 augmented LLM](/blog/w01-augmented-llm/) · [w02 prompt chaining](/blog/w02-prompt-chaining/) · [w03 routing](/blog/w03-routing/) · [w04 parallelization](/blog/w04-parallelization/) · [w05 orchestrator-workers](/blog/w05-orchestrator-workers/).

## Context

The w05 support flow assembles context, merges worker results, and calls the answer chain once. Whatever comes back ships. That single pass has no step that asks "does this reply state a return window that matches the policy row?" If the model misreads the policy it was handed, nothing catches it before the customer reads it.

This is **Layer 3** — evals and guardrails — arriving inside the request path rather than in a test suite. The pattern is evaluator-optimizer: one call produces a draft, a second call grades it against criteria you name, and the generator rewrites from the feedback. The loop ends when the criteria pass or a stop rule fires.

Anthropic states the fit condition plainly: it applies "when we have clear evaluation criteria, and when iterative refinement provides measurable value". Both halves are preconditions, not defaults. If the criteria are vague, or nobody measured whether refinement helps, the pattern is an unverified cost.

## Pattern

Three roles, two of which are model calls:

- The **generator** drafts the reply from context the earlier patterns already fetched.
- The **critic** receives the draft and the relevant policy rows, and returns a structured verdict: pass, or a list of specific violations.
- The **optimizer** is the generator again, rewriting only what the critique cited.

The difference from prompt chaining (w02) is where the length of the work is decided. A chain has a fixed order and a fixed number of steps, known before the request runs. Here the number of generate → critique → rewrite cycles is a runtime decision made by the verdict; only the cap is fixed.

Three research anchors shape the design:

- **Self-Refine** (arXiv 2303.17651) shows one model can act as generator, critic and rewriter with no training, up to four iterations.
- **Reflexion** (arXiv 2303.11366) splits the roles into Actor, Evaluator and Self-Reflection. Its ablation matters more than its headline: the gains come from a feedback signal grounded in the environment, not from the model re-reading its own output.
- **CRITIC** (arXiv 2305.11738) is the strongest statement of the same point. Tool interaction "plays a critical role", while the model's own critiques "contribute marginally".

So the critic must be able to check something outside the draft: a policy row with `return_window_days: 30`, an order lookup, a schema. A critic that grades "does this sound policy-compliant" is a second opinion from the same witness.

The cap belongs in code, not in a prompt. In the sample it is `MAX_REWRITES = 1`, a constructor argument; on both clouds it is a state-machine or orchestrator constant. A cap the model can talk itself past is not a cap.

And the judge is a new failure surface, not a safety net. LLM-as-a-judge (arXiv 2306.05685) documents position, verbosity and self-enhancement biases. A 2026 study of fourteen non-generative System-1 judges (arXiv 2611.00505) finds instruction injection flips 17–49% of correct verdicts for nine of them. In a support flow the draft contains customer-supplied text, so the critic inherits the prompt-injection problem one step earlier than w28 addresses it.

## Scenario ladder

| Variant | Need | This week | Ships |
|---------|------|-----------|-------|
| Single-pass draft | Criteria unclear, or first attempts already clear the bar | No — this is the baseline to measure | w01 |
| Draft → critic → one rewrite | Criteria are explicit and one named failure is likely | **Yes** | w06 |
| Multi-iteration loop with a plateau rule | Refinement keeps paying past one pass | No | w33 |
| Several specialised critics | Independent criteria graded separately | No | w32 |
| Deterministic grader instead of a model | A linter, schema or test can decide | No | w37 |
| Async critique | Latency forbids an inline critic | No | w33 |

Only the middle row ships this week. The rest need evidence that w06 does not yet have: a failure-rate baseline, a plateau rule, or a latency budget that rules the inline critic out.

## When not to use

- **First-attempt quality already meets requirements.** Anthropic's own advice is to find the simplest solution. Run the single-pass draft for two weeks and count how often a policy rule is actually missed before standing up a critic.
- **The criteria are subjective.** "Make it friendlier" is not a criterion. "Does the reply state a return window that matches the policy row" is.
- **The critic can only read the draft.** Without an external signal, the loop collapses into self-agreement. The sample ships a test that deletes the policy store and watches the critic pass the bad draft.
- **A deterministic check would do.** If a linter, a schema or a unit test can grade the output, use that. A model critic is the expensive way to approximate a test.
- **The latency budget is hard.** An inline critic adds at least one round trip to every reply; a failing draft adds two.
- **Nobody will read the verdicts.** If the score is emitted and never sampled or alerted on, the loop is a cost with no feedback. What an online eval hook should *do* on a low score — sampling rate, threshold, block or escalate — is still an open question; no source in this week's corpus defines it.

## Apply it to Acme

The w06 increment is one file, `projects/acme-support/core/critic.py`, on top of the w05 orchestrator:

- The draft still comes from the w05 path (`default_orchestrator`), so the critic grades the real reply, not a toy string.
- `critique(llm, draft, policies)` hands the critic the policy rows the draft touches. `check_policy(draft, policies)` is the deterministic checker behind it, and the fallback when a verdict cannot be parsed.
- `answer_with_critic(...)` runs draft → critique → at most one `rewrite(...)`, then returns the reply plus every verdict.
- Policy facts are now data in `policies.json` — `return_window_days: 30`, `opened_requires_review: true`, `warranty_months: 12` — because "follow the returns policy" cannot be checked and `30` can.
- Each attempt emits `Verdict.as_telemetry()`: `passed`, `score`, and the violation rule ids.

The demo shows the loop doing its job. A draft that says "within 90 days… even if you have opened it" scores 0.5 with two cited violations. One rewrite fixes both: 30 days, and opened items need manager review. The second verdict passes at 1.0. A compliant draft skips the rewrite entirely, which is the case that decides whether the pattern is worth its cost.

```bash
cd projects/acme-support && uv sync --extra dev && uv run pytest
```

Twelve new tests cover the checks, the cap, the grounded and blind critic, the fallback, and the telemetry. The suite runs 28 tests in mock mode with no API keys.

The increment is tagged `stage-w06`; freeze a copy with `git fetch --tags && git checkout stage-w06`.

## Architect's notebook

| Field | Notes |
|-------|-------|
| Decision | One critic pass grounded in the policy store, one bounded rewrite, verdict emitted per attempt |
| Rejected | Open-ended loop, and a critic that grades the draft without the policy row |
| Top failure mode | A judge that agrees with the draft (or is steered by text inside it), so a bad reply passes |
| Cost hint | Two model calls on a pass, three on a fail, versus one for w01 — order of magnitude 2–3× the single pass, and higher in tokens because the critique prompt carries the draft plus the policy rows |
| NFRs | Latency (one or two extra round trips on the critical path), security (critic gets read-only policy access, no write scope), audit (every verdict stored with its violations) |

## Reference implementation

- **Pattern sample:** [`patterns/w06-evaluator-optimizer/code/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/patterns/w06-evaluator-optimizer/code)
- **Acme spine:** [`projects/acme-support/`](https://github.com/shiva171289/agentic-ai-architecture/tree/main/projects/acme-support)

Tests run without cloud API keys. The mock's first draft is wrong on purpose, so the loop has something to fix.

## AWS mapping

Typical services (verify current names):

- **Amazon Bedrock** for both calls, with **AgentCore** hosting the generator.
- **AWS Step Functions** owns the bounded loop; the cap is a state-machine constant, not a prompt instruction.
- A critic **Lambda** reads the policy row from **DynamoDB**, then a second Bedrock invoke returns the JSON verdict.
- **CloudWatch Omni** holds the verdict as an evaluation score beside the agent trace.
- **Amazon Bedrock Guardrails** filters the final text. It is a backstop after the loop, not a substitute for grading policy compliance.

The critic gets an IAM role with read-only policy access. A judge with write permissions is a new attack surface for no gain.

## Azure mapping

Typical services (verify current names):

- **Microsoft Foundry models** (Azure OpenAI) for both calls, with **Foundry Agent Service** hosting the generator agent.
- A **Durable Functions** orchestrator owns the loop. The verdict and the iteration count are part of the orchestrator history, so a restart resumes at the same decision instead of re-running the critique.
- An **Azure Functions** activity reads the policy row from **Cosmos DB** or **Azure AI Search**; a second Foundry model call returns the verdict.
- **Application Insights** receives the verdict as a custom event or metric, correlated by operation ID.
- **Azure AI Content Safety** filters the output after the loop.

Identity is an Entra ID managed identity with scoped read on the policy store. Same rule as AWS: the critic reads, it does not write.

## Production checklist

Before this pattern goes near a customer reply, walk the [Production Readiness Checklist](/production-readiness-checklist/) — the parts that matter here are the eval baseline, the judge's measured bias, verdict retention, and the cost cap on the loop. And decide the inline-versus-async question explicitly, because it is the one the sources leave open.

## Further reading

- Anthropic — Building effective agents: https://www.anthropic.com/research/building-effective-agents
- Self-Refine: Iterative Refinement with Self-Feedback: https://arxiv.org/abs/2303.17651
- Reflexion: Language Agents with Verbal Reinforcement Learning: https://arxiv.org/abs/2303.11366
- CRITIC: LLMs Can Self-Correct with Tool-Interactive Critiquing: https://arxiv.org/abs/2305.11738
- Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena: https://arxiv.org/abs/2306.05685

## Disclaimer

Views and examples are my own, for learning purposes, and do not represent my employer.
