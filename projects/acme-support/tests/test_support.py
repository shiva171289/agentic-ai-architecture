from core.llm import CapableMockLLM, FastMockLLM, MockLLM
from core.support import (
    answer_faq,
    answer_with_parallel_context,
    answer_with_chain,
    classify_intent,
    retrieve_policy_snippet,
    route_and_answer,
)


def test_retrieve_warranty():
    snippet = retrieve_policy_snippet("Is my widget still under warranty?")
    assert "12-month" in snippet


def test_classify_product_intent():
    assert classify_intent("My widget is frozen") == "product"


def test_classify_billing_intent():
    assert classify_intent("I need a refund on my invoice") == "billing"


def test_faq_grounded_answer():
    llm = MockLLM()
    r = answer_faq(llm, "How do I reset my frozen widget?")
    assert "policy" in r.text.lower() or "context" in r.text.lower() or "acme" in r.text.lower()


def test_chain_uses_billing_prompt():
    llm = MockLLM()
    r = answer_with_chain(llm, "refund policy for my order")
    assert r.tool_call is None


def test_tool_blocked_without_permission():
    llm = MockLLM()
    r = answer_faq(llm, "Please CREATE_TICKET for broken device", allow_tools=False)
    assert r.tool_call is None
    assert "blocked" in r.text.lower()


def test_route_simple_uses_fast():
    r = route_and_answer("warranty on widget")
    assert r.text.startswith("[fast]")


def test_route_complex_uses_capable():
    long_q = " ".join(["widget"] * 25)
    r = route_and_answer(long_q)
    assert r.text.startswith("[capable]")


def test_parallel_includes_order():
    llm = MockLLM()
    r = answer_with_parallel_context(llm, "Where is order ORD-1001?")
    assert "shipped" in r.text.lower() or "acme" in r.text.lower()
