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
    Uses Python standard library only (urllib, xml.etree.ElementTree).
    Returned URLs are Google News redirect links; fetch.py follows redirects.
"""

import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET


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

        title = (title_el.text or "").strip() if title_el is not None else ""
        url = (link_el.text or "").strip() if link_el is not None else ""
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
