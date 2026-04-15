"""
search.py — Search for news articles related to a topic.

Responsibilities:
- Accept a topic string.
- Return a list of article metadata dicts, each containing:
    title, url, source, published_date.

Implementation note:
    Two-layer design (mirrors fetch.py):
    - parse_rss(xml_text): pure function, parses Google News RSS XML into
      a list of article metadata dicts. Testable without network access.
    - search_articles(topic): thin HTTP layer, fetches the RSS feed and
      delegates to parse_rss(). Network calls can be mocked in tests.

    Search source: Google News RSS (free, no API key required).
    Uses Python standard library only (urllib, xml.etree.ElementTree, html.parser).

    URL extraction strategy:
    Google News RSS <link> elements are redirect URLs that require JavaScript
    to resolve to the real article. The real publisher URL is embedded as the
    href of the first <a> tag inside the <description> HTML fragment.
    parse_rss() prefers that href; falls back to <link> if not found.
"""

from html.parser import HTMLParser
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET


class _FirstHrefParser(HTMLParser):
    """Find the href of the first <a> tag in an HTML fragment."""

    def __init__(self):
        super().__init__()
        self.href = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a" and not self.href:
            for name, value in attrs:
                if name == "href" and value:
                    self.href = value
                    break


def _extract_url_from_description(description_html: str) -> str:
    """Return the href of the first <a> tag in description_html, or ''.

    Args:
        description_html: HTML string from a Google News RSS <description> element.

    Returns:
        The first href found, or "" if none exists.
    """
    if not description_html:
        return ""
    parser = _FirstHrefParser()
    parser.feed(description_html)
    return parser.href


def parse_rss(xml_text: str) -> list[dict]:
    """Parse Google News RSS XML and return a list of article metadata dicts.

    Each dict contains: title, url, source, published_date.
    Items missing both title and url are skipped.
    Returns [] if xml_text is empty, unparseable, or contains no valid items.

    Args:
        xml_text: Raw RSS XML string.

    Returns:
        List of article metadata dicts, possibly empty.
    """
    if not xml_text or not xml_text.strip():
        return []

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []

    channel = root.find("channel")
    if channel is None:
        return []

    results = []
    for item in channel.findall("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        source_el = item.find("source")
        pubdate_el = item.find("pubDate")
        description_el = item.find("description")

        title = (title_el.text or "").strip() if title_el is not None else ""
        link_url = (link_el.text or "").strip() if link_el is not None else ""
        description_html = (description_el.text or "") if description_el is not None else ""
        url = _extract_url_from_description(description_html) or link_url
        source = (source_el.text or "").strip() if source_el is not None else ""
        published_date = (pubdate_el.text or "").strip() or None if pubdate_el is not None else None

        if not (title and url):
            continue

        results.append({
            "title": title,
            "url": url,
            "source": source,
            "published_date": published_date,
        })

    return results


def search_articles(topic: str, max_results: int = 5) -> list[dict]:
    """Search Google News RSS for articles related to topic.

    Returns up to max_results article metadata dicts.
    Returns [] on any network or HTTP error (best-effort, not strict).

    Args:
        topic: The topic to search for.
        max_results: Maximum number of articles to return.

    Returns:
        A list of dicts with keys: title, url, source, published_date.
    """
    query = urllib.parse.quote(topic)
    rss_url = (
        f"https://news.google.com/rss/search"
        f"?q={query}&hl=en-US&gl=US&ceid=US:en"
    )

    try:
        req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_text = response.read().decode("utf-8", errors="replace")
        return parse_rss(xml_text)[:max_results]
    except (urllib.error.URLError, OSError):
        return []
