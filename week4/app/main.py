from pathlib import Path

from app.search import search_news
from app.summarizer import summarize_article
from app.writer import write_digest_file


def run() -> None:
    topic = "AI"
    max_results = 3
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    candidates = search_news(topic, max_results=max_results)

    for index, candidate in enumerate(candidates, start=1):
        digest = summarize_article(candidate)
        output_file = output_dir / f"{index:03d}.md"
        write_digest_file(digest, str(output_file))

    print(f"Done. Wrote {len(candidates)} digest files to {output_dir.resolve()}")


if __name__ == "__main__":
    run()