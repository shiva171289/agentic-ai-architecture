from core.llm import CapableLLM, FastLLM, LLM, LLMResponse


def is_complex(question: str) -> bool:
    return len(question.split()) > 15 or "dispute" in question.lower()


def route_and_complete(question: str) -> LLMResponse:
    llm: LLM = CapableLLM() if is_complex(question) else FastLLM()
    return llm.complete("Answer support questions.", f"Question: {question}")
