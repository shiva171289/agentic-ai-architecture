"""AWS adapter stub — wire to Bedrock + Knowledge Bases in a flagship repo."""

from core.llm import LLM, LLMResponse


class BedrockLLM(LLM):
    def complete(self, system: str, user: str) -> LLMResponse:
        raise NotImplementedError("Configure Bedrock client and model ID")
