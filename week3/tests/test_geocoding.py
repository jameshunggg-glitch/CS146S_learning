# week3/tests/test_geocoding.py

from __future__ import annotations

from unittest.mock import Mock, patch

import requests

from week3.tools.geocoding import search_location


def test_search_location_returns_validation_error_for_empty_query() -> None:
    result = search_location(query="   ", count=5, language="en")

    assert result["status"] == "error"
    assert result["error_type"] == "validation_error"
    assert "query cannot be empty" in result["message"]


@patch("week3.tools.geocoding.requests.get")
def test_search_location_returns_formatted_results_on_success(
    mock_get: Mock,
) -> None:
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [
            {
                "name": "Taipei",
                "country": "Taiwan",
                "country_code": "TW",
                "admin1": "Taipei City",
                "admin2": None,
                "latitude": 25.0330,
                "longitude": 121.5654,
                "timezone": "Asia/Taipei",
            }
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = search_location(query="Taipei", count=3, language="en")

    assert result["status"] == "ok"
    assert result["data"]["query"] == "Taipei"
    assert result["data"]["result_count"] == 1
    assert len(result["data"]["results"]) == 1

    first = result["data"]["results"][0]
    assert first["name"] == "Taipei"
    assert first["country"] == "Taiwan"
    assert first["country_code"] == "TW"
    assert first["admin1"] == "Taipei City"
    assert first["latitude"] == 25.0330
    assert first["longitude"] == 121.5654
    assert first["timezone"] == "Asia/Taipei"

    mock_get.assert_called_once()
    _, kwargs = mock_get.call_args
    assert kwargs["params"]["name"] == "Taipei"
    assert kwargs["params"]["count"] == 3
    assert kwargs["params"]["language"] == "en"


@patch("week3.tools.geocoding.requests.get")
def test_search_location_returns_not_found_when_results_empty(
    mock_get: Mock,
) -> None:
    mock_response = Mock()
    mock_response.json.return_value = {"results": []}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = search_location(query="some-unknown-place", count=5, language="en")

    assert result["status"] == "error"
    assert result["error_type"] == "not_found"
    assert "No locations found" in result["message"]


@patch("week3.tools.geocoding.requests.get")
def test_search_location_returns_timeout_error_on_timeout(
    mock_get: Mock,
) -> None:
    mock_get.side_effect = requests.Timeout

    result = search_location(query="Taipei", count=5, language="en")

    assert result["status"] == "error"
    assert result["error_type"] == "timeout_error"
    assert "timed out" in result["message"]


@patch("week3.tools.geocoding.requests.get")
def test_search_location_returns_api_error_on_request_exception(
    mock_get: Mock,
) -> None:
    mock_get.side_effect = requests.RequestException

    result = search_location(query="Taipei", count=5, language="en")

    assert result["status"] == "error"
    assert result["error_type"] == "api_error"
    assert "Failed to connect" in result["message"]


@patch("week3.tools.geocoding.requests.get")
def test_search_location_returns_api_error_on_http_error_with_reason(
    mock_get: Mock,
) -> None:
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError
    mock_response.json.return_value = {
        "error": True,
        "reason": "Invalid language parameter",
    }
    mock_get.return_value = mock_response

    result = search_location(query="Taipei", count=5, language="en")

    assert result["status"] == "error"
    assert result["error_type"] == "api_error"
    assert result["message"] == "Invalid language parameter"


@patch("week3.tools.geocoding.requests.get")
def test_search_location_returns_unexpected_error_for_invalid_json(
    mock_get: Mock,
) -> None:
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("invalid json")
    mock_get.return_value = mock_response

    result = search_location(query="Taipei", count=5, language="en")

    assert result["status"] == "error"
    assert result["error_type"] == "unexpected_error"
    assert "invalid JSON" in result["message"]