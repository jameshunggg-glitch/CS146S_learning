from app.models import ArticleCandidate, ArticleDigest

candidate = ArticleCandidate(
    title="Test News",
    url="https://example.com",
    source="BBC",
    published_date="2026-04-08"
)

print(candidate)

digest = ArticleDigest(
    title="Test News",
    url="https://example.com",
    source="BBC",
    published_date="2026-04-08",
    extraction_status="Success",
    summary="This is a short summary.",
    key_points=[
        "Point one",
        "Point two",
        "Point three",
    ],
    warnings=[
        "Paywall not checked",
    ],
)

print(digest)
print(digest.key_points)
print(digest.warnings)