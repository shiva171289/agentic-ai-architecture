from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str


class LLM:
    def complete(self, system: str, user: str) -> LLMResponse:
        raise NotImplementedError


class FastLLM(LLM):
    def complete(self, system: str, user: str) -> LLMResponse:
        return LLMResponse(text="[fast] answer")


class CapableLLM(LLM):
    def complete(self, system: str, user: str) -> LLMResponse:
        return LLMResponse(text="[capable] answer")
