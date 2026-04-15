"""
test_writer.py — Tests for app/writer.py.

Covers:
- Digest file contains expected sections (title, source, link, summary).
- Articles file contains cleaned article text.
"""

import os
import pytest
from app.writer import write_digest, write_articles


FAKE_ARTICLES = [
    {
        "title": "AI Breaks New Ground in 2025",
        "source": "Tech News Daily",
        "published_date": "2025-04-10",
        "url": "https://example.com/ai-breaks-ground",
        "summary": "Researchers have achieved a new milestone in AI reasoning capabilities.",
        "cleaned_text": "AI systems showed remarkable progress in 2025. Several labs reported improved reasoning benchmarks.",
    },
    {
        "title": "Open Source Models Catching Up",
        "source": "Open AI Weekly",
        "published_date": "2025-04-11",
        "url": "https://example.com/open-source-models",
        "summary": "Open source models are now competitive with proprietary alternatives.",
        "cleaned_text": "A wave of open source releases in early 2025 narrowed the gap with closed models significantly.",
    },
]


class TestWriteDigest:
    def test_creates_file(self, tmp_path):
        path = write_digest("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        assert os.path.isfile(path)

    def test_filename_contains_topic(self, tmp_path):
        path = write_digest("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        assert "AI" in os.path.basename(path)

    def test_filename_ends_with_digest(self, tmp_path):
        path = write_digest("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        assert os.path.basename(path).endswith("_digest.md")

    def test_contains_topic_header(self, tmp_path):
        path = write_digest("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        content = open(path, encoding="utf-8").read()
        assert "AI" in content

    def test_contains_article_titles(self, tmp_path):
        path = write_digest("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        content = open(path, encoding="utf-8").read()
        assert "AI Breaks New Ground in 2025" in content
        assert "Open Source Models Catching Up" in content

    def test_contains_sources(self, tmp_path):
        path = write_digest("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        content = open(path, encoding="utf-8").read()
        assert "Tech News Daily" in content
        assert "Open AI Weekly" in content

    def test_contains_links(self, tmp_path):
        path = write_digest("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        content = open(path, encoding="utf-8").read()
        assert "https://example.com/ai-breaks-ground" in content
        assert "https://example.com/open-source-models" in content

    def test_contains_summaries(self, tmp_path):
        path = write_digest("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        content = open(path, encoding="utf-8").read()
        assert "Researchers have achieved a new milestone" in content
        assert "competitive with proprietary alternatives" in content

    def test_does_not_contain_cleaned_text(self, tmp_path):
        path = write_digest("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        content = open(path, encoding="utf-8").read()
        assert "narrowed the gap with closed models" not in content

    def test_article_count_shown(self, tmp_path):
        path = write_digest("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        content = open(path, encoding="utf-8").read()
        assert "2" in content

    def test_empty_articles_list(self, tmp_path):
        path = write_digest("AI", [], output_dir=str(tmp_path))
        assert os.path.isfile(path)
        content = open(path, encoding="utf-8").read()
        assert "AI" in content


class TestWriteArticles:
    def test_creates_file(self, tmp_path):
        path = write_articles("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        assert os.path.isfile(path)

    def test_filename_contains_topic(self, tmp_path):
        path = write_articles("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        assert "AI" in os.path.basename(path)

    def test_filename_ends_with_articles(self, tmp_path):
        path = write_articles("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        assert os.path.basename(path).endswith("_articles.md")

    def test_contains_article_titles(self, tmp_path):
        path = write_articles("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        content = open(path, encoding="utf-8").read()
        assert "AI Breaks New Ground in 2025" in content
        assert "Open Source Models Catching Up" in content

    def test_contains_sources(self, tmp_path):
        path = write_articles("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        content = open(path, encoding="utf-8").read()
        assert "Tech News Daily" in content

    def test_contains_links(self, tmp_path):
        path = write_articles("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        content = open(path, encoding="utf-8").read()
        assert "https://example.com/ai-breaks-ground" in content

    def test_contains_cleaned_text(self, tmp_path):
        path = write_articles("AI", FAKE_ARTICLES, output_dir=str(tmp_path))
        content = open(path, encoding="utf-8").read()
        assert "narrowed the gap with closed models" in content
        assert "improved reasoning benchmarks" in content

    def test_does_not_require_summary(self, tmp_path):
        # articles file uses cleaned_text, not summary — this should not raise
        articles_no_summary = [
            {
                "title": "Test Article",
                "source": "Test Source",
                "published_date": "2025-04-01",
                "url": "https://example.com/test",
                "cleaned_text": "This is the cleaned body text.",
            }
        ]
        path = write_articles("AI", articles_no_summary, output_dir=str(tmp_path))
        content = open(path, encoding="utf-8").read()
        assert "cleaned body text" in content

    def test_empty_articles_list(self, tmp_path):
        path = write_articles("AI", [], output_dir=str(tmp_path))
        assert os.path.isfile(path)
