from app.models import ArticleCandidate, ArticleDigest


def summarize_article(candidate: ArticleCandidate) -> ArticleDigest:
    return ArticleDigest(
        title=candidate.title,
        url=candidate.url,
        source=candidate.source,
        published_date=candidate.published_date,
        extraction_status="Success",
        summary=f"This is a stub summary for {candidate.title}.",
        key_points=[
            f"Key point 1 for {candidate.title}",
            f"Key point 2 for {candidate.title}",
        ],
        warnings=[
            "Stub summary only. Original article not parsed.",
        ],
    )