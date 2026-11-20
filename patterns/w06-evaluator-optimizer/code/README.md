# w06 evaluator-optimizer

One call drafts, a second call grades the draft against named criteria, and
the generator rewrites from the critique. The loop ends on the verdict or a
hard cap.

```bash
# with uv (on the laptop)
uv sync --extra dev && uv run pytest

# without uv (bundled interpreter)
python3 -m pytest -q
```

No API keys are needed — the sample uses a deterministic mock LLM
(`core/llm.py`). The mock's first draft is *wrong on purpose* (a 90-day
return window), so the loop has something to fix.

## Layout

- `core/contracts.py` — `PolicyRule`, `Violation`, `Verdict`, `Attempt`, `Run`
- `core/policy.py` — the policy store: criteria as data, plus the
  deterministic checker and the verdict parser
- `core/pattern.py` — `generate` → `evaluate` → `revise`, capped by
  `DEFAULT_MAX_REWRITES = 1`
- `core/llm.py` — LLM protocol + `MockLLM` (draft / critique / rewrite)
- `aws/`, `azure/` — deployment stubs, including where the loop cap lives

## Design rules the sample follows

1. **The critic reads a tool, not the draft.** `PolicyStore.evidence()`
   supplies the policy rows; the critique call is given them. Delete the
   store and the critic cannot see the violation — there is a test for that.
2. **Cap the loop before you run it.** `max_rewrites` is a parameter, not a
   prompt instruction. `max_rewrites=0` reproduces the single-pass baseline.
3. **Every attempt is scored.** `on_verdict` fires for the draft and for each
   rewrite, so the score is emitted even when the rewrite saves the reply.
4. **Fail back to the deterministic check.** An unparseable verdict falls back
   to `PolicyStore.check` instead of shipping unchecked or blocking the reply.
