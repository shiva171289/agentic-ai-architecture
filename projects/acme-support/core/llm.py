from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    tool_call: str | None = None


class LLM:
    def complete(self, system: str, user: str) -> LLMResponse:
        raise NotImplementedError


class MockLLM(LLM):
    """Deterministic mock for tests and local demos."""

    def complete(self, system: str, user: str) -> LLMResponse:
        return _default_complete(system, user)


def _default_complete(system: str, user: str) -> LLMResponse:
    if "CREATE_TICKET" in user.upper():
        return LLMResponse(text="Ticket created.", tool_call="create_ticket")
    has_order_ctx = "order:" in user.lower() and "status" in user.lower()
    policy_miss = "no matching policy" in user.lower() or "policy: no matching" in user.lower()
    if has_order_ctx or (
        "context:" in user.lower() and not policy_miss
    ):
        return LLMResponse(
            text="Based on Acme policy and order Context: follow the steps given. "
            "If unresolved, offer to create a support ticket."
        )
    if policy_miss and not has_order_ctx:
        return LLMResponse(text="I could not find a matching policy. Would you like to open a ticket?")
    return LLMResponse(text="Please describe your Acme product issue.")


class FastMockLLM(LLM):
    """w03 — cheaper path for simple FAQs."""

    def complete(self, system: str, user: str) -> LLMResponse:
        r = _default_complete(system, user)
        return LLMResponse(text=f"[fast] {r.text}", tool_call=r.tool_call)


class CapableMockLLM(LLM):
    """w03 — capable path for ambiguous or long questions."""

    def complete(self, system: str, user: str) -> LLMResponse:
        r = _default_complete(system, user)
        return LLMResponse(text=f"[capable] {r.text}", tool_call=r.tool_call)
