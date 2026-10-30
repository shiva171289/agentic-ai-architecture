"""Azure adapter stub — wire to Azure OpenAI / Foundry in a flagship repo."""

from core.llm import LLM, LLMResponse


class FoundryLLM(LLM):
    def complete(self, system: str, user: str) -> LLMResponse:
        raise NotImplementedError("Configure Azure OpenAI client and deployment")
