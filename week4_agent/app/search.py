"""
search.py — Search for news articles related to a topic.

Responsibilities:
- Accept a topic string.
- Return a list of article metadata dicts, each containing:
    - title (str)
    - url (str)
    - source (str)
    - published_date (str or None)
"""


def search_articles(topic: str, max_results: int = 5) -> list[dict]:
    """Search for news articles related to the given topic.

    Args:
        topic: The topic to search for.
        max_results: Maximum number of articles to return.

    Returns:
        A list of dicts with keys: title, url, source, published_date.
    """
    # TODO: implement search using a news API or web search
    raise NotImplementedError
