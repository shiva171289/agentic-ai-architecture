# Brief — w06 evaluator-optimizer

**Topic:** Evaluator-optimizer (+ reflection) — one LLM generates a draft, a second call evaluates it against explicit criteria, and the generator rewrites the draft from the critique, looping until the criteria pass or a stop rule fires
**Date researched:** 2026-11-20
**Corpus:** `content/source-corpus/latest.md` (483 entries, window 7 days, generated 2026-11-20)
**Acme stage (W06):** Draft reply → policy critic → one rewrite (includes reflection)
**Mapping focus:** Online eval hooks

## Summary

Evaluator-optimizer is the first pattern in the ladder that improves an answer by *critique* instead of by more context: one call produces a draft, a second call grades it against criteria you name, and the generator rewrites from that feedback. Anthropic states the fit condition plainly — it works when "evaluation criteria" are clear and "iterative refinement provides measurable value". The research lineage is mature: Self-Refine (2303.17651) showed a single model can act as generator, feedback provider, and refiner with no training; Reflexion (2303.11366) formalized the three-role split (Actor, Evaluator, Self-Reflection) and the key finding that the critic only helps when it gets an *external* signal, not when it reads its own draft. That last point is the whole design risk, and this week's corpus says the ecosystem has started to answer it in production: evaluators are being decoupled from the request path (CloudWatch Omni collects agent traces and *evaluation scores* as telemetry), split from generative judges (DeepEval 4.2.2 routes closed-ended verdicts to a non-generative, calibrated decision model), and hardened against their own biases (System-1 judges are more repeatable but still flip 17–49% of verdicts under instruction injection). For Acme this is the week the support reply stops being a single pass: a draft is checked against the policy store by a critic, then rewritten once. The honest caution is in the sources too — every guidance set says the loop burns tokens and latency, and none shows it is worth it without a measured baseline first.

## Sources

Corpus entries (vendor blogs, window 2026-11-13 → 2026-11-20):

| Title | URL | Date accessed |
|-------|-----|---------------|
| AWS — How the Managed Services Model on AWS Grows Up for Agentic AI | https://aws.amazon.com/blogs/apn/how-the-managed-services-model-on-aws-grows-up-for-agentic-ai/ | 2026-11-20 |
| AWS — How Airbnb uses cost per task to operate coding agents on Amazon Bedrock | https://aws.amazon.com/blogs/machine-learning/how-airbnb-uses-cost-per-task-to-operate-coding-agents-on-amazon-bedrock/ | 2026-11-20 |
| AWS — Best practices for deploying Amazon CloudWatch Omni at enterprise scale | https://aws.amazon.com/blogs/mt/best-practices-for-deploying-amazon-cloudwatch-omni-at-enterprise-scale/ | 2026-11-20 |
| AWS — Runtime governance for AI agents with Noma Security and AgentCore Gateway | https://aws.amazon.com/blogs/apn/runtime-governance-for-ai-agents-with-noma-security-and-agentcore-gateway/ | 2026-11-20 |
| AWS — JA Canada launches generative AI with Qalius and Amazon Bedrock | https://aws.amazon.com/blogs/apn/ja-canada-launches-generative-ai-with-qalius-and-amazon-bedrock/ | 2026-11-20 |
| AWS — Introducing the Apache Spark Optimization Agent for Amazon EMR Serverless | https://aws.amazon.com/about-aws/whats-new/2026/11/apache-spark-optimization-agent/ | 2026-11-20 |
| Microsoft — What's new in Foundry Agent Service at Ignite 2026 | https://devblogs.microsoft.com/foundry/whats-new-in-foundry-agent-service-at-ignite-2026/ | 2026-11-20 |
| Google Cloud — Testing changes, fast: Introducing agentic assessments in Database Center | https://cloud.google.com/blog/products/databases/database-center-assessments-for-cloud-sql-for-postgresql/ | 2026-11-20 |
| OpenAI — Research acceleration: The jagged frontier | https://openai.com/index/research-acceleration-jagged-frontier | 2026-11-20 |
| OpenAI — Our first phase of embedded assessments | https://openai.com/index/our-first-phase-of-embedded-assessments | 2026-11-20 |
| Anthropic — An Update On Independent Evaluators | https://www.anthropic.com/news/an-update-on-independent-evaluators | 2026-11-20 |

Primary sources fetched this session (pattern definition, papers, OSS releases):

| Title | URL | Date accessed |
|-------|-----|---------------|
| Anthropic — Building effective agents (workflow: Evaluator-optimizer) | https://www.anthropic.com/research/building-effective-agents | 2026-11-20 |
| arXiv — Self-Refine: Iterative Refinement with Self-Feedback (2303.17651) | https://arxiv.org/abs/2303.17651 | 2026-11-20 |
| arXiv — Reflexion: Language Agents with Verbal Reinforcement Learning (2303.11366) | https://arxiv.org/abs/2303.11366 | 2026-11-20 |
| arXiv — Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (2306.05685) | https://arxiv.org/abs/2306.05685 | 2026-11-20 |
| arXiv — CRITIC: LLMs Can Self-Correct with Tool-Interactive Critiquing (2305.11738) | https://arxiv.org/abs/2305.11738 | 2026-11-20 |
| arXiv — To Jev or Not to Jev: When Can System-1 Decision Models Replace LLM Judges? (2611.00505) | https://arxiv.org/abs/2611.00505 | 2026-11-20 |
| GitHub — DeepEval releases (4.2.2: Jev System-1 judging) | https://github.com/confident-ai/deepeval/releases | 2026-11-20 |
| GitHub — promptfoo releases (0.126.0, 2026-11-18) | https://github.com/promptfoo/promptfoo/releases | 2026-11-20 |
| GitHub — Inspect AI releases (v0.3.291, 2026-11-17) | https://github.com/UKGovernmentBEIS/inspect_ai/releases | 2026-11-20 |

Corpus note: `content/source-corpus/latest.md` contains **no** entry that names the pattern "evaluator-optimizer", "self-refine", or "reflection" as a workflow. The canonical definition above comes from Anthropic's pattern guide, and the reflection mechanics come from the Self-Refine / Reflexion / CRITIC papers — both fetched this session, not from the corpus. The corpus supplies the *production* signal (evaluating output quality, traces and evaluation scores, calibrated judges): do not upgrade those entries into a statement that a vendor ships the loop pattern by name.

## Key concepts

- **The loop is generator → evaluator → optimize, and Anthropic frames the fit as a precondition, not a default.** "In the evaluator-optimizer workflow, one LLM call generates a response while another provides evaluation and feedback in a loop." It applies "when we have clear evaluation criteria, and when iterative refinement provides measurable value" — the two signs being that a human's articulated feedback demonstrably improves the output, and that the LLM can produce that feedback.
- **Evaluation and generation are different cognitive tasks, so split the roles.** The pattern's value is that the evaluator specializes on applying one consistent criterion while the generator specializes on producing content (Anthropic pattern guide). This is the difference from prompt chaining (w02): a chain is a fixed order of steps; the optimizer's number of iterations is decided at runtime by the verdict.
- **Self-Refine: one model can be generator, critic, and rewriter — no training.** Self-Refine (2303.17651) "does not require any supervised training data, additional training, or reinforcement learning"; it alternates FEEDBACK and REFINE on the same model, up to a maximum of four iterations, until "the desired output quality or task-specific criterion is reached".
- **Reflexion names the three roles and the external-signal requirement.** Reflexion (2303.11366) uses an **Actor** that generates, an **Evaluator** that scores, and a **Self-Reflection** model that writes verbal feedback stored in an episodic buffer for the next attempt — "reinforce language agents not by updating weights, but instead through linguistic feedback". The ablation matters more than the headline: gains come from a feedback signal grounded in the environment (unit-test pass/fail, task success), which the authors study explicitly across signal types.
- **A critic without a tool can reinforce its own errors; tool-grounded critique is what lifts quality.** CRITIC (2305.11738) has the model "interact with appropriate tools to evaluate certain aspects of the text, and then revise the output based on the feedback"; the paper reports that **tool-interaction plays a critical role** while "the model's own critiques contribute marginally". Design takeaway: the critic needs a verifier (policy store, tests, search), not just a re-read of the draft.
- **The judge itself is now an unreliable component to be measured.** LLM-as-a-judge (2306.05685) is the scalable evaluation primitive, but the paper documents position, verbosity, and self-enhancement biases and limited reasoning. The 2026 follow-up (2611.00505) evaluates 14 non-generative System-1 judges against four generative judges and finds them cheaper, faster, and often better calibrated — but also that **robustness to instructions injected into the judged response is a property of the individual model, reversing 17–49% of correct verdicts for nine of the fourteen**.
- **The evaluator is being pulled out of the request path in production.** CloudWatch Omni's enterprise guidance separates "agent developers observe agent traces and evaluation scores" from SRE latency and security reviews — i.e. evaluation scores are now a telemetry stream alongside traces. Airbnb (corpus) "runs evals on real engineering tasks" and warns that production spending can differ from eval results, which is the same online-vs-offline split at the cost layer.
- **A concrete generate→critique→recommend loop already ships in an unexpected place.** The Apache Spark Optimization Agent (corpus) takes a goal (cost or performance), reads job config, logs, and telemetry, and "returns specific configuration changes with the telemetry evidence and reasoning behind each suggestion"; when cost and performance trade off it "improves the metric you chose while keeping any regression of the other within defined limits". That regression bound is the design pattern a critic loop needs: optimize one criterion without silently degrading the others.
- **Verdicts are being split from generation.** DeepEval 4.2.2 introduces TypeSafe's Jev: "language tasks stay with your evaluation LLM; decision points go to Jev" — a non-generative model that "returns a typed decision with calibrated probabilities", replacing free-form JSON grading for closed-ended verdicts. Inspect AI (UK AISI) runs agent evals in sandboxes, and promptfoo (0.126.0, still MIT) remains the CI-side declarative gate.

## Contrarian angles

1. **Most tasks do not need the loop — measure the first draft before adding a critic.** Anthropic's own guidance is to find the simplest solution and add complexity only when needed; its pattern material says to avoid the loop when "first-attempt quality already meets requirements", when criteria are subjective, or when time and cost "outweigh quality improvements". At Acme, run the single augmented draft for two weeks and count how often a policy rule is actually missed before standing up a critic.
2. **A critic that only reads the draft is the weakest form of the pattern.** CRITIC's result — the model's own critiques contribute marginally, tool-interaction is decisive — means the evaluator must be able to *check* something outside the text: the policy store, the order lookup, a linter. A support critic that grades "does this sound policy-compliant" without reading the policy row is just a second opinion from the same witness, and Self-Refine's single-model design shows how easily it collapses into self-agreement.
3. **The judge is a new failure surface, not a safety net.** LLM-as-a-judge carries position, verbosity, and self-enhancement biases (2306.05685), and the 2026 System-1 study shows a note appended to the judged response can reverse up to half of a judge's correct verdicts. In a support flow where the "draft" contains customer-supplied text, the critic inherits the prompt-injection problem (w28) one step earlier. Use a critic that is blind to attacker-controlled formatting and, where possible, non-generative and calibrated.

## Open questions

- **What is the break-even?** Every source says measure that the loop beats a single call; none gives a threshold. There is no corpus or paper number for "N% of drafts fail criteria" that justifies the extra call and latency. Baseline first, configure second.
- **Fixed iteration cap or evaluator-decided stop?** Anthropic's example has the evaluator decide "whether further searches are warranted"; the white paper cites 2–4 cycles as typical; Self-Refine caps at four. Which stop rule is safer for a policy critic — a hard cap, a threshold, or the evaluator's own verdict (which can itself be wrong)?
- **Same model or a stronger/different critic?** Self-Refine uses one model for all three roles; enterprise guidance leans toward separating them. The corpus does not say what an Acme support critic should be, or whether a cheaper calibrated judge is good enough for policy compliance.
- **What does an "online eval hook" actually do on a low score?** CloudWatch Omni shows evaluation scores flowing next to traces, but no source defines the sampling rate, the alert threshold, or the action (block, escalate, retrain the prompt). This is the W06 mapping-focus gap.
- **Where does the critic run — inline or async?** Inline doubles latency and cost per reply; async means the customer sees the un-reviewed draft. The corpus supports both eval-as-telemetry and eval-for-gating but does not choose for a customer-facing reply.
- **How do you stop the loop from plateauing while still spending?** The stated "pro tip" is to set maximum iterations and a quality threshold before iterating, because the evaluator can keep finding minor issues while quality flatlines. No source gives a detection rule for "good enough" that is cheaper than another iteration.
