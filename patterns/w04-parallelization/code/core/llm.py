from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str


class MockLLM:
    def complete(self, system: str, user: str) -> LLMResponse:
        return LLMResponse(text="Merged context answer.")
