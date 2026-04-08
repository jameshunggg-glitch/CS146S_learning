from app.models import ArticleCandidate


def search_news(topic: str, max_results: int = 3) -> list[ArticleCandidate]:
    candidates = [
        ArticleCandidate(
            title=f"{topic} News 1",
            url="https://example.com/article1",
            source="BBC",
            published_date="2026-04-08",
            note="Stub result",
        ),
        ArticleCandidate(
            title=f"{topic} News 2",
            url="https://example.com/article2",
            source="Reuters",
            published_date="2026-04-07",
            note="Stub result",
        ),
        ArticleCandidate(
            title=f"{topic} News 3",
            url="https://example.com/article3",
            source="AP News",
            published_date="2026-04-06",
            note="Stub result",
        ),
    ]

    return candidates[:max_results]