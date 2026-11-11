from core.llm import MockLLM
from core.pattern import run_parallel


def test_parallel_merges():
    r = run_parallel(MockLLM(), "warranty on ORD-1001")
    assert "answer" in r.text.lower()
