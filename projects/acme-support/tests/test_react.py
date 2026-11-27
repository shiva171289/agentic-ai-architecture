from core.llm import LLM, LLMResponse, MockLLM
from core.react import (
    MAX_STEPS,
    READ_TOOLS,
    ToolCall,
    check_tool_call,
    get_order_status,
    react_answer,
)

ORDERS = [
    {"order_id": "ORD-1001", "status": "shipped", "item": "Acme Widget Pro"},
    {"order_id": "ORD-2044", "status": "processing", "item": "Acme Widget Mini"},
]

FACTS_IN_REQUEST = "Order ORD-1001 status: shipped, item Acme Widget Pro."


class RecordingLLM(MockLLM):
    def __init__(self):
        self.systems: list[str] = []

    def complete(self, system: str, user: str) -> LLMResponse:
        self.systems.append(system)
        return super().complete(system, user)


# --- the agent decides whether to act -------------------------------------


def test_answers_without_a_tool_when_the_request_carries_the_facts():
    result = react_answer(MockLLM(), FACTS_IN_REQUEST, orders=ORDERS)
    assert result.stop_reason == "answered"
    assert result.steps == []
    assert "no lookup is needed" in result.answer.lower()


def test_calls_the_tool_when_the_facts_are_missing():
    result = react_answer(MockLLM(), "What is the status of order ORD-2044?", orders=ORDERS)
    assert result.stop_reason == "answered"
    assert len(result.steps) == 1
    assert result.steps[0].tool == "get_order_status"
    assert result.steps[0].arguments["order_id"] == "ORD-2044"
    assert "processing" in result.answer


def test_answers_a_request_with_no_order_number():
    result = react_answer(MockLLM(), "Where is my widget?", orders=ORDERS)
    assert result.steps == []
    assert "order number" in result.answer.lower()


# --- the pre-execution check ----------------------------------------------


def test_unknown_tool_is_rejected_before_execution():
    call = ToolCall("refund_order", {"order_id": "ORD-1001"})
    assert "allowlist" in (check_tool_call(call) or "")


def test_bad_arguments_are_rejected():
    call = ToolCall("get_order_status", {})
    assert "order_id" in (check_tool_call(call) or "")


def test_write_tools_are_not_in_the_loop():
    assert READ_TOOLS == {"get_order_status"}


# --- the stop rule is ours -------------------------------------------------


def test_the_cap_fires_and_returns_an_honest_fallback():
    class AlwaysTool(LLM):
        def complete(self, system: str, user: str) -> LLMResponse:
            return LLMResponse(
                text="",
                tool_call="get_order_status",
                tool_arguments={"order_id": "ORD-2044"},
            )

    result = react_answer(AlwaysTool(), "status?", orders=ORDERS, max_steps=2)
    assert result.stop_reason == "max_steps"
    assert len(result.steps) == 2  # the two allowed steps ran
    assert "escalate" in result.answer.lower()


# --- the trace -------------------------------------------------------------


def test_trace_records_the_call_and_the_observation():
    result = react_answer(MockLLM(), "status of ORD-1001?", orders=ORDERS)
    trace = result.trace()
    assert trace["stop_reason"] == "answered"
    assert trace["steps"][0]["tool"] == "get_order_status"
    assert trace["steps"][0]["ok"] is True
    assert "shipped" in trace["steps"][0]["observation"]


# --- the tool itself -------------------------------------------------------


def test_order_tool_returns_status_and_handles_an_unknown_order():
    assert "processing" in get_order_status("ORD-2044", ORDERS)
    assert "No order" in get_order_status("ORD-9999", ORDERS)
