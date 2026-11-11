from core.llm import LLM, LLMResponse


class FoundryRouter(LLM):
    def complete(self, system: str, user: str) -> LLMResponse:
        raise NotImplementedError("Select deployment per route")
