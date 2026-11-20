# Cloud mapping — Evaluator-optimizer

## Cloud-agnostic core

The pattern has five moving parts, and only one of them is a model:

- **Generator** — produces a draft reply from the context the earlier patterns already fetched.
- **Criteria** — the named rules the draft is graded against. For Acme: a return window that matches the policy row, a warranty period that matches the policy row, and no refund offered on an opened item without manager review.
- **Critic (evaluator)** — reads the draft *and* the policy rows, then returns a structured verdict: pass, or a list of specific violations. The policy read is a tool call, not a re-read of the draft (CRITIC).
- **Optimizer (rewrite)** — the generator applies the cited violations and returns a second draft.
- **Loop control** — a hard iteration cap plus a quality threshold, both set before the first call. For w06 the cap is one rewrite.

The portability question is where the *verdict* goes. Every cloud now ships an evaluation surface that can hold a score next to a trace (CloudWatch Omni on AWS, Foundry evaluations with Application Insights on Azure). The verdict contract — pass/fail plus violation codes plus a 0–1 score — is the portable part. The pipeline that stores and alerts on it is not.

One thing the loop should not own: the stop decision. Keep the cap and the threshold in your code, not in the prompt. A model-driven stop rule is a second thing that can be wrong.

## AWS

| Component | Service | Notes |
|-----------|---------|-------|
| Model (generator + critic) | Amazon Bedrock | Two calls: draft, then critique. A cheaper model is admissible for the critic if its bias is measured |
| Critic's external signal | Lambda + DynamoDB policy store (or Bedrock Knowledge Bases) | The critic reads the policy row; it does not grade from memory |
| Loop control | AWS Step Functions | A bounded `Map`/retry around draft → critique → rewrite; the cap is a state-machine constant, not a prompt |
| Agent runtime | Amazon Bedrock AgentCore | Hosts the generator; the critique can run as a separate invoke |
| Verdict telemetry | CloudWatch Omni (agent traces + evaluation scores) | The same verdict that gates the reply is emitted as a score beside the trace |
| Guardrail backstop | Amazon Bedrock Guardrails | Applied after the loop; it filters output, it does not grade policy compliance |
| Identity | IAM roles | The critic gets read-only policy access and no write scope |

### AWS diagram notes

A channel invokes the AgentCore-hosted generator through a Step Functions state machine. The state machine calls Bedrock for the draft, then calls the critic path: the critic Lambda reads the policy row from DynamoDB and passes draft plus evidence to a second Bedrock invoke. The verdict returns as structured JSON. On `pass`, the draft ships. On `fail`, the state machine runs one rewrite and re-critiques; the cap is a constant in the state machine, so a second failure ships the rewrite with a logged violation rather than looping. Each verdict is written to CloudWatch Omni as an evaluation score next to the trace.

## Azure

| Component | Service | Notes |
|-----------|---------|-------|
| Model (generator + critic) | Microsoft Foundry models (Azure OpenAI) | Same two-call shape; separate deployments per role |
| Critic's external signal | Azure Functions + Cosmos DB policy store (or Azure AI Search) | Read-only lookup of the policy row |
| Loop control | Durable Functions | A deterministic orchestrator with a bounded `for` over iterations; replay-safe |
| Agent runtime | Microsoft Foundry Agent Service | Hosts the generator agent; the critic is a second agent or a plain invoke |
| Verdict telemetry | Application Insights (custom events / metrics) | Emit the verdict as a custom event on the same operation ID as the trace |
| Guardrail backstop | Azure AI Content Safety | Output filtering, not policy grading |
| Identity | Microsoft Entra ID managed identity | Scoped read on the policy store; no write role |

### Azure diagram notes

A Durable Functions orchestrator owns the loop: draft (Foundry model call) → critic (activity function reads the policy row, then a second model call) → branch. Because the orchestrator is deterministic and replays its history, the verdict and the iteration count are checkpointed: a host restart resumes at the same decision instead of restarting the loop. Verdicts are emitted as custom events to Application Insights and correlated by operation ID.

## Comparison

| Dimension | AWS | Azure |
|-----------|-----|-------|
| Managed agent runtime | Bedrock AgentCore | Foundry Agent Service |
| Bounded loop | Step Functions | Durable Functions |
| Verdict telemetry | CloudWatch Omni (traces + evaluation scores) | Application Insights custom events/metrics |
| Policy read for the critic | DynamoDB / Knowledge Bases via Lambda | Cosmos DB / AI Search via Functions |
| Typical lock-in | State-machine DSL, Omni trace/eval schema | Durable orchestrator API, App Insights schema |

> **Open question (from ADR/brief):** no source defines what an online eval hook does on a low score — sampling rate, alert threshold, and the action (block, escalate, retrain the prompt). Both clouds can carry the score; neither vendor's guidance says what to do with it. Do not state otherwise.

## Indicative cost (1,000 runs)

Assumptions: a small model on both calls; mean draft ~600 tokens in, ~250 out; critique ~900 in (draft + policy rows), ~120 out; one rewrite on the fraction of drafts that fail. Cost is model tokens, not compute — the Lambda/Function and state-machine hops are negligible beside them.

| Cloud | Est. USD (order of magnitude) |
|-------|-------------------------------|
| AWS | ~single-digit dollars per 1,000 runs; ≈2× the single-pass call count when the critic passes, ≈3× when it fails |
| Azure | ~single-digit dollars per 1,000 runs; same call shape, so the same multiple |

The multiplier is the number that matters, and it is the one the ADR cannot yet justify: **2 calls on a pass, 3 on a fail, versus 1 for w01**. By call count that is 2–3×; by tokens it is higher still, because the critique prompt carries the draft *plus* the policy rows while the draft call carries the task *plus* the retrieved context. The differentiator is not the price per token — it is the share of drafts that fail the criteria. Measure that share on the single-pass baseline before you budget the loop.

## Portability notes

- The verdict schema (pass, violation codes, score) is the portable contract. Keep it a plain JSON document so it can be written to either telemetry surface, or to neither.
- The loop cap belongs in your code. Step Functions and Durable Functions both give you a bounded, replayable loop; a `while` in application code gives you the same thing with less lock-in if the reply is short-lived.
- Criteria should be data, not prompt text: a policy row with an explicit value (`return_window_days: 30`) can be checked; "follow the returns policy" cannot.
- The critic is a second model call and therefore a second data-egress path for customer text. Review it under the same rules as the generator, and keep it read-only.
- **Verify docs** before quoting a per-service price or a renamed service; vendor pricing and evaluation surfaces change faster than this table.
