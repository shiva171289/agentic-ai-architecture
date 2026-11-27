"""Tool registry, the order tool, and the pre-execution check.

The registry owns the tool set the agent can see. ``check`` is the
pre-execution control the ADR asks for: a proposed call must name a tool in the
allowlist and its arguments must validate against the tool's schema *before*
the handler runs. The registry refuses any tool whose scope is not ``"read"``.
"""

from __future__ import annotations

from core.contracts import ToolCall, ToolResult, ToolSpec

ORDERS: dict[str, dict] = {
    "ORD-1001": {"status": "shipped", "item": "Acme Widget Pro", "eta": "2026-11-28"},
    "ORD-2044": {"status": "processing", "item": "Acme Widget Mini", "eta": "2026-12-02"},
}


def get_order_status(args: dict) -> str:
    order_id = args.get("order_id", "")
    order = ORDERS.get(order_id)
    if order is None:
        return f"No order found for {order_id!r}."
    return f"Order {order_id}: {order['status']}, item {order['item']}, ETA {order['eta']}."


def order_status_tool() -> ToolSpec:
    return ToolSpec(
        name="get_order_status",
        description="Return the current status of one Acme order by order id.",
        parameters={
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
        },
        handler=get_order_status,
        scope="read",
    )


class ToolRegistry:
    """Holds the tools the loop may call and gates every proposed call."""

    def __init__(self, tools: list[ToolSpec]) -> None:
        self._tools = {t.name: t for t in tools}

    def specs(self) -> list[ToolSpec]:
        return list(self._tools.values())

    def check(self, call: ToolCall) -> str | None:
        """Return an error string if the call must not run, else ``None``.

        Two controls, both *before* execution: the tool must be in the
        allowlist (and not a write), and the arguments must satisfy the tool's
        schema. A failed check becomes the observation, so the model can
        correct on the next step.
        """

        spec = self._tools.get(call.name)
        if spec is None:
            return f"tool {call.name!r} is not in the allowlist"
        if spec.scope != "read":
            return f"tool {call.name!r} is a write and is not allowed in the loop"
        missing = [
            key
            for key in spec.parameters.get("required", [])
            if key not in call.arguments
        ]
        if missing:
            return f"tool {call.name!r} missing required arguments: {', '.join(missing)}"
        for key, value in call.arguments.items():
            prop = spec.parameters.get("properties", {}).get(key, {})
            if prop.get("type") == "string" and not isinstance(value, str):
                return f"tool {call.name!r} argument {key!r} must be a string"
        return None

    def execute(self, call: ToolCall) -> ToolResult:
        error = self.check(call)
        if error is not None:
            return ToolResult(call.id, call.name, ok=False, error=error)
        spec = self._tools[call.name]
        try:
            content = spec.handler(call.arguments)
        except Exception as exc:  # pragma: no cover - defensive
            return ToolResult(call.id, call.name, ok=False, error=str(exc))
        return ToolResult(call.id, call.name, ok=True, content=content)
