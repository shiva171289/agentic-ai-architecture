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
        if "CREATE_TICKET" in user.upper():
            return LLMResponse(text="Ticket created.", tool_call="create_ticket")
        if "Context:" in user and "No matching policy" not in user:
            return LLMResponse(
                text="Based on Acme policy: follow the steps in Context. "
                "If unresolved, offer to create a support ticket."
            )
        if "No matching policy" in user:
            return LLMResponse(text="I could not find a matching policy. Would you like to open a ticket?")
        return LLMResponse(text="Please describe your Acme product issue.")
