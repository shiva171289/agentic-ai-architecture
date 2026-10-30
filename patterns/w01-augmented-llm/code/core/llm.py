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
        if "Context:" in user:
            return LLMResponse(text="Based on the docs: reset the device using the power button.")
        return LLMResponse(text="I need more context.")
