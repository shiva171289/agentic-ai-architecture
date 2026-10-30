from core.llm import LLM, LLMResponse


DOCS = {
    "reset": "Power button hold 10 seconds to reset Acme Widget.",
    "warranty": "Acme Widget warranty is 12 months from purchase.",
}


def retrieve(query: str) -> str:
    q = query.lower()
    for key, text in DOCS.items():
        if key in q:
            return text
    return "No matching document."


def run_augmented(llm: LLM, question: str, *, allow_tools: bool = False) -> LLMResponse:
    context = retrieve(question)
    system = "You answer using Context only. If user asks to open ticket, respond CREATE_TICKET."
    user = f"Question: {question}\nContext: {context}"
    response = llm.complete(system, user)
    if response.tool_call and not allow_tools:
        return LLMResponse(text="Tool blocked by policy.", tool_call=None)
    return response
