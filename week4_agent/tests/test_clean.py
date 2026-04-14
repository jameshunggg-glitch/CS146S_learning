"""
test_clean.py — Tests for app/clean.py.

Covers:
- Removing common noise strings (e.g. "Continue reading").
- Collapsing excessive blank lines.
- Preserving normal article content.
- Removing obviously meaningless short lines.
"""

from app.clean import clean_text


# ---------------------------------------------------------------------------
# Noise phrase removal
# ---------------------------------------------------------------------------

def test_removes_continue_reading():
    text = "Some article text.\nContinue reading\nMore article text."
    result = clean_text(text)
    assert "Continue reading" not in result
    assert "Some article text." in result
    assert "More article text." in result


def test_removes_all_noise_phrases():
    noise_lines = [
        "Continue reading",
        "Read more",
        "Subscribe",
        "Sign up",
        "Advertisement",
    ]
    for phrase in noise_lines:
        text = f"Before.\n{phrase}\nAfter."
        result = clean_text(text)
        assert phrase not in result, f"Expected '{phrase}' to be removed"


def test_noise_removal_is_case_insensitive():
    text = "Intro.\ncontinue reading\nBody text."
    result = clean_text(text)
    assert "continue reading" not in result.lower()


# ---------------------------------------------------------------------------
# Excessive blank lines
# ---------------------------------------------------------------------------

def test_collapses_multiple_blank_lines():
    text = "First paragraph.\n\n\n\nSecond paragraph."
    result = clean_text(text)
    assert "\n\n\n" not in result  # no triple blank lines
    assert "First paragraph." in result
    assert "Second paragraph." in result


def test_single_blank_line_preserved():
    text = "Line one.\n\nLine two."
    result = clean_text(text)
    assert "Line one." in result
    assert "Line two." in result


# ---------------------------------------------------------------------------
# Short meaningless line removal
# ---------------------------------------------------------------------------

def test_removes_pure_punctuation_lines():
    # Lines with no alphanumeric characters are dropped (UI chrome / dividers).
    for junk in ["-", "---", "***", "|", ">>"]:
        text = f"Real content here.\n{junk}\nMore content."
        result = clean_text(text)
        assert junk not in result.splitlines(), f"Expected '{junk}' to be removed"
        assert "Real content here." in result


def test_keeps_short_alphanumeric_lines():
    # Short lines that contain letters or digits must be preserved.
    for token in ["AI", "Q1", "v2"]:
        text = f"Context.\n{token}\nMore context."
        result = clean_text(text)
        assert token in result, f"Expected '{token}' to be kept"


# ---------------------------------------------------------------------------
# False positives — noise phrases embedded in normal sentences
# ---------------------------------------------------------------------------

def test_does_not_remove_read_more_inside_sentence():
    # "read more" as part of a real sentence should not be removed.
    text = "You can read more about this topic in the full report."
    result = clean_text(text)
    assert text in result


def test_does_not_remove_subscribe_inside_sentence():
    # "subscribe" as part of a real sentence should not be removed.
    text = "Many users subscribe to newsletters to stay informed."
    result = clean_text(text)
    assert text in result


# ---------------------------------------------------------------------------
# Normal content preservation
# ---------------------------------------------------------------------------

def test_preserves_normal_article_content():
    article = (
        "Researchers have announced a major breakthrough in renewable energy.\n"
        "The new solar panels achieve an efficiency of 40 percent.\n"
        "This could dramatically reduce costs for consumers worldwide."
    )
    result = clean_text(article)
    assert result == article


def test_strips_leading_and_trailing_whitespace():
    text = "\n\nSome text.\n\n"
    result = clean_text(text)
    assert not result.startswith("\n")
    assert not result.endswith("\n")
