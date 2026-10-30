import json
from pathlib import Path

from core.llm import LLM, LLMResponse

_POLICIES_PATH = Path(__file__).resolve().parent.parent / "data" / "policies.json"

SYSTEM_PROMPT = """You are Acme Manufacturing tier-1 support.
Answer using Context only. Do not invent policy.
If the user asks to open a ticket, respond with CREATE_TICKET in your reasoning only when appropriate.
Be concise."""


def load_policies() -> list[dict]:
    with _POLICIES_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def retrieve_policy_snippet(question: str, policies: list[dict] | None = None) -> str:
    """Naive keyword retrieval (w01 stage — vector search comes later)."""
    policies = policies if policies is not None else load_policies()
    q = question.lower()
    for entry in policies:
        if any(kw in q for kw in entry["keywords"]):
            return entry["text"]
    return "No matching policy."


def answer_faq(llm: LLM, question: str, *, allow_tools: bool = False) -> LLMResponse:
    context = retrieve_policy_snippet(question)
    user = f"Question: {question}\nContext: {context}"
    response = llm.complete(SYSTEM_PROMPT, user)
    if response.tool_call and not allow_tools:
        return LLMResponse(text="Tool blocked by policy.", tool_call=None)
    return response
