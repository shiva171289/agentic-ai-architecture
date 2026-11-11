from core.retrieval.protocol import Retriever


class KeywordRetriever:
    """w01 — naive keyword / contains match over policy entries."""

    def retrieve(self, query: str, documents: list[dict]) -> str:
        q = query.lower()
        for entry in documents:
            if any(kw in q for kw in entry["keywords"]):
                return entry["text"]
        return "No matching policy."
