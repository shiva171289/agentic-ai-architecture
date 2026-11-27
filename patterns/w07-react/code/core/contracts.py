"""Shared contracts for the ReAct sample.

The loop is four things: a tool registry, a typed tool call, a typed
observation, and a trajectory. The provider's tool contract is a typed
``tool_call`` block that our code executes and returns as a ``tool_result``
block — not a "Thought / Action / Observation" string we parse back out of the
model's prose.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class ToolSpec:
    """One tool: a name, a description, a JSON-schema subset, and a handler.

    ``scope`` is the identity the tool runs under. The loop only exposes read
    tools; a write is a separate, gated action and never runs inside the loop.
    """

    name: str
    description: str
    parameters: dict
    handler: Callable[[dict], str]
    scope: str = "read"


@dataclass(frozen=True)
class ToolCall:
    """A typed tool-call block, exactly as the provider returns it."""

    id: str
    name: str
    arguments: dict


@dataclass
class ToolResult:
    """A typed tool-result block, returned to the model as an observation."""

    tool_call_id: str
    name: str
    ok: bool
    content: str = ""
    error: str | None = None

    def as_message(self) -> str:
        return self.content if self.ok else f"ERROR: {self.error}"


@dataclass
class Message:
    """One turn in the conversation sent back to the model each step."""

    role: str  # "user" | "assistant" | "tool"
    content: str = ""
    tool_call: ToolCall | None = None


@dataclass
class Step:
    """One reason -> act -> observe turn. This is what the trace stores."""

    index: int
    thought: str
    tool_call: ToolCall | None
    result: ToolResult | None


@dataclass
class Trajectory:
    """The whole run, kept so a bad answer can be explained afterwards."""

    steps: list[Step] = field(default_factory=list)
    final_text: str = ""
    stop_reason: str = "answered"  # "answered" | "max_steps" | "budget"
    tokens_used: int = 0

    def as_trace(self) -> dict:
        return {
            "stop_reason": self.stop_reason,
            "tokens_used": self.tokens_used,
            "steps": [
                {
                    "index": s.index,
                    "thought": s.thought,
                    "tool": s.tool_call.name if s.tool_call else None,
                    "arguments": s.tool_call.arguments if s.tool_call else None,
                    "observation": s.result.as_message() if s.result else None,
                    "ok": s.result.ok if s.result else None,
                }
                for s in self.steps
            ],
        }
