from app.models import ArticleCandidate
from app.search import search_news


def test_search_news_returns_article_candidates():
    results = search_news("AI", max_results=2)

    assert isinstance(results, list)
    assert len(results) == 2
    assert isinstance(results[0], ArticleCandidate)
    assert isinstance(results[1], ArticleCandidate)

    assert results[0].title != ""
    assert results[0].url != ""
    assert results[0].source != ""
    assert results[0].published_date != ""

    assert results[1].title != ""
    assert results[1].url != ""
    assert results[1].source != ""
    assert results[1].published_date != ""


def test_search_news_respects_max_results():
    results = search_news("AI", max_results=1)

    assert len(results) == 1
    assert isinstance(results[0], ArticleCandidate)
    assert results[0].title != ""
    assert results[0].url != ""