from app.models import ArticleDigest
from app.writer import format_digest_markdown, write_digest_file


def test_format_digest_markdown_includes_main_sections():
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
        ],
        warnings=[
            "Paywall not checked",
        ],
    )

    markdown = format_digest_markdown(digest)

    assert "# Test News" in markdown
    assert "## Summary" in markdown
    assert "## Key Points" in markdown
    assert "## Warnings" in markdown
    assert "- Point one" in markdown
    assert "- Paywall not checked" in markdown


def test_format_digest_markdown_shows_none_for_empty_lists():
    digest = ArticleDigest(
        title="Empty Case",
        url="https://example.com/empty",
        source="BBC",
        published_date="2026-04-08",
        extraction_status="Success",
        summary="No key points or warnings were extracted.",
    )

    markdown = format_digest_markdown(digest)

    assert "## Key Points" in markdown
    assert "## Warnings" in markdown
    assert "- None" in markdown


def test_write_digest_file_creates_markdown_file(tmp_path):
    digest = ArticleDigest(
        title="Saved News",
        url="https://example.com/saved",
        source="BBC",
        published_date="2026-04-08",
        extraction_status="Success",
        summary="This digest should be written to a file.",
        key_points=[
            "Saved point one",
        ],
        warnings=[
            "Saved warning one",
        ],
    )

    output_file = tmp_path / "saved_news.md"

    write_digest_file(digest, str(output_file))

    assert output_file.exists()

    content = output_file.read_text(encoding="utf-8")
    assert "# Saved News" in content
    assert "## Summary" in content
    assert "- Saved point one" in content
    assert "- Saved warning one" in content