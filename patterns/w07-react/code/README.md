# w07 react

A bounded ReAct loop: the agent reasons, decides whether it needs the order
lookup, reads the observation, and either takes another step or answers. This
is the first week where control flow leaves the code — so the sample shows the
part you own: the tool allowlist, the argument check, and the stop rule.

```bash
# with uv (on the laptop)
uv sync --extra dev && uv run pytest

# without uv (bundled interpreter)
python3 -m pytest -q
```

No API keys are needed — the sample uses a deterministic mock LLM
(`core/llm.py`).

## Layout

- `core/contracts.py` — `ToolSpec`, `ToolCall`, `ToolResult`, `Message`,
  `Step`, `Trajectory` (the trace shape)
- `core/tools.py` — the registry, the `get_order_status` tool, and `check`:
  the allowlist + schema check that runs *before* every call
- `core/pattern.py` — `run_react`: reason → act → observe, capped by
  `DEFAULT_MAX_STEPS`, `DEFAULT_TOKEN_BUDGET` and `DEFAULT_WALL_CLOCK_MS`
- `core/llm.py` — LLM protocol + `MockLLM` (answers when the facts are in the
  request, calls the tool when they are not)
- `aws/`, `azure/` — deployment stubs (runtime, model contract, gate, stop rule)

## Design rules the sample follows

1. **The provider's tool contract, not parsed prose.** A step carries a typed
   `ToolCall`; the loop returns a typed `ToolResult`. Nothing regexes
   "Thought / Action / Observation" out of the model's text.
2. **Check the proposed call before execution.** `ToolRegistry.check` allowlists
   the tool (and refuses write scope) and validates arguments against the tool
   schema. A failed check becomes the observation, so the model can correct.
3. **Own the stop rule.** `max_steps`, `token_budget` and `wall_clock_ms` are
   parameters. `max_steps=0` reproduces "answer without acting".
4. **Record the trajectory.** `Trajectory.as_trace()` keeps the reason, the
   call and the observation per step — a non-deterministic run you can still
   explain.
5. **The agent decides whether to act.** `MockLLM` answers in one call when the
   request already carries the order facts, and calls the tool when it does
   not; a request with facts present is the case that makes the loop worth its
   cost over a fixed chain.
