from core.llm import MockLLM
from core.pattern import run_augmented


def test_retrieval_grounded_answer():
    llm = MockLLM()
    r = run_augmented(llm, "How do I reset my widget?")
    assert "power button" in r.text.lower()


def test_tool_blocked_without_permission():
    llm = MockLLM()
    r = run_augmented(llm, "Please CREATE_TICKET for broken device", allow_tools=False)
    assert r.tool_call is None
    assert "blocked" in r.text.lower()
