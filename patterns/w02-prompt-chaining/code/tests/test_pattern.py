from core.llm import MockLLM
from core.pattern import classify_intent, run_chain


def test_classify_billing():
    assert classify_intent("I need a refund") == "billing"


def test_chain_product_answer():
    llm = MockLLM()
    r = run_chain(llm, "reset my frozen widget")
    assert "product" in r.text.lower() or "context" in r.text.lower()
