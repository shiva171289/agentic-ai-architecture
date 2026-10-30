from core.llm import MockLLM
from core.support import answer_faq


def main() -> None:
    llm = MockLLM()
    questions = [
        "How do I reset my Acme Widget?",
        "What is the warranty period?",
    ]
    for q in questions:
        print(f"Q: {q}")
        print(f"A: {answer_faq(llm, q).text}\n")


if __name__ == "__main__":
    main()
