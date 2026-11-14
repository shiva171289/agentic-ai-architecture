from core.llm import MockLLM
from core.orchestrator import (
    MAX_WORKERS,
    Task,
    answer_with_orchestrator,
    decompose,
    default_orchestrator,
    order_worker,
    policy_worker,
)
from core.support import fetch_order_snippet, retrieve_policy_snippet


def test_decompose_multi_part_request():
    kinds = [t.kind for t in decompose("Where is my order ORD-1001 and the return window?")]
    assert kinds == ["order_lookup", "policy_lookup"]


def test_decompose_single_part_request():
    kinds = [t.kind for t in decompose("How do I reset my widget?")]
    assert kinds == ["policy_lookup"]


def test_decompose_caps_fan_out():
    long_q = "order and return and warranty and refund and policy and ship"
    assert len(decompose(long_q)) <= MAX_WORKERS


def test_merge_includes_both_workers():
    results = [
        policy_worker("warranty?", retrieve_policy_snippet)(Task("policy_lookup", "")),
        order_worker("ORD-1001 status", fetch_order_snippet)(Task("order_lookup", "")),
    ]
    from core.orchestrator import merge

    context = merge(results)
    assert "policy_lookup:" in context
    assert "order_lookup:" in context


def test_orchestrator_answer_uses_merged_context():
    r = default_orchestrator(MockLLM(), "Where is order ORD-1001 and the return window?")
    # The stub model answers from the merged worker context, not the fallback.
    assert "Context" in r.text
    assert "describe your Acme product issue" not in r.text.lower()


def test_orchestrator_blocks_tools_without_permission():
    r = answer_with_orchestrator(
        MockLLM(),
        "Please CREATE_TICKET for broken device and warranty",
        policy_lookup=retrieve_policy_snippet,
        order_lookup=fetch_order_snippet,
        allow_tools=False,
    )
    assert r.tool_call is None
