"""
test_integration.py — Small integration test using fake article data.

Verifies that:
- Cleaned text can be passed into the writer.
- Both digest and articles Markdown files are generated successfully.

No live network calls. All data is fake/hardcoded.
"""

import pytest
from app.writer import write_digest, write_articles


# TODO: implement integration test once writer is implemented
