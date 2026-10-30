# Code template layout

```text
code/
  pyproject.toml
  README.md
  core/
    __init__.py
    llm.py          # LLM protocol + MockLLM
    pattern.py      # pattern logic
  aws/
    __init__.py
    adapter.py      # stub
  azure/
    __init__.py
    adapter.py      # stub
  tests/
    test_pattern.py
```

Run:

```bash
cd code
uv sync
uv run pytest
```

Environment variables for real cloud (optional): `AWS_PROFILE`, `AZURE_OPENAI_ENDPOINT`, etc. Default CI uses mock only.
