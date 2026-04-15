"""
test_integration.py — Small integration test using fake article data.

Verifies that:
- Cleaned text can be passed into the writer.
- Both digest and articles Markdown files are generated successfully.

No live network calls. All data is fake/hardcoded.
"""

import os
import pytest
from app.clean import clean_text
from app.writer import write_digest, write_articles


FAKE_RAW_ARTICLES = [
    {
        "title": "AI Reasoning Models Reach New Milestone",
        "source": "Tech News Daily",
        "published_date": "2025-04-10",
        "url": "https://example.com/ai-reasoning-milestone",
        "raw_text": (
            "AI reasoning systems made significant strides in early 2025.\n"
            "Continue reading\n"
            "The gains were most visible in mathematical benchmarks.\n"
            "Advertisement\n"
        ),
        "summary": "AI reasoning models hit a new milestone in 2025.",
    },
    {
        "title": "Open Source Models Close the Gap",
        "source": "Open AI Weekly",
        "published_date": "2025-04-11",
        "url": "https://example.com/open-source-gap",
        "raw_text": (
            "Open source releases surprised the industry in 2025.\n"
            "Subscribe\n"
            "Performance narrowed the gap with proprietary alternatives.\n"
        ),
        "summary": "Open source models became competitive with closed alternatives.",
    },
]


def build_articles(raw_articles: list[dict]) -> tuple[list[dict], list[dict]]:
    """Shared helper: clean raw text and split into digest and full article lists."""
    digest_articles = []
    full_articles = []

    for article in raw_articles:
        cleaned = clean_text(article["raw_text"])
        base = {
            "title": article["title"],
            "source": article["source"],
            "published_date": article["published_date"],
            "url": article["url"],
        }
        digest_articles.append({**base, "summary": article["summary"]})
        full_articles.append({**base, "cleaned_text": cleaned})

    return digest_articles, full_articles


class TestIntegration:
    def test_both_files_are_created(self, tmp_path):
        digest_articles, full_articles = build_articles(FAKE_RAW_ARTICLES)
        digest_path = write_digest("AI", digest_articles, output_dir=str(tmp_path))
        articles_path = write_articles("AI", full_articles, output_dir=str(tmp_path))
        assert os.path.isfile(digest_path)
        assert os.path.isfile(articles_path)

    def test_digest_and_articles_are_different_files(self, tmp_path):
        digest_articles, full_articles = build_articles(FAKE_RAW_ARTICLES)
        digest_path = write_digest("AI", digest_articles, output_dir=str(tmp_path))
        articles_path = write_articles("AI", full_articles, output_dir=str(tmp_path))
        assert digest_path != articles_path

    def test_noise_removed_from_articles_file(self, tmp_path):
        digest_articles, full_articles = build_articles(FAKE_RAW_ARTICLES)
        articles_path = write_articles("AI", full_articles, output_dir=str(tmp_path))
        content = open(articles_path, encoding="utf-8").read()
        assert "Continue reading" not in content
        assert "Advertisement" not in content
        assert "Subscribe" not in content

    def test_article_body_preserved_in_articles_file(self, tmp_path):
        digest_articles, full_articles = build_articles(FAKE_RAW_ARTICLES)
        articles_path = write_articles("AI", full_articles, output_dir=str(tmp_path))
        content = open(articles_path, encoding="utf-8").read()
        assert "mathematical benchmarks" in content
        assert "narrowed the gap" in content

    def test_summaries_in_digest_not_in_articles(self, tmp_path):
        digest_articles, full_articles = build_articles(FAKE_RAW_ARTICLES)
        digest_path = write_digest("AI", digest_articles, output_dir=str(tmp_path))
        articles_path = write_articles("AI", full_articles, output_dir=str(tmp_path))
        digest_content = open(digest_path, encoding="utf-8").read()
        articles_content = open(articles_path, encoding="utf-8").read()
        assert "new milestone in 2025" in digest_content
        assert "new milestone in 2025" not in articles_content

    def test_both_article_titles_appear_in_both_files(self, tmp_path):
        digest_articles, full_articles = build_articles(FAKE_RAW_ARTICLES)
        digest_path = write_digest("AI", digest_articles, output_dir=str(tmp_path))
        articles_path = write_articles("AI", full_articles, output_dir=str(tmp_path))
        for path in (digest_path, articles_path):
            content = open(path, encoding="utf-8").read()
            assert "AI Reasoning Models Reach New Milestone" in content
            assert "Open Source Models Close the Gap" in content
