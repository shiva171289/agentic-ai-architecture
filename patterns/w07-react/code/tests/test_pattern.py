from core.contracts import ToolCall, ToolSpec
from core.llm import MockLLM
from core.pattern import run_react
from core.tools import ToolRegistry, get_order_status, order_status_tool

FACTS_IN_REQUEST = "Order ORD-1001 status: shipped, ETA 2026-11-28."


def _registry() -> ToolRegistry:
    return ToolRegistry([order_status_tool()])


# --- the agent decides whether the lookup is needed -----------------------


def test_answers_without_a_tool_when_the_request_carries_the_facts():
    traj = run_react(MockLLM(), FACTS_IN_REQUEST, registry=_registry())
    assert traj.stop_reason == "answered"
    assert traj.steps == []
    assert "shipped" in traj.final_text


def test_agent_calls_the_tool_when_the_facts_are_missing():
    traj = run_react(MockLLM(), "What is the status of order ORD-2044?", registry=_registry())
    assert traj.stop_reason == "answered"
    assert len(traj.steps) == 1
    assert traj.steps[0].tool_call.name == "get_order_status"
    assert "processing" in traj.steps[0].result.content
    assert "processing" in traj.final_text


def test_tool_call_is_a_typed_block_not_parsed_text():
    traj = run_react(MockLLM(), "status of ORD-1001?", registry=_registry())
    call = traj.steps[0].tool_call
    assert isinstance(call, ToolCall)
    assert isinstance(call.arguments, dict)
    assert call.arguments["order_id"] == "ORD-1001"


# --- the pre-execution check ----------------------------------------------


def test_unknown_tool_is_rejected_before_execution():
    traj = run_react(MockLLM(force="unknown_tool"), "Refund ORD-1001", registry=_registry())
    step = traj.steps[0]
    assert step.result.ok is False
    assert "allowlist" in step.result.error


def test_malformed_arguments_are_rejected():
    traj = run_react(MockLLM(force="bad_args"), "status of ORD-1001?", registry=_registry())
    assert traj.steps[0].result.ok is False
    assert "required" in traj.steps[0].result.error


def test_registry_refuses_a_write_tool():
    write = ToolSpec(
        name="refund_order",
        description="Writes a refund.",
        parameters={"type": "object", "properties": {}, "required": []},
        handler=lambda _args: "refunded",
        scope="write",
    )
    error = ToolRegistry([write]).check(ToolCall("c1", "refund_order", {}))
    assert error is not None and "write" in error


# --- the stop rule is ours -------------------------------------------------


def test_step_cap_stops_the_loop():
    traj = run_react(
        MockLLM(force="always_tool"), "ORD-1001", registry=_registry(), max_steps=2
    )
    assert traj.stop_reason == "max_steps"
    assert len(traj.steps) == 2


def test_token_budget_stops_the_loop():
    traj = run_react(
        MockLLM(force="always_tool"), "ORD-1001", registry=_registry(), token_budget=0
    )
    assert traj.stop_reason == "budget"
    assert len(traj.steps) == 1


def test_wall_clock_budget_stops_the_loop():
    ticks = iter([0.0, 10.0])  # start, then a check 10 s later
    traj = run_react(
        MockLLM(force="always_tool"),
        "ORD-1001",
        registry=_registry(),
        wall_clock_ms=1000,
        clock=lambda: next(ticks),
    )
    assert traj.stop_reason == "budget"
    assert traj.steps == []


# --- the trace -------------------------------------------------------------


def test_trace_records_each_step():
    traj = run_react(MockLLM(), "status of ORD-1001?", registry=_registry())
    trace = traj.as_trace()
    assert trace["stop_reason"] == "answered"
    assert trace["steps"][0]["tool"] == "get_order_status"
    assert trace["steps"][0]["ok"] is True
    assert trace["steps"][0]["observation"]


# --- the tool itself -------------------------------------------------------


def test_order_tool_returns_status_and_handles_an_unknown_order():
    assert "processing" in get_order_status({"order_id": "ORD-2044"})
    assert "No order" in get_order_status({"order_id": "ORD-9999"})
