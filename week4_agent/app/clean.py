"""
clean.py — Clean noisy article text.

Responsibilities:
- Remove common noise strings (e.g. "Continue reading", "Subscribe").
- Remove obviously meaningless short lines.
- Collapse excessive blank lines.
- Preserve the main article body.
"""

import re

# Lines that exactly match one of these phrases (case-insensitive, stripped) are dropped.
NOISE_PHRASES = [
    "Continue reading",
    "Read more",
    "Subscribe",
    "Sign up",
    "Advertisement",
]

# A line consisting entirely of these characters (after stripping) is considered
# meaningless UI chrome and is dropped.  Real words like "AI" or "Q1" contain
# alphanumeric characters and therefore pass through.
_PUNCTUATION_ONLY = re.compile(r'^[^\w]+$')

_noise_set = {p.lower() for p in NOISE_PHRASES}


def clean_text(text: str) -> str:
    """Clean raw article text by removing noise and fixing whitespace.

    Cleaning steps (applied in order):
    1. Split into lines.
    2. Drop lines that exactly match a known noise phrase (case-insensitive).
    3. Drop lines that contain no alphanumeric characters (pure punctuation/symbols).
    4. Collapse runs of more than one blank line into a single blank line.
    5. Strip leading/trailing whitespace from the result.

    Args:
        text: Raw article text.

    Returns:
        Cleaned text string.
    """
    lines = text.splitlines()

    kept = []
    for line in lines:
        stripped = line.strip()

        # Rule 1: drop known noise phrases (exact whole-line match, case-insensitive).
        if stripped.lower() in _noise_set:
            continue

        # Rule 2: drop lines that are pure punctuation/symbols with no alphanumeric chars
        # (e.g. "---", "***", "|", ">>").  Empty lines are kept for blank-line collapsing.
        if stripped and _PUNCTUATION_ONLY.match(stripped):
            continue

        kept.append(stripped)

    # Rule 3: collapse consecutive blank lines into one.
    result_lines = []
    prev_blank = False
    for line in kept:
        is_blank = line == ""
        if is_blank and prev_blank:
            continue
        result_lines.append(line)
        prev_blank = is_blank

    return "\n".join(result_lines).strip()
