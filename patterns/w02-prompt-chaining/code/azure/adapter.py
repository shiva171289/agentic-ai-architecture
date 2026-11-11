"""Azure stub — Durable Functions / Prompt Flow chain."""

from core.llm import LLM, LLMResponse


class FoundryLLM(LLM):
    def complete(self, system: str, user: str) -> LLMResponse:
        raise NotImplementedError("Wire Foundry chat deployment")
