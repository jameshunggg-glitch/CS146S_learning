from pathlib import Path

from app.models import ArticleDigest
from app.writer import write_digest_file

digest = ArticleDigest(
    title="Test News",
    url="https://example.com",
    source="BBC",
    published_date="2026-04-08",
    extraction_status="Success",
    summary="This is a short summary.",
    key_points=[
        "Point one",
        "Point two",
    ],
    warnings=[
        "Paywall not checked",
    ],
)

write_digest_file(digest, "test_output.md")

print("File written successfully.")
print("Current working directory:", Path.cwd())
print("Expected file path:", Path("test_output.md").resolve())
print("File exists:", Path("test_output.md").exists())