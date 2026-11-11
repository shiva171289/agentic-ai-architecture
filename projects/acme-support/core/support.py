import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from core.llm import CapableMockLLM, FastMockLLM, LLM, LLMResponse
from core.retrieval import KeywordRetriever

_POLICIES_PATH = Path(__file__).resolve().parent.parent / "data" / "policies.json"
_ORDERS_PATH = Path(__file__).resolve().parent.parent / "data" / "orders.json"

SYSTEM_PROMPT = """You are Acme Manufacturing tier-1 support.
Answer using Context only. Do not invent policy.
If the user asks to open a ticket, respond with CREATE_TICKET in your reasoning only when appropriate.
Be concise."""

INTENT_PROMPTS = {
    "billing": "Answer billing and payment questions using Context only. Be brief.",
    "product": "Answer product and troubleshooting questions using Context only. Be brief.",
    "other": "Answer general support questions using Context only. Offer ticket if unsure.",
}

_retriever = KeywordRetriever()


def load_policies() -> list[dict]:
    with _POLICIES_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def load_orders() -> list[dict]:
    if not _ORDERS_PATH.exists():
        return []
    with _ORDERS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def retrieve_policy_snippet(question: str, policies: list[dict] | None = None) -> str:
    policies = policies if policies is not None else load_policies()
    return _retriever.retrieve(question, policies)


def fetch_order_snippet(question: str, orders: list[dict] | None = None) -> str:
    """Synthetic order lookup (w04+). Returns empty snippet when no order id."""
    orders = orders if orders is not None else load_orders()
    q = question.lower()
    for order in orders:
        if order["order_id"].lower() in q:
            return f"Order {order['order_id']}: status {order['status']}, item {order['item']}."
    return "No order context."


def classify_intent(question: str) -> str:
    q = question.lower()
    if any(w in q for w in ("refund", "invoice", "payment", "billing", "charge")):
        return "billing"
    if any(w in q for w in ("widget", "reset", "warranty", "broken", "frozen")):
        return "product"
    return "other"


def answer_for_intent(llm: LLM, question: str, intent: str, context: str) -> LLMResponse:
    system = INTENT_PROMPTS.get(intent, INTENT_PROMPTS["other"])
    user = f"Intent: {intent}\nQuestion: {question}\nContext: {context}"
    return llm.complete(system, user)


def answer_with_chain(llm: LLM, question: str, *, allow_tools: bool = False) -> LLMResponse:
    """w02 — classify then answer with specialized system prompt."""
    intent = classify_intent(question)
    context = retrieve_policy_snippet(question)
    response = answer_for_intent(llm, question, intent, context)
    if response.tool_call and not allow_tools:
        return LLMResponse(text="Tool blocked by policy.", tool_call=None)
    return response


def answer_faq(llm: LLM, question: str, *, allow_tools: bool = False) -> LLMResponse:
    """Entry point — uses prompt chain (w02+ stage)."""
    return answer_with_chain(llm, question, allow_tools=allow_tools)


def _is_complex(question: str, intent: str) -> bool:
    if intent == "other":
        return True
    if len(question.split()) > 18:
        return True
    return "dispute" in question.lower() or "exception" in question.lower()


def route_and_answer(question: str, *, allow_tools: bool = False) -> LLMResponse:
    """w03 — route simple FAQs to fast mock model, complex to capable mock model."""
    intent = classify_intent(question)
    context = retrieve_policy_snippet(question)
    if _is_complex(question, intent):
        llm: LLM = CapableMockLLM()
    else:
        llm = FastMockLLM()
    response = answer_for_intent(llm, question, intent, context)
    if response.tool_call and not allow_tools:
        return LLMResponse(text="Tool blocked by policy.", tool_call=None)
    return response


def answer_with_parallel_context(
    llm: LLM, question: str, *, allow_tools: bool = False
) -> LLMResponse:
    """w04 — retrieve policy and order snippet in parallel, then one synthesis call."""
    policies = load_policies()
    orders = load_orders()

    def policy_task() -> str:
        return _retriever.retrieve(question, policies)

    def order_task() -> str:
        return fetch_order_snippet(question, orders)

    with ThreadPoolExecutor(max_workers=2) as pool:
        policy_future = pool.submit(policy_task)
        order_future = pool.submit(order_task)
        policy_ctx = policy_future.result()
        order_ctx = order_future.result()

    context = f"Policy: {policy_ctx}\nOrder: {order_ctx}"
    intent = classify_intent(question)
    response = answer_for_intent(llm, question, intent, context)
    if response.tool_call and not allow_tools:
        return LLMResponse(text="Tool blocked by policy.", tool_call=None)
    return response
