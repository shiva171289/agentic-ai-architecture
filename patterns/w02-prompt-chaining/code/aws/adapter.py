"""AWS stub — Step Functions or Lambda chain."""

from core.llm import LLM, LLMResponse


class BedrockLLM(LLM):
    def complete(self, system: str, user: str) -> LLMResponse:
        raise NotImplementedError("Wire Bedrock per intent template")
