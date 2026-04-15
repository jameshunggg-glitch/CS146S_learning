"""
main.py — CLI entry point for the AI News Digest tool.

Usage:
    python main.py --topic "AI"

Pipeline (fake-data MVP):
    1. Accept a topic from the command line.
    2. Load a small set of fake articles (stand-in for real search + fetch).
    3. Clean each article's raw text using clean_text().
    4. Attach a placeholder summary (stand-in for real summarization).
    5. Write digest and articles Markdown files to output/.
"""

import argparse
from app.clean import clean_text
from app.writer import write_digest, write_articles


# ---------------------------------------------------------------------------
# Fake article data — replaces real search + fetch for the MVP
# ---------------------------------------------------------------------------

FAKE_ARTICLES = [
    {
        "title": "AI Reasoning Models Reach New Milestone",
        "source": "Tech News Daily",
        "published_date": "2025-04-10",
        "url": "https://example.com/ai-reasoning-milestone",
        "raw_text": (
            "AI reasoning systems made significant strides in early 2025.\n"
            "Several leading labs reported improvements in multi-step problem solving.\n"
            "Continue reading\n"
            "The gains were most visible in mathematical and scientific benchmarks.\n"
            "Advertisement\n"
            "Researchers noted that model scaling alone no longer explains the improvements.\n"
        ),
        "summary": "AI reasoning models hit a new milestone in 2025, with gains in multi-step problem solving and scientific benchmarks.",
    },
    {
        "title": "Open Source Models Close the Gap",
        "source": "Open AI Weekly",
        "published_date": "2025-04-11",
        "url": "https://example.com/open-source-gap",
        "raw_text": (
            "A wave of open source model releases in early 2025 surprised the industry.\n"
            "Subscribe\n"
            "Performance on standard benchmarks narrowed the gap with proprietary alternatives.\n"
            "Sign up\n"
            "Community fine-tuning contributed to several unexpected capability jumps.\n"
            "Read more\n"
        ),
        "summary": "Open source models became competitive with closed alternatives in 2025, driven by community fine-tuning and new releases.",
    },
]


def build_articles(topic: str) -> tuple[list[dict], list[dict]]:
    """Clean raw text and prepare two article lists for the writer.

    Returns:
        digest_articles: list of dicts with title, source, published_date, url, summary.
        full_articles:   list of dicts with title, source, published_date, url, cleaned_text.
    """
    digest_articles = []
    full_articles = []

    for article in FAKE_ARTICLES:
        cleaned = clean_text(article["raw_text"])

        base = {
            "title": article["title"],
            "source": article["source"],
            "published_date": article["published_date"],
            "url": article["url"],
        }

        digest_articles.append({**base, "summary": article["summary"]})
        full_articles.append({**base, "cleaned_text": cleaned})

    return digest_articles, full_articles


def main():
    parser = argparse.ArgumentParser(description="AI News Digest tool")
    parser.add_argument("--topic", required=True, help="Topic to search for")
    args = parser.parse_args()

    topic = args.topic
    print(f"Topic: {topic}")
    print(f"Articles: {len(FAKE_ARTICLES)} (fake data)")

    digest_articles, full_articles = build_articles(topic)

    digest_path = write_digest(topic, digest_articles)
    articles_path = write_articles(topic, full_articles)

    print(f"Digest:   {digest_path}")
    print(f"Articles: {articles_path}")


if __name__ == "__main__":
    main()
