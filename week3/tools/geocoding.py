# week3/tools/geocoding.py

from __future__ import annotations

from week3.utils.validators import (
    validate_count,
    validate_language,
    validate_query,
)


def search_location(query: str, count: int = 5, language: str = "en") -> dict:
    try:
        query = validate_query(query)
        count = validate_count(count)
        language = validate_language(language)
    except ValueError as exc:
        return {
            "status": "error",
            "error_type": "validation_error",
            "message": str(exc),
        }

    return {
        "status": "ok",
        "data": {
            "query": query,
            "count": count,
            "language": language,
            "results": [],
        },
    }