from pathlib import Path

from app.search import search_news
from app.summarizer import summarize_article
from app.writer import write_digest_file


def run(topic: str = "AI", max_results: int = 3, output_dir: str = "outputs") -> None:
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    candidates = search_news(topic, max_results=max_results)

    for index, candidate in enumerate(candidates, start=1):
        digest = summarize_article(candidate)
        output_file = output_path / f"{index:03d}.md"
        write_digest_file(digest, str(output_file))

    print(f"Done. Wrote {len(candidates)} digest files to {output_path.resolve()}")


if __name__ == "__main__":
    run()