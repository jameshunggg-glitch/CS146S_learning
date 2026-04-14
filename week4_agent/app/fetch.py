"""
fetch.py — Fetch article content from a URL.

Responsibilities:
- Accept an article URL.
- Return the raw text body of the article (best-effort extraction).
"""


def fetch_article(url: str) -> str:
    """Fetch and return the raw text content of an article.

    Args:
        url: The URL of the article to fetch.

    Returns:
        Raw text content as a string. May contain noise; cleaned later by clean.py.
    """
    # TODO: implement HTTP fetch + basic text extraction
    raise NotImplementedError
