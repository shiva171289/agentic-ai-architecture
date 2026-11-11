from core.retrieval import KeywordRetriever


def test_keyword_retriever():
    docs = [{"keywords": ["warranty"], "text": "12-month warranty."}]
    r = KeywordRetriever()
    assert "12-month" in r.retrieve("warranty question", docs)
