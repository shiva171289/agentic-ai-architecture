"""Deterministic mock LLM for the ReAct sample.

The provider's contract is a typed ``tool_call`` block, not prose. The mock
returns the same shape a real provider returns, so the loop is exercised
without API keys and the tests are stable across runs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from core.contracts import Message, ToolCall, ToolSpec

ORDER_ID = re.compile(r"ORD-\d{3,}", re.IGNORECASE)


@dataclass
class LLMResponse:
    """One model turn: a thought, and either a tool call or a final answer."""

    thought: str = ""
    tool_call: ToolCall | None = None
    text: str = ""

    @property
    def stop_reason(self) -> str:
        return "tool_use" if self.tool_call is not None else "end_turn"


class LLM:
    def complete(
        self, system: str, messages: list[Message], tools: list[ToolSpec]
    ) -> LLMResponse:  # pragma: no cover
        raise NotImplementedError


class MockLLM(LLM):
    """A model that decides whether the lookup is needed.

    It carries the two behaviours the ADR cares about: it answers without a
    tool call when the request already carries the facts, and it calls
    ``get_order_status`` when it does not. ``force`` lets a test drive the
    failure paths (an unknown tool, a malformed argument, a loop that never
    stops).
    """

    def __init__(self, *, force: str | None = None) -> None:
        # force: None | "unknown_tool" | "bad_args" | "always_tool"
        self._force = force

    def complete(
        self, system: str, messages: list[Message], tools: list[ToolSpec]
    ) -> LLMResponse:
        user = next((m.content for m in messages if m.role == "user"), "")
        last = messages[-1]

        # A loop that never takes a final answer, for the cap tests.
        if self._force == "always_tool":
            return LLMResponse(
                thought="Check the order.",
                tool_call=ToolCall("call_1", "get_order_status", {"order_id": "ORD-1001"}),
            )

        # A tool result already arrived: answer from it.
        if last.role == "tool":
            return LLMResponse(text=f"Here is what I found: {last.content}")

        if self._force == "unknown_tool":
            return LLMResponse(
                thought="I will try a write tool.",
                tool_call=ToolCall("call_1", "refund_order", {"order_id": "ORD-1001"}),
            )
        if self._force == "bad_args":
            return LLMResponse(
                thought="I will call the tool with a wrong argument.",
                tool_call=ToolCall("call_1", "get_order_status", {}),
            )

        # The request already carries the facts (order number + status) -> no
        # tool call. This is the decision the ADR says belongs to the agent.
        if self._facts_present(user):
            return LLMResponse(text=f"Answering from the request: {user}")

        match = ORDER_ID.search(user)
        if match:
            return LLMResponse(
                thought="I need the live order status.",
                tool_call=ToolCall(
                    "call_1", "get_order_status", {"order_id": match.group(0).upper()}
                ),
            )
        return LLMResponse(text="I could not find an order id. Please share it.")

    @staticmethod
    def _facts_present(user: str) -> bool:
        # "status:" (with the colon) means the request is stating the facts,
        # so the live lookup would be a wasted tool round-trip.
        return "status:" in user.lower()
