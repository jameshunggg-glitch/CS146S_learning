"""
test_search.py — Tests for app/search.py.

Covers:
- parse_rss(): pure function tests against RSS XML strings (no network).
- search_articles(): mock-based tests for the HTTP layer (no real requests).
"""

import urllib.error
from unittest.mock import patch, MagicMock

from app.search import parse_rss, search_articles


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_rss(items: list[dict]) -> str:
    """Build a minimal RSS XML string from a list of item dicts."""
    item_blocks = []
    for it in items:
        block = "<item>"
        if "title" in it:
            block += f"<title>{it['title']}</title>"
        if "link" in it:
            block += f"<link>{it['link']}</link>"
        if "source" in it:
            block += f"<source>{it['source']}</source>"
        if "pubDate" in it:
            block += f"<pubDate>{it['pubDate']}</pubDate>"
        block += "</item>"
        item_blocks.append(block)

    items_xml = "".join(item_blocks)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<rss version="2.0"><channel>{items_xml}</channel></rss>'
    )


def _make_mock_response(xml: str) -> MagicMock:
    """Build a mock compatible with urllib.request.urlopen as a context manager."""
    mock = MagicMock()
    mock.read.return_value = xml.encode("utf-8")
    mock.__enter__ = lambda s: s
    mock.__exit__ = MagicMock(return_value=False)
    return mock


SAMPLE_RSS = _make_rss([
    {
        "title": "AI Breakthrough in 2025",
        "link": "https://news.google.com/rss/articles/abc123",
        "source": "Tech Daily",
        "pubDate": "Thu, 10 Apr 2025 12:00:00 GMT",
    },
    {
        "title": "Open Source Models Compete",
        "link": "https://news.google.com/rss/articles/def456",
        "source": "AI Weekly",
        "pubDate": "Fri, 11 Apr 2025 09:00:00 GMT",
    },
])


# ---------------------------------------------------------------------------
# parse_rss — pure function tests
# ---------------------------------------------------------------------------

def test_parse_returns_list():
    assert isinstance(parse_rss(SAMPLE_RSS), list)


def test_parse_correct_count():
    assert len(parse_rss(SAMPLE_RSS)) == 2


def test_parse_result_has_required_keys():
    result = parse_rss(SAMPLE_RSS)[0]
    assert "title" in result
    assert "url" in result
    assert "source" in result
    assert "published_date" in result


def test_parse_correct_title():
    assert parse_rss(SAMPLE_RSS)[0]["title"] == "AI Breakthrough in 2025"


def test_parse_correct_url():
    assert parse_rss(SAMPLE_RSS)[0]["url"] == "https://news.google.com/rss/articles/abc123"


def test_parse_correct_source():
    assert parse_rss(SAMPLE_RSS)[0]["source"] == "Tech Daily"


def test_parse_correct_published_date():
    assert parse_rss(SAMPLE_RSS)[0]["published_date"] == "Thu, 10 Apr 2025 12:00:00 GMT"


def test_parse_empty_string_returns_empty():
    assert parse_rss("") == []


def test_parse_invalid_xml_returns_empty():
    assert parse_rss("not valid xml <<>>") == []


def test_parse_no_items_returns_empty():
    xml = '<?xml version="1.0"?><rss version="2.0"><channel></channel></rss>'
    assert parse_rss(xml) == []


def test_parse_skips_items_without_title_and_url():
    # An item with only source/pubDate and no title+url should be dropped.
    xml = _make_rss([{"source": "Orphan Source", "pubDate": "Mon, 01 Jan 2025 00:00:00 GMT"}])
    assert parse_rss(xml) == []


# ---------------------------------------------------------------------------
# search_articles — mock-based HTTP tests
# ---------------------------------------------------------------------------

def test_search_returns_list():
    with patch("urllib.request.urlopen", return_value=_make_mock_response(SAMPLE_RSS)):
        result = search_articles("AI")
    assert isinstance(result, list)


def test_search_returns_correct_results():
    with patch("urllib.request.urlopen", return_value=_make_mock_response(SAMPLE_RSS)):
        result = search_articles("AI")
    assert len(result) == 2
    assert result[0]["title"] == "AI Breakthrough in 2025"


def test_search_respects_max_results():
    # Feed has 2 items; request only 1.
    with patch("urllib.request.urlopen", return_value=_make_mock_response(SAMPLE_RSS)):
        result = search_articles("AI", max_results=1)
    assert len(result) == 1


def test_search_returns_empty_on_url_error():
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("refused")):
        assert search_articles("AI") == []


def test_search_returns_empty_on_http_error():
    err = urllib.error.HTTPError(
        url="https://news.google.com/rss/search",
        code=429,
        msg="Too Many Requests",
        hdrs=None,
        fp=None,
    )
    with patch("urllib.request.urlopen", side_effect=err):
        assert search_articles("AI") == []
