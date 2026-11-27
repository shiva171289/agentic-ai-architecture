"""ReAct loop: reason -> act -> observe, bounded by our stop rule.

The loop is the first place control flow leaves the code. The model chooses
the next action; our code owns what it can call (allowlist), what it may pass
(schema), and when it stops (a step cap plus a token and wall-clock budget).
ReAct has no built-in terminator, so the stop rule is ours, not the model's.
"""

from __future__ import annotations

import time
from typing import Callable

from core.contracts import Message, Step, Trajectory
from core.llm import LLM
from core.tools import ToolRegistry

DEFAULT_MAX_STEPS = 4
DEFAULT_TOKEN_BUDGET = 4000
DEFAULT_WALL_CLOCK_MS = 2000

SYSTEM_PROMPT = (
    "You are Acme tier-1 support. Decide whether you need the order lookup. "
    "If the request already carries the facts, answer without a tool. Use only "
    "the tools provided, and call at most one tool per step."
)

StepHook = Callable[[Step], None]


def estimate_tokens(*texts: str) -> int:
    """Rough token count for the budget. A real client reads the usage field."""

    return sum(len(t) for t in texts) // 4


def run_react(
    llm: LLM,
    request: str,
    *,
    registry: ToolRegistry,
    system: str = SYSTEM_PROMPT,
    max_steps: int = DEFAULT_MAX_STEPS,
    token_budget: int = DEFAULT_TOKEN_BUDGET,
    wall_clock_ms: int = DEFAULT_WALL_CLOCK_MS,
    on_step: StepHook | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> Trajectory:
    """Run the bounded loop and return the trajectory with a stop reason.

    ``on_step`` is the trace hook: it fires once per tool step, so the
    reasoning, the call and the observation are recorded even when the loop
    later stops on the cap.
    """

    tools = registry.specs()
    messages = [Message(role="user", content=request)]
    trajectory = Trajectory()
    start = clock()

    for index in range(max_steps):
        if trajectory.tokens_used > token_budget:
            trajectory.stop_reason = "budget"
            return trajectory
        if (clock() - start) * 1000.0 > wall_clock_ms:
            trajectory.stop_reason = "budget"
            return trajectory

        response = llm.complete(system, messages, tools)
        trajectory.tokens_used += estimate_tokens(
            system, request, response.thought, response.text
        )

        if response.tool_call is None:
            trajectory.final_text = response.text
            trajectory.stop_reason = "answered"
            return trajectory

        # check() runs inside execute(): allowlist + schema, before the call.
        result = registry.execute(response.tool_call)
        step = Step(
            index=index,
            thought=response.thought,
            tool_call=response.tool_call,
            result=result,
        )
        trajectory.steps.append(step)
        trajectory.tokens_used += estimate_tokens(result.as_message())

        messages.append(
            Message(role="assistant", content=response.thought, tool_call=response.tool_call)
        )
        messages.append(Message(role="tool", content=result.as_message()))

        if on_step:
            on_step(step)

    trajectory.stop_reason = "max_steps"
    return trajectory
