from app.models import ArticleCandidate, ArticleDigest
from app.summarizer import summarize_article


def test_summarize_article_returns_digest():
    candidate = ArticleCandidate(
        title="AI News 1",
        url="https://example.com/article1",
        source="BBC",
        published_date="2026-04-08",
        note="Stub result",
    )

    digest = summarize_article(candidate)

    assert isinstance(digest, ArticleDigest)
    assert digest.title == "AI News 1"
    assert digest.url == "https://example.com/article1"
    assert digest.source == "BBC"
    assert digest.published_date == "2026-04-08"
    assert digest.extraction_status == "Success"
    assert "AI News 1" in digest.summary
    assert len(digest.key_points) == 2
    assert len(digest.warnings) == 1