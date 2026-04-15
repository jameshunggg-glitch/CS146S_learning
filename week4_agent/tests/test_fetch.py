"""
test_fetch.py — Tests for app/fetch.py.

Covers:
- extract_text(): pure function tests against HTML strings (no network).
- fetch_article(): mock-based tests for the HTTP layer (no real requests).
"""

import urllib.error
from unittest.mock import patch, MagicMock

from app.fetch import extract_text, fetch_article


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _make_mock_response(html: str, encoding: str = "utf-8") -> MagicMock:
    """Build a mock compatible with urllib.request.urlopen used as a context manager."""
    mock = MagicMock()
    mock.read.return_value = html.encode(encoding)
    mock.headers.get_content_charset.return_value = encoding
    mock.__enter__ = lambda s: s
    mock.__exit__ = MagicMock(return_value=False)
    return mock


# ---------------------------------------------------------------------------
# extract_text — pure function tests
# ---------------------------------------------------------------------------

def test_extract_returns_string():
    assert isinstance(extract_text("<p>Hello</p>"), str)


def test_extract_removes_html_tags():
    result = extract_text("<p>Hello world.</p>")
    assert "<p>" not in result
    assert "Hello world." in result


def test_extract_normal_article_html():
    html = (
        "<html><body>"
        "<h1>Article Title</h1>"
        "<p>First paragraph of the article.</p>"
        "<p>Second paragraph with more content.</p>"
        "</body></html>"
    )
    result = extract_text(html)
    assert "Article Title" in result
    assert "First paragraph" in result
    assert "Second paragraph" in result


def test_extract_excludes_script_content():
    html = "<html><body><script>alert('bad');</script><p>Good content.</p></body></html>"
    result = extract_text(html)
    assert "alert" not in result
    assert "Good content." in result


def test_extract_excludes_style_content():
    html = (
        "<html><head><style>body { color: red; }</style></head>"
        "<body><p>Article text.</p></body></html>"
    )
    result = extract_text(html)
    assert "color" not in result
    assert "Article text." in result


def test_extract_empty_string_returns_empty():
    assert extract_text("") == ""


def test_extract_whitespace_only_returns_empty():
    assert extract_text("   \n   ") == ""


def test_extract_tags_only_returns_empty():
    assert extract_text("<html><body></body></html>") == ""


def test_extract_produces_one_node_per_line():
    html = "<p>Line one.</p><p>Line two.</p>"
    lines = extract_text(html).splitlines()
    assert "Line one." in lines
    assert "Line two." in lines


def test_extract_handles_html_entities():
    # HTMLParser decodes entities automatically.
    html = "<p>AT&amp;T sells phones.</p>"
    result = extract_text(html)
    assert "AT&T" in result


# ---------------------------------------------------------------------------
# fetch_article — mock-based HTTP tests
# ---------------------------------------------------------------------------

def test_fetch_returns_text_for_successful_response():
    html = "<html><body><p>This is the article content we fetched.</p></body></html>"
    with patch("urllib.request.urlopen", return_value=_make_mock_response(html)):
        result = fetch_article("https://example.com/article")
    assert "article content" in result


def test_fetch_strips_html_tags():
    html = "<html><body><h1>Title</h1><p>Body text here.</p></body></html>"
    with patch("urllib.request.urlopen", return_value=_make_mock_response(html)):
        result = fetch_article("https://example.com/article")
    assert "<h1>" not in result
    assert "Title" in result
    assert "Body text here." in result


def test_fetch_returns_string_type():
    html = "<p>Some content that is returned.</p>"
    with patch("urllib.request.urlopen", return_value=_make_mock_response(html)):
        result = fetch_article("https://example.com")
    assert isinstance(result, str)


def test_fetch_returns_empty_on_url_error():
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("refused")):
        result = fetch_article("https://example.com/article")
    assert result == ""


def test_fetch_returns_empty_on_http_error():
    err = urllib.error.HTTPError(
        url="https://example.com/article",
        code=404,
        msg="Not Found",
        hdrs=None,
        fp=None,
    )
    with patch("urllib.request.urlopen", side_effect=err):
        result = fetch_article("https://example.com/article")
    assert result == ""


def test_fetch_sends_user_agent_header():
    # Confirm that fetch_article() includes a User-Agent header in the request,
    # so real websites don't reject it as a bare urllib call.
    html = "<p>Content.</p>"
    with patch("urllib.request.urlopen", return_value=_make_mock_response(html)) as mock_open:
        fetch_article("https://example.com/article")
    request_arg = mock_open.call_args[0][0]
    assert request_arg.get_header("User-agent") == "Mozilla/5.0"
