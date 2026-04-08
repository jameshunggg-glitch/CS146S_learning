from app.models import ArticleDigest


def format_digest_markdown(digest: ArticleDigest) -> str:
    key_points_lines = "\n".join(f"- {point}" for point in digest.key_points)
    warnings_lines = "\n".join(f"- {warning}" for warning in digest.warnings)

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