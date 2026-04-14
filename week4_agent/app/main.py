"""
main.py — CLI entry point for the AI News Digest tool.

Usage:
    python main.py --topic "AI"

Pipeline:
    1. Search for news articles on the given topic.
    2. Fetch content from each article URL.
    3. Clean the raw article text.
    4. Summarize each cleaned article.
    5. Write digest and articles Markdown files to output/.
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="AI News Digest tool")
    parser.add_argument("--topic", required=True, help="Topic to search for")
    args = parser.parse_args()

    topic = args.topic
    print(f"Topic: {topic}")
    # TODO: wire up search → fetch → clean → summarize → write


if __name__ == "__main__":
    main()
