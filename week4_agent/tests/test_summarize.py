"""
test_summarize.py — Tests for app/summarize.py.

Covers:
- Returning a non-empty string for normal article text.
- Limiting output to at most 3 sentences.
- Skipping lines that are too short to be real sentences.
- Handling empty and whitespace-only input gracefully.
- Preserving content from the first few sentences.
"""

from app.summarize import summarize


# ---------------------------------------------------------------------------
# Basic behaviour
# ---------------------------------------------------------------------------

def test_returns_string():
    text = "This is a reasonably long first sentence about AI research.\n" \
           "It covers several important topics in detail."
    result = summarize(text)
    assert isinstance(result, str)


def test_returns_nonempty_for_normal_text():
    text = (
        "AI reasoning systems made significant strides in early 2025.\n"
        "The gains were most visible in mathematical and scientific benchmarks.\n"
        "Researchers noted that model scaling alone no longer explains the improvements."
    )
    assert summarize(text) != ""


def test_includes_content_from_first_sentence():
    text = (
        "Researchers discovered a new method for solar energy capture.\n"
        "The technique doubles efficiency compared to current panels.\n"
        "Several companies have already expressed interest in licensing it."
    )
    result = summarize(text)
    assert "solar energy" in result


# ---------------------------------------------------------------------------
# Sentence limit
# ---------------------------------------------------------------------------

def test_at_most_three_sentences():
    text = (
        "First long sentence with enough characters to count.\n"
        "Second long sentence with enough characters to count.\n"
        "Third long sentence with enough characters to count.\n"
        "Fourth long sentence that should not appear in the summary.\n"
        "Fifth long sentence that should also not appear in the summary."
    )
    result = summarize(text)
    # Each sentence ends with a period; count how many appear
    parts = result.split(". ")
    assert len(parts) <= 3


def test_does_not_include_fourth_sentence():
    text = (
        "Sentence one is here and has plenty of characters to qualify.\n"
        "Sentence two is here and has plenty of characters to qualify.\n"
        "Sentence three is here and has plenty of characters to qualify.\n"
        "Sentence four should be excluded from the summary output."
    )
    result = summarize(text)
    assert "Sentence four" not in result


# ---------------------------------------------------------------------------
# Short line filtering
# ---------------------------------------------------------------------------

def test_skips_short_lines():
    # Lines shorter than 20 characters should be skipped.
    text = "AI\nShort\nThis is a long enough sentence to be included in the summary."
    result = summarize(text)
    assert "AI" not in result
    assert "Short" not in result
    assert "long enough sentence" in result


def test_short_only_text_returns_empty():
    # If all lines are too short, return "".
    text = "AI\nML\nOK\nYes"
    assert summarize(text) == ""


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_empty_string_returns_empty():
    assert summarize("") == ""


def test_whitespace_only_returns_empty():
    assert summarize("   \n\n   ") == ""


def test_single_long_sentence():
    text = "This is the only sentence and it is long enough to be included."
    result = summarize(text)
    assert "only sentence" in result


def test_does_not_raise_on_mixed_content():
    text = (
        "OK\n"
        "A real sentence that is long enough to pass the filter and appear.\n"
        "Another real sentence that is also long enough for the summarizer.\n"
    )
    result = summarize(text)
    assert "real sentence" in result
