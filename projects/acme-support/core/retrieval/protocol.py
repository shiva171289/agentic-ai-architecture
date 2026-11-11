from typing import Protocol


class Retriever(Protocol):
    """Acme retrieval interface — variants added per content/topics/retrieval-ladder.md."""

    def retrieve(self, query: str, documents: list[dict]) -> str:
        """Return the best snippet or a not-found message."""
