from core.llm import MockLLM
from core.support import answer_faq


def critic_demo() -> None:
    """w06 — a wrong draft, the critic's verdict, and the rewrite."""

    from core.critic import answer_with_critic

    flawed = (
        "You can return your Acme Widget within 90 days for a full refund, "
        "even if you have opened it."
    )
    print("w06 — evaluator-optimizer")
    print(f"Draft: {flawed}")
    result = answer_with_critic(MockLLM(), "return window?", draft_fn=lambda: flawed)
    for i, verdict in enumerate(result.verdicts, start=1):
        print(f"  verdict {i}: passed={verdict['passed']} score={verdict['score']}")
    print(f"Reply: {result.answer}\n")


def react_demo() -> None:
    """w07 — the agent decides whether the order lookup is needed."""

    from core.react import react_answer

    print("w07 — ReAct loop")
    for question in (
        "What is the status of order ORD-2044?",
        "Order ORD-1001 status: shipped, item Acme Widget Pro.",
    ):
        result = react_answer(MockLLM(), question)
        print(f"Q: {question}")
        print(f"  steps={len(result.steps)} stop={result.stop_reason}")
        for step in result.steps:
            print(f"  tool={step.tool}{step.arguments} -> {step.observation}")
        print(f"A: {result.answer}\n")


def main() -> None:
    llm = MockLLM()
    questions = [
        "How do I reset my Acme Widget?",
        "What is the warranty period?",
    ]
    for q in questions:
        print(f"Q: {q}")
        print(f"A: {answer_faq(llm, q).text}\n")
    critic_demo()
    react_demo()


if __name__ == "__main__":
    main()
