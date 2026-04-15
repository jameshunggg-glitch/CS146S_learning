"""
main.py — CLI entry point for the AI News Digest tool.

Usage:
    python -m app.main --topic "AI"

Real pipeline:
    1. Accept a topic from the command line.
    2. Search for articles with search_articles(topic).
    3. Fetch each article's content with fetch_article(url).
    4. Clean the raw text with clean_text().
    5. Generate a short summary with summarize().
    6. Write digest and articles Markdown files to output/.

Failure handling:
    - No search results → print message and exit.
    - Individual fetch failure or empty content → skip that article.
    - All articles unusable after fetching → print message and exit without
      writing empty files.
"""

import argparse
import sys

from app.search import search_articles
from app.fetch import fetch_article
from app.clean import clean_text
from app.summarize import summarize
from app.writer import write_digest, write_articles


def run_pipeline(topic: str) -> int:
    """Run the full search → fetch → clean → summarize → write pipeline.

    Returns 0 on success, 1 if nothing could be written.
    Separated from main() to make the pipeline logic testable without
    sys.exit or argparse.
    """
    print(f"Topic: {topic}")

    # --- Search ---
    articles_meta = search_articles(topic)
    if not articles_meta:
        print("No articles found. Try a different topic.")
        return 1

    print(f"Found {len(articles_meta)} article(s). Fetching content...")

    # --- Fetch / clean / summarize ---
    digest_articles = []
    full_articles = []

    for meta in articles_meta:
        url = meta["url"]
        raw_text = fetch_article(url)

        if not raw_text:
            print(f"  Skip (fetch failed):  {meta['title']}")
            continue

        cleaned = clean_text(raw_text)
        if not cleaned:
            print(f"  Skip (empty content): {meta['title']}")
            continue

        summary = summarize(cleaned)

        base = {
            "title": meta["title"],
            "source": meta["source"],
            "published_date": meta["published_date"],
            "url": url,
        }
        digest_articles.append({**base, "summary": summary})
        full_articles.append({**base, "cleaned_text": cleaned})
        print(f"  OK: {meta['title']}")

    # --- Write ---
    if not digest_articles:
        print("No usable articles after fetching. Nothing written.")
        return 1

    digest_path = write_digest(topic, digest_articles)
    articles_path = write_articles(topic, full_articles)

    print(f"Digest:   {digest_path}")
    print(f"Articles: {articles_path}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="AI News Digest tool")
    parser.add_argument("--topic", required=True, help="Topic to search for")
    args = parser.parse_args()

    sys.exit(run_pipeline(args.topic))


if __name__ == "__main__":
    main()
