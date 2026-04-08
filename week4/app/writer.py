from pathlib import Path

from app.models import ArticleDigest


def format_digest_markdown(digest: ArticleDigest) -> str:
    if digest.key_points:
        key_points_lines = "\n".join(f"- {point}" for point in digest.key_points)
    else:
        key_points_lines = "- None"

    if digest.warnings:
        warnings_lines = "\n".join(f"- {warning}" for warning in digest.warnings)
    else:
        warnings_lines = "- None"

    markdown = f"""# {digest.title}

- Source: {digest.source}
- Published: {digest.published_date}
- URL: {digest.url}
- Status: {digest.extraction_status}

## Summary
{digest.summary}

## Key Points
{key_points_lines}

## Warnings
{warnings_lines}
"""

    return markdown


def write_digest_file(digest: ArticleDigest, output_path: str) -> None:
    markdown = format_digest_markdown(digest)

    path = Path(output_path)
    path.write_text(markdown, encoding="utf-8")