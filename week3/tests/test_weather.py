# week3/tests/test_weather.py

from __future__ import annotations

from unittest.mock import Mock, patch

import requests

from week3.tools.weather import get_weather_forecast


def test_get_weather_forecast_returns_validation_error_for_invalid_latitude() -> None:
    result = get_weather_forecast(
        latitude=999,
        longitude=121.56,
        timezone="Asia/Taipei",
        forecast_days=3,
        temperature_unit="celsius",
        wind_speed_unit="kmh",
    )

    assert result["status"] == "error"
    assert result["error_type"] == "validation_error"
    assert "latitude must be between -90 and 90" in result["message"]


@patch("week3.tools.weather.requests.get")
def test_get_weather_forecast_returns_formatted_result_on_success(
    mock_get: Mock,
) -> None:
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "latitude": 25.0330,
        "longitude": 121.5654,
        "timezone": "Asia/Taipei",
        "current": {
            "time": "2026-04-02T09:00",
            "temperature_2m": 26.1,
            "wind_speed_10m": 12.3,
            "weather_code": 3,
        },
        "daily": {
            "time": ["2026-04-02", "2026-04-03", "2026-04-04"],
            "weather_code": [3, 61, 2],
            "temperature_2m_max": [28.5, 27.0, 29.1],
            "temperature_2m_min": [22.4, 21.8, 23.0],
            "precipitation_probability_max": [20, 80, 10],
        },
    }
    mock_get.return_value = mock_response

    result = get_weather_forecast(
        latitude=25.0330,
        longitude=121.5654,
        timezone="Asia/Taipei",
        forecast_days=3,
        temperature_unit="celsius",
        wind_speed_unit="kmh",
    )

    assert result["status"] == "ok"

    data = result["data"]
    assert data["location"]["latitude"] == 25.0330
    assert data["location"]["longitude"] == 121.5654
    assert data["location"]["timezone"] == "Asia/Taipei"

    assert data["current"]["time"] == "2026-04-02T09:00"
    assert data["current"]["temperature"] == 26.1
    assert data["current"]["wind_speed"] == 12.3
    assert data["current"]["weather_code"] == 3

    assert len(data["daily_forecast"]) == 3
    assert data["daily_forecast"][0] == {
        "date": "2026-04-02",
        "weather_code": 3,
        "temp_max": 28.5,
        "temp_min": 22.4,
        "precipitation_probability_max": 20,
    }

    mock_get.assert_called_once()
    _, kwargs = mock_get.call_args
    assert kwargs["params"]["latitude"] == 25.0330
    assert kwargs["params"]["longitude"] == 121.5654
    assert kwargs["params"]["timezone"] == "Asia/Taipei"
    assert kwargs["params"]["forecast_days"] == 3
    assert kwargs["params"]["temperature_unit"] == "celsius"
    assert kwargs["params"]["wind_speed_unit"] == "kmh"


@patch("week3.tools.weather.requests.get")
def test_get_weather_forecast_returns_timeout_error_on_timeout(
    mock_get: Mock,
) -> None:
    mock_get.side_effect = requests.Timeout

    result = get_weather_forecast(
        latitude=25.0330,
        longitude=121.5654,
        timezone="Asia/Taipei",
        forecast_days=3,
        temperature_unit="celsius",
        wind_speed_unit="kmh",
    )

    assert result["status"] == "error"
    assert result["error_type"] == "timeout_error"
    assert "timed out" in result["message"]


@patch("week3.tools.weather.requests.get")
def test_get_weather_forecast_returns_api_error_on_request_exception(
    mock_get: Mock,
) -> None:
    mock_get.side_effect = requests.RequestException

    result = get_weather_forecast(
        latitude=25.0330,
        longitude=121.5654,
        timezone="Asia/Taipei",
        forecast_days=3,
        temperature_unit="celsius",
        wind_speed_unit="kmh",
    )

    assert result["status"] == "error"
    assert result["error_type"] == "api_error"
    assert "Failed to connect" in result["message"]


@patch("week3.tools.weather.requests.get")
def test_get_weather_forecast_returns_api_error_on_http_error_with_reason(
    mock_get: Mock,
) -> None:
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError
    mock_response.json.return_value = {
        "error": True,
        "reason": "Invalid coordinates",
    }
    mock_get.return_value = mock_response

    result = get_weather_forecast(
        latitude=25.0330,
        longitude=121.5654,
        timezone="Asia/Taipei",
        forecast_days=3,
        temperature_unit="celsius",
        wind_speed_unit="kmh",
    )

    assert result["status"] == "error"
    assert result["error_type"] == "api_error"
    assert result["message"] == "Invalid coordinates"


@patch("week3.tools.weather.requests.get")
def test_get_weather_forecast_returns_unexpected_error_for_invalid_json(
    mock_get: Mock,
) -> None:
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("invalid json")
    mock_get.return_value = mock_response

    result = get_weather_forecast(
        latitude=25.0330,
        longitude=121.5654,
        timezone="Asia/Taipei",
        forecast_days=3,
        temperature_unit="celsius",
        wind_speed_unit="kmh",
    )

    assert result["status"] == "error"
    assert result["error_type"] == "unexpected_error"
    assert "invalid JSON" in result["message"]


@patch("week3.tools.weather.requests.get")
def test_get_weather_forecast_returns_unexpected_error_when_current_missing(
    mock_get: Mock,
) -> None:
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "latitude": 25.0330,
        "longitude": 121.5654,
        "timezone": "Asia/Taipei",
        "daily": {
            "time": ["2026-04-02"],
            "weather_code": [3],
            "temperature_2m_max": [28.5],
            "temperature_2m_min": [22.4],
            "precipitation_probability_max": [20],
        },
    }
    mock_get.return_value = mock_response

    result = get_weather_forecast(
        latitude=25.0330,
        longitude=121.5654,
        timezone="Asia/Taipei",
        forecast_days=1,
        temperature_unit="celsius",
        wind_speed_unit="kmh",
    )

    assert result["status"] == "error"
    assert result["error_type"] == "unexpected_error"
    assert "incomplete forecast data" in result["message"]


@patch("week3.tools.weather.requests.get")
def test_get_weather_forecast_returns_unexpected_error_when_daily_missing(
    mock_get: Mock,
) -> None:
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "latitude": 25.0330,
        "longitude": 121.5654,
        "timezone": "Asia/Taipei",
        "current": {
            "time": "2026-04-02T09:00",
            "temperature_2m": 26.1,
            "wind_speed_10m": 12.3,
            "weather_code": 3,
        },
    }
    mock_get.return_value = mock_response

    result = get_weather_forecast(
        latitude=25.0330,
        longitude=121.5654,
        timezone="Asia/Taipei",
        forecast_days=1,
        temperature_unit="celsius",
        wind_speed_unit="kmh",
    )

    assert result["status"] == "error"
    assert result["error_type"] == "unexpected_error"
    assert "incomplete forecast data" in result["message"]


@patch("week3.tools.weather.requests.get")
def test_get_weather_forecast_returns_unexpected_error_when_daily_forecast_empty(
    mock_get: Mock,
) -> None:
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "latitude": 25.0330,
        "longitude": 121.5654,
        "timezone": "Asia/Taipei",
        "current": {
            "time": "2026-04-02T09:00",
            "temperature_2m": 26.1,
            "wind_speed_10m": 12.3,
            "weather_code": 3,
        },
        "daily": {
            "time": [],
            "weather_code": [],
            "temperature_2m_max": [],
            "temperature_2m_min": [],
            "precipitation_probability_max": [],
        },
    }
    mock_get.return_value = mock_response

    result = get_weather_forecast(
        latitude=25.0330,
        longitude=121.5654,
        timezone="Asia/Taipei",
        forecast_days=1,
        temperature_unit="celsius",
        wind_speed_unit="kmh",
    )

    assert result["status"] == "error"
    assert result["error_type"] == "unexpected_error"
    assert "No daily forecast data was available" in result["message"]