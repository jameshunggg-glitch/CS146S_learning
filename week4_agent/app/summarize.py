"""
summarize.py — Generate a short summary for a cleaned article.

Responsibilities:
- Accept cleaned article text.
- Return a short summary (up to 3 sentences extracted from the text).

Implementation note:
    This is an extractive summarizer: it picks the first few meaningful
    sentences from the cleaned text. No network calls or LLM required.
    Replace with a Claude API call when ready for real summarization.
"""

_MIN_LINE_LEN = 20   # characters; shorter lines are skipped as noise
_MAX_SENTENCES = 3   # how many sentences to include in the summary


def summarize(text: str) -> str:
    """Return a short extractive summary of the given cleaned article text.

    Picks the first up to 3 lines that are long enough to be real sentences.
    Returns an empty string if no suitable lines are found.

    Args:
        text: Cleaned article text (output of clean_text()).

    Returns:
        A short summary string, or "" if the text has no usable content.
    """
    if not text:
        return ""

    lines = text.splitlines()
    sentences = [line.strip() for line in lines if len(line.strip()) >= _MIN_LINE_LEN]
    selected = sentences[:_MAX_SENTENCES]

    return " ".join(selected)
