# week3/tools/geocoding.py

from __future__ import annotations

import logging
from typing import Any

import requests

from week3.utils.validators import (
    validate_count,
    validate_language,
    validate_query,
)

logger = logging.getLogger(__name__)

GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
REQUEST_TIMEOUT_SECONDS = 10


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

    params = {
        "name": query,
        "count": count,
        "language": language,
        "format": "json",
    }

    try:
        logger.info(
            "Calling geocoding API | query=%r count=%s language=%s",
            query,
            count,
            language,
        )

        response = requests.get(
            GEOCODING_API_URL,
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()

    except requests.Timeout:
        logger.exception("Geocoding API timeout")
        return {
            "status": "error",
            "error_type": "timeout_error",
            "message": "The geocoding request timed out.",
        }

    except requests.HTTPError:
        logger.exception("Geocoding API returned HTTP error")

        message = "The geocoding API returned an HTTP error."
        try:
            error_payload = response.json()
            if isinstance(error_payload, dict) and error_payload.get("reason"):
                message = str(error_payload["reason"])
        except Exception:
            pass

        return {
            "status": "error",
            "error_type": "api_error",
            "message": message,
        }

    except requests.RequestException:
        logger.exception("Geocoding API request failed")
        return {
            "status": "error",
            "error_type": "api_error",
            "message": "Failed to connect to the geocoding API.",
        }

    except ValueError:
        logger.exception("Failed to decode geocoding API JSON response")
        return {
            "status": "error",
            "error_type": "unexpected_error",
            "message": "The geocoding API returned invalid JSON.",
        }

    results = payload.get("results", [])
    if not results:
        return {
            "status": "error",
            "error_type": "not_found",
            "message": f"No locations found for query: {query}",
        }

    formatted_results = [_format_location_result(item) for item in results]

    return {
        "status": "ok",
        "data": {
            "query": query,
            "result_count": len(formatted_results),
            "results": formatted_results,
        },
    }


def _format_location_result(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": item.get("name"),
        "country": item.get("country"),
        "country_code": item.get("country_code"),
        "admin1": item.get("admin1"),
        "admin2": item.get("admin2"),
        "latitude": item.get("latitude"),
        "longitude": item.get("longitude"),
        "timezone": item.get("timezone"),
    }