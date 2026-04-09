from urllib.parse import quote_plus

import feedparser

from app.models import ArticleCandidate


GOOGLE_NEWS_RSS_BASE_URL = "https://news.google.com/rss/search"
GOOGLE_NEWS_HL = "en-US"
GOOGLE_NEWS_GL = "US"
GOOGLE_NEWS_CEID = "US:en"

DEFAULT_TITLE = "Untitled"
DEFAULT_URL = ""
DEFAULT_SOURCE = "Unknown source"
DEFAULT_PUBLISHED_DATE = "Unknown date"
DEFAULT_NOTE = "Fetched from Google News RSS"


def _build_google_news_rss_url(topic: str) -> str:
    encoded_topic = quote_plus(topic)
    return (
        f"{GOOGLE_NEWS_RSS_BASE_URL}"
        f"?q={encoded_topic}"
        f"&hl={GOOGLE_NEWS_HL}"
        f"&gl={GOOGLE_NEWS_GL}"
        f"&ceid={GOOGLE_NEWS_CEID}"
    )


def _fetch_google_news_feed(topic: str):
    rss_url = _build_google_news_rss_url(topic)
    return feedparser.parse(rss_url)


def _extract_title(entry) -> str:
    return getattr(entry, "title", DEFAULT_TITLE)


def _extract_url(entry) -> str:
    return getattr(entry, "link", DEFAULT_URL)


def _extract_published_date(entry) -> str:
    return getattr(entry, "published", DEFAULT_PUBLISHED_DATE)


def _extract_source(entry) -> str:
    if hasattr(entry, "source") and isinstance(entry.source, dict):
        return entry.source.get("title", DEFAULT_SOURCE)
    return DEFAULT_SOURCE


def _entry_to_candidate(entry, note: str = DEFAULT_NOTE) -> ArticleCandidate:
    return ArticleCandidate(
        title=_extract_title(entry),
        url=_extract_url(entry),
        source=_extract_source(entry),
        published_date=_extract_published_date(entry),
        note=note,
    )


def search_news(topic: str, max_results: int = 3) -> list[ArticleCandidate]:
    feed = _fetch_google_news_feed(topic)

    if getattr(feed, "bozo", False) and not getattr(feed, "entries", []):
        return []

    candidates: list[ArticleCandidate] = []
    skipped_entries = 0

    for entry in feed.entries[:max_results]:
        try:
            candidate = _entry_to_candidate(entry)
            candidates.append(candidate)
        except Exception:
            skipped_entries += 1
            continue

    if skipped_entries > 0:
        for candidate in candidates:
            candidate.note = f"{DEFAULT_NOTE} | skipped_entries={skipped_entries}"

    return candidates