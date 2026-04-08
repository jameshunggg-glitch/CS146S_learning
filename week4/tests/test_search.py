from app.models import ArticleCandidate
from app.search import search_news


def test_search_news_returns_stub_candidates():
    results = search_news("AI", max_results=2)

    assert len(results) == 2
    assert isinstance(results[0], ArticleCandidate)
    assert isinstance(results[1], ArticleCandidate)
    assert results[0].title == "AI News 1"
    assert results[1].title == "AI News 2"


def test_search_news_respects_max_results():
    results = search_news("AI", max_results=1)

    assert len(results) == 1
    assert results[0].title == "AI News 1"