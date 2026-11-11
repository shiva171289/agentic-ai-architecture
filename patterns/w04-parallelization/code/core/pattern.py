from concurrent.futures import ThreadPoolExecutor

from core.llm import MockLLM, LLMResponse


def policy_lookup(question: str) -> str:
    return "12-month warranty." if "warranty" in question.lower() else "No policy."


def order_lookup(question: str) -> str:
    return "Order ORD-1001 shipped." if "ord-1001" in question.lower() else "No order."


def run_parallel(llm: MockLLM, question: str) -> LLMResponse:
    with ThreadPoolExecutor(max_workers=2) as pool:
        policy_f = pool.submit(policy_lookup, question)
        order_f = pool.submit(order_lookup, question)
        context = f"Policy: {policy_f.result()}\nOrder: {order_f.result()}"
    return llm.complete("Synthesize.", f"Question: {question}\n{context}")
