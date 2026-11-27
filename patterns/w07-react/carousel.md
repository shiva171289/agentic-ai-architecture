# LinkedIn carousel — w07 react

**Slide 1 — The limits of static workflows**
- Past patterns (w01–w06) lock the path before execution: chain, router, worker list, critic criteria.
- The model chooses what to say, not what to do next.
- Fixed paths break when the next step depends on runtime data.

**Slide 2 — When static paths fail**
- A request for order status needs `get_order_status` — unless the order number and delivery date are already present.
- No prior pattern skips steps based on live context.
- Hardcoding all branches leads to combinatorial explosion.

**Slide 3 — What ReAct really is**
- Model generates a reasoning trace, selects a tool, reads the result, and decides the next step — looping until done.
- "Dynamically direct their own processes and tool usage" (Anthropic).
- Reference: ReAct (arXiv 2210.03629).

**Slide 4 — Your three responsibilities**
- Curate a small, read-only tool set.
- Enforce pre-execution checks: allowlist, argument schema, intent validation.
- Define the stop rule: max steps, token budget, wall-clock limit — ReAct has no built-in terminator.

**Slide 5 — Use typed contracts, not parsers**
- Use the provider's `tool_use` block — executed by your code, returned as typed `tool_result`.
- Avoid hand-rolled "Thought / Action / Observation" parsers — they degrade silently.
- Typed execution ensures fidelity and debuggability.

**Slide 6 — New risks in the loop**
- Prompt injection can steer tool calls — customer text becomes action.
- Google's inline semantic policy check reduces attack success from 48.7% to 0.9%.
- Keep write-capable tools out of the loop.

**Slide 7 — When not to use ReAct**
- Use fixed chains (w02) for known, short paths.
- Use routers (w03) for bounded branching.
- ReAct earns its keep only when the next step depends on tool output and the path length is unknown.
- Open question: no source specifies a safe step limit for customer-facing loops.
