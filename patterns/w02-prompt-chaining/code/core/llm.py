from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    tool_call: str | None = None


class LLM:
    def complete(self, system: str, user: str) -> LLMResponse:
        raise NotImplementedError


class MockLLM(LLM):
    def complete(self, system: str, user: str) -> LLMResponse:
        if "billing" in system.lower():
            return LLMResponse(text="Billing answer from context.")
        if "product" in system.lower():
            return LLMResponse(text="Product answer: see Context.")
        return LLMResponse(text="General answer from context.")
