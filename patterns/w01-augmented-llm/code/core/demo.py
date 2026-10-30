from core.llm import MockLLM
from core.pattern import run_augmented


def main() -> None:
    llm = MockLLM()
    print(run_augmented(llm, "How do I reset my widget?").text)


if __name__ == "__main__":
    main()
