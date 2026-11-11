from core.llm import LLM, LLMResponse


class BedrockRouter(LLM):
    def complete(self, system: str, user: str) -> LLMResponse:
        raise NotImplementedError("Select modelId per route")
