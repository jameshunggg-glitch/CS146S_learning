"""
writer.py — Write Markdown output files.

Responsibilities:
- Write a digest file: quick-reading summary of all articles.
- Write an articles file: cleaned full text of all articles.

Output filenames (relative to output/):
    {topic}_{date}_digest.md
    {topic}_{date}_articles.md
"""

import os
from datetime import date


def write_digest(topic: str, articles: list[dict], output_dir: str = "output") -> str:
    """Write a digest Markdown file for quick reading.

    Each article dict should have:
        title, source, published_date, url, summary

    Args:
        topic: The search topic.
        articles: List of article dicts with summary included.
        output_dir: Directory to write the file into.

    Returns:
        Path of the written file.
    """
    # TODO: implement Markdown digest generation
    raise NotImplementedError


def write_articles(topic: str, articles: list[dict], output_dir: str = "output") -> str:
    """Write an articles Markdown file for knowledge-base storage.

    Each article dict should have:
        title, source, published_date, url, cleaned_text

    Args:
        topic: The search topic.
        articles: List of article dicts with cleaned_text included.
        output_dir: Directory to write the file into.

    Returns:
        Path of the written file.
    """
    # TODO: implement Markdown articles file generation
    raise NotImplementedError
