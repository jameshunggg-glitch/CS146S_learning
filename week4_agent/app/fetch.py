"""
fetch.py — Fetch article content from a URL.

Responsibilities:
- Accept an article URL.
- Return the raw text body of the article (best-effort extraction).

Implementation note:
    Two-layer design:
    - extract_text(html): pure function, strips HTML tags, returns plain text.
      Fully testable without any network access.
    - fetch_article(url): thin HTTP layer, downloads HTML and delegates to
      extract_text(). Network calls can be mocked in tests.

    Uses Python standard library only (urllib, html.parser).
    Returned text may contain noise; clean.py handles that downstream.
"""

from html.parser import HTMLParser
import urllib.request
import urllib.error


# Tags whose text content should be discarded entirely.
_SKIP_TAGS = {"script", "style"}


class _TextExtractor(HTMLParser):
    """Strip HTML tags and collect visible text nodes."""

    def __init__(self):
        super().__init__()
        self._skip = False
        self._parts = []

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP_TAGS:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in _SKIP_TAGS:
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            stripped = data.strip()
            if stripped:
                self._parts.append(stripped)

    def get_text(self) -> str:
        return "\n".join(self._parts)


def extract_text(html: str) -> str:
    """Extract plain text from an HTML string.

    Strips all HTML tags. Discards content inside <script> and <style> blocks.
    Returns one text node per line, with empty/whitespace-only nodes removed.

    Args:
        html: Raw HTML string.

    Returns:
        Plain text string, or "" if html is empty or yields no text.
    """
    if not html:
        return ""
    extractor = _TextExtractor()
    extractor.feed(html)
    return extractor.get_text()


def fetch_article(url: str) -> str:
    """Fetch and return the plain text content of an article at url.

    Downloads the HTML via HTTP GET and extracts plain text with extract_text().
    Returns "" on any network or HTTP error (best-effort, not strict).

    Args:
        url: The URL of the article to fetch.

    Returns:
        Plain text extracted from the page, or "" on failure.
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_bytes = response.read()
            encoding = response.headers.get_content_charset() or "utf-8"
            html = raw_bytes.decode(encoding, errors="replace")
        return extract_text(html)
    except (urllib.error.URLError, OSError):
        return ""
