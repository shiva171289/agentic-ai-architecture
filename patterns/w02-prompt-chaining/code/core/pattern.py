from core.llm import LLM, LLMResponse

DOCS = {
    "billing": "Refunds within 30 days with receipt.",
    "product": "Hold power 10 seconds to reset Acme Widget.",
}

INTENTS = {
    "billing": "You answer billing questions. Use Context only.",
    "product": "You answer product questions. Use Context only.",
    "other": "You answer general questions. Use Context only.",
}


def classify_intent(question: str) -> str:
    q = question.lower()
    if any(w in q for w in ("refund", "invoice", "payment")):
        return "billing"
    if any(w in q for w in ("widget", "reset", "frozen")):
        return "product"
    return "other"


def retrieve(intent: str, question: str) -> str:
    if intent == "billing":
        return DOCS["billing"]
    if intent == "product":
        return DOCS["product"]
    return "No matching document."


def run_chain(llm: LLM, question: str) -> LLMResponse:
    intent = classify_intent(question)
    context = retrieve(intent, question)
    system = INTENTS[intent]
    user = f"Question: {question}\nContext: {context}"
    return llm.complete(system, user)
