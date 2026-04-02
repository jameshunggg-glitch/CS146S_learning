# week3/tools/weather.py

from __future__ import annotations

import logging
from typing import Any

import requests

from week3.utils.validators import (
    validate_forecast_days,
    validate_latitude,
    validate_longitude,
    validate_temperature_unit,
    validate_timezone,
    validate_wind_speed_unit,
)

logger = logging.getLogger(__name__)

FORECAST_API_URL = "https://api.open-meteo.com/v1/forecast"
REQUEST_TIMEOUT_SECONDS = 10


def get_weather_forecast(
    latitude: float,
    longitude: float,
    timezone: str = "auto",
    forecast_days: int = 3,
    temperature_unit: str = "celsius",
    wind_speed_unit: str = "kmh",
) -> dict:
    try:
        latitude = validate_latitude(latitude)
        longitude = validate_longitude(longitude)
        timezone = validate_timezone(timezone)
        forecast_days = validate_forecast_days(forecast_days)
        temperature_unit = validate_temperature_unit(temperature_unit)
        wind_speed_unit = validate_wind_speed_unit(wind_speed_unit)
    except ValueError as exc:
        return {
            "status": "error",
            "error_type": "validation_error",
            "message": str(exc),
        }

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "forecast_days": forecast_days,
        "temperature_unit": temperature_unit,
        "wind_speed_unit": wind_speed_unit,
        "current": [
            "temperature_2m",
            "wind_speed_10m",
            "weather_code",
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
        ],
    }

    try:
        logger.info(
            (
                "Calling forecast API | latitude=%s longitude=%s timezone=%s "
                "forecast_days=%s temperature_unit=%s wind_speed_unit=%s"
            ),
            latitude,
            longitude,
            timezone,
            forecast_days,
            temperature_unit,
            wind_speed_unit,
        )

        response = requests.get(
            FORECAST_API_URL,
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()

    except requests.Timeout:
        logger.exception("Forecast API timeout")
        return {
            "status": "error",
            "error_type": "timeout_error",
            "message": "The weather forecast request timed out.",
        }

    except requests.HTTPError:
        logger.exception("Forecast API returned HTTP error")

        message = "The weather forecast API returned an HTTP error."
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
        logger.exception("Forecast API request failed")
        return {
            "status": "error",
            "error_type": "api_error",
            "message": "Failed to connect to the weather forecast API.",
        }

    except ValueError:
        logger.exception("Failed to decode forecast API JSON response")
        return {
            "status": "error",
            "error_type": "unexpected_error",
            "message": "The weather forecast API returned invalid JSON.",
        }

    current = payload.get("current")
    daily = payload.get("daily")

    if not current or not daily:
        return {
            "status": "error",
            "error_type": "unexpected_error",
            "message": "The weather forecast API returned incomplete forecast data.",
        }

    daily_forecast = _format_daily_forecast(daily)

    if not daily_forecast:
        return {
            "status": "error",
            "error_type": "unexpected_error",
            "message": "No daily forecast data was available.",
        }

    return {
        "status": "ok",
        "data": {
            "location": {
                "latitude": payload.get("latitude", latitude),
                "longitude": payload.get("longitude", longitude),
                "timezone": payload.get("timezone", timezone),
            },
            "current": {
                "time": current.get("time"),
                "temperature": current.get("temperature_2m"),
                "wind_speed": current.get("wind_speed_10m"),
                "weather_code": current.get("weather_code"),
            },
            "daily_forecast": daily_forecast,
        },
    }


def _format_daily_forecast(daily: dict[str, Any]) -> list[dict[str, Any]]:
    dates = daily.get("time", [])
    weather_codes = daily.get("weather_code", [])
    temp_maxs = daily.get("temperature_2m_max", [])
    temp_mins = daily.get("temperature_2m_min", [])
    precipitation_probs = daily.get("precipitation_probability_max", [])

    n_days = min(
        len(dates),
        len(weather_codes),
        len(temp_maxs),
        len(temp_mins),
        len(precipitation_probs),
    )

    results: list[dict[str, Any]] = []

    for i in range(n_days):
        results.append(
            {
                "date": dates[i],
                "weather_code": weather_codes[i],
                "temp_max": temp_maxs[i],
                "temp_min": temp_mins[i],
                "precipitation_probability_max": precipitation_probs[i],
            }
        )

    return results