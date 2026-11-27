"""w07 — ReAct loop for the Acme support reply.

The w05/w06 stages fixed the path before the request ran: context was fetched,
a draft was written, a critic graded it. This stage lets the agent decide
*whether* it needs the order lookup before it writes the reply.

The model picks the action; our code owns the guardrails, all from the ADR:

- **A small, curated read-only tool set.** One tool, ``get_order_status``.
  Writes never enter the loop; they stay behind the existing approval gate.
- **Check the proposed call before execution.** ``check_tool_call`` allowlists
  the tool and validates the argument against its schema. A failed check
  becomes the observation, so the model can correct on the next step.
- **Own the stop rule.** ``MAX_STEPS`` is a code constant, not a prompt
  instruction. ReAct has no built-in terminator.
- **Record the trajectory.** ``ReactResult.trace()`` keeps the call and the
  observation per step, so a non-deterministic run stays explainable.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Callable

from core.llm import LLM

REACT_MARKER = "TASK:REACT"
MAX_STEPS = 4

ORDER_ID = re.compile(r"ORD-\d{3,}", re.IGNORECASE)

# The loop sees only read tools. A write is a separate, gated action.
READ_TOOLS = frozenset({"get_order_status"})

REACT_SYSTEM = (
    f"{REACT_MARKER}\n"
    "You are Acme Manufacturing tier-1 support. Decide whether you need the "
    "order lookup. If the request already carries the facts, answer without a "
    "tool. Use only the tool provided, and call at most one tool per step."
)


@dataclass(frozen=True)
class ToolCall:
    """A typed tool call. The model proposes it; we check it before running."""

    name: str
    arguments: dict


@dataclass
class ToolResult:
    name: str
    ok: bool
    content: str = ""
    error: str | None = None

    def as_message(self) -> str:
        return self.content if self.ok else f"ERROR: {self.error}"


@dataclass
class ReactStep:
    index: int
    tool: str
    arguments: dict
    observation: str
    ok: bool


@dataclass
class ReactResult:
    answer: str
    steps: list[ReactStep] = field(default_factory=list)
    stop_reason: str = "answered"  # "answered" | "max_steps"

    def trace(self) -> dict:
        return {
            "stop_reason": self.stop_reason,
            "steps": [
                {
                    "index": s.index,
                    "tool": s.tool,
                    "arguments": s.arguments,
                    "observation": s.observation,
                    "ok": s.ok,
                }
                for s in self.steps
            ],
        }


StepHook = Callable[[ReactStep], None]


# --- the tool layer -------------------------------------------------------


def get_order_status(order_id: str, orders: list[dict]) -> str:
    for order in orders:
        if order["order_id"].lower() == order_id.lower():
            return (
                f"Order {order['order_id']}: status {order['status']}, "
                f"item {order['item']}."
            )
    return f"No order found for {order_id}."


def check_tool_call(call: ToolCall) -> str | None:
    """The pre-execution check: allowlist the tool, validate the arguments."""

    if call.name not in READ_TOOLS:
        return f"tool {call.name!r} is not in the allowlist"
    order_id = call.arguments.get("order_id")
    if not isinstance(order_id, str) or not order_id:
        return "get_order_status requires a string order_id"
    return None


def execute_tool(call: ToolCall, orders: list[dict]) -> ToolResult:
    error = check_tool_call(call)
    if error is not None:
        return ToolResult(call.name, ok=False, error=error)
    return ToolResult(
        call.name, ok=True, content=get_order_status(call.arguments["order_id"], orders)
    )


# --- the loop -------------------------------------------------------------


def react_answer(
    llm: LLM,
    question: str,
    *,
    orders: list[dict] | None = None,
    max_steps: int = MAX_STEPS,
    on_step: StepHook | None = None,
) -> ReactResult:
    """Reason -> act -> observe until the agent answers or the cap fires.

    ``on_step`` is the trace hook: it fires once per tool step so the trace is
    recorded even when the loop later stops on the cap.
    """

    if orders is None:
        from core.support import load_orders

        orders = load_orders()

    transcript: list[dict] = []
    steps: list[ReactStep] = []

    for index in range(max_steps):
        payload = json.dumps({"question": question, "transcript": transcript})
        response = llm.complete(REACT_SYSTEM, payload)

        if not response.tool_call:
            return ReactResult(answer=response.text, steps=steps, stop_reason="answered")

        call = ToolCall(response.tool_call, response.tool_arguments or {})
        result = execute_tool(call, orders)
        step = ReactStep(
            index=index,
            tool=call.name,
            arguments=call.arguments,
            observation=result.as_message(),
            ok=result.ok,
        )
        steps.append(step)
        transcript.append({"tool": call.name, "observation": result.as_message()})
        if on_step:
            on_step(step)

    # The cap fired: return an honest fallback, not a half-finished answer.
    return ReactResult(
        answer="I need to check that — let me escalate to a human.",
        steps=steps,
        stop_reason="max_steps",
    )
