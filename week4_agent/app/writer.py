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
    today = date.today().isoformat()
    filename = f"{topic}_{today}_digest.md"
    filepath = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    lines = [
        f"# News Digest: {topic}",
        f"",
        f"**Generated:** {today}  ",
        f"**Articles:** {len(articles)}",
        f"",
        f"---",
        f"",
    ]

    for article in articles:
        lines += [
            f"## {article.get('title', 'Untitled')}",
            f"",
            f"**Source:** {article.get('source', 'Unknown')}  ",
            f"**Date:** {article.get('published_date', 'Unknown')}  ",
            f"**Link:** {article.get('url', '')}",
            f"",
            f"### Summary",
            f"",
            f"{article.get('summary', '')}",
            f"",
            f"---",
            f"",
        ]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filepath


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
    today = date.today().isoformat()
    filename = f"{topic}_{today}_articles.md"
    filepath = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    lines = [
        f"# Articles: {topic}",
        f"",
        f"**Generated:** {today}  ",
        f"**Articles:** {len(articles)}",
        f"",
        f"---",
        f"",
    ]

    for article in articles:
        lines += [
            f"## {article.get('title', 'Untitled')}",
            f"",
            f"**Source:** {article.get('source', 'Unknown')}  ",
            f"**Date:** {article.get('published_date', 'Unknown')}  ",
            f"**Link:** {article.get('url', '')}",
            f"",
            f"### Content",
            f"",
            f"{article.get('cleaned_text', '')}",
            f"",
            f"---",
            f"",
        ]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filepath
