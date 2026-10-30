from core.llm import MockLLM
from core.support import answer_faq, retrieve_policy_snippet


def test_retrieve_warranty():
    snippet = retrieve_policy_snippet("Is my widget still under warranty?")
    assert "12-month" in snippet


def test_faq_grounded_answer():
    llm = MockLLM()
    r = answer_faq(llm, "How do I reset my frozen widget?")
    assert "policy" in r.text.lower() or "context" in r.text.lower() or "acme" in r.text.lower()


def test_tool_blocked_without_permission():
    llm = MockLLM()
    r = answer_faq(llm, "Please CREATE_TICKET for broken device", allow_tools=False)
    assert r.tool_call is None
    assert "blocked" in r.text.lower()
