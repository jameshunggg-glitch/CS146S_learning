from app.models import ArticleCandidate
from app.summarizer import summarize_article

candidate = ArticleCandidate(
    title="AI News 1",
    url="https://example.com/article1",
    source="BBC",
    published_date="2026-04-08",
    note="Stub result",
)

digest = summarize_article(candidate)

print(digest)
print(digest.summary)
print(digest.key_points)
print(digest.warnings)