# w02 — prompt chaining sample

```bash
uv sync --extra dev && uv run pytest
uv run python -c "from core.llm import MockLLM; from core.pattern import run_chain; print(run_chain(MockLLM(), 'refund policy').text)"
```
