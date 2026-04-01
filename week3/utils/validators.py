# week3/utils/validators.py

from __future__ import annotations


SUPPORTED_TEMPERATURE_UNITS = {"celsius", "fahrenheit"}
SUPPORTED_WIND_SPEED_UNITS = {"kmh", "ms", "mph", "kn"}
SUPPORTED_LANGUAGES = {"en", "zh", "ja", "ko"}


def validate_query(query: str) -> str:
    if not isinstance(query, str):
        raise ValueError("query must be a string")

    query = query.strip()
    if not query:
        raise ValueError("query cannot be empty")

    return query


def validate_count(count: int) -> int:
    if not isinstance(count, int):
        raise ValueError("count must be an integer")

    if count <= 0:
        raise ValueError("count must be greater than 0")

    if count > 10:
        raise ValueError("count must be less than or equal to 10")

    return count


def validate_language(language: str) -> str:
    if not isinstance(language, str):
        raise ValueError("language must be a string")

    language = language.strip().lower()
    if not language:
        raise ValueError("language cannot be empty")

    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"language must be one of: {sorted(SUPPORTED_LANGUAGES)}"
        )

    return language


def validate_latitude(latitude: float) -> float:
    if not isinstance(latitude, (int, float)):
        raise ValueError("latitude must be a number")

    latitude = float(latitude)
    if not (-90 <= latitude <= 90):
        raise ValueError("latitude must be between -90 and 90")

    return latitude


def validate_longitude(longitude: float) -> float:
    if not isinstance(longitude, (int, float)):
        raise ValueError("longitude must be a number")

    longitude = float(longitude)
    if not (-180 <= longitude <= 180):
        raise ValueError("longitude must be between -180 and 180")

    return longitude


def validate_forecast_days(forecast_days: int) -> int:
    if not isinstance(forecast_days, int):
        raise ValueError("forecast_days must be an integer")

    if forecast_days <= 0:
        raise ValueError("forecast_days must be greater than 0")

    if forecast_days > 7:
        raise ValueError("forecast_days must be less than or equal to 7")

    return forecast_days


def validate_temperature_unit(temperature_unit: str) -> str:
    if not isinstance(temperature_unit, str):
        raise ValueError("temperature_unit must be a string")

    temperature_unit = temperature_unit.strip().lower()
    if temperature_unit not in SUPPORTED_TEMPERATURE_UNITS:
        raise ValueError(
            f"temperature_unit must be one of: {sorted(SUPPORTED_TEMPERATURE_UNITS)}"
        )

    return temperature_unit


def validate_wind_speed_unit(wind_speed_unit: str) -> str:
    if not isinstance(wind_speed_unit, str):
        raise ValueError("wind_speed_unit must be a string")

    wind_speed_unit = wind_speed_unit.strip().lower()
    if wind_speed_unit not in SUPPORTED_WIND_SPEED_UNITS:
        raise ValueError(
            f"wind_speed_unit must be one of: {sorted(SUPPORTED_WIND_SPEED_UNITS)}"
        )

    return wind_speed_unit


def validate_timezone(timezone: str) -> str:
    if not isinstance(timezone, str):
        raise ValueError("timezone must be a string")

    timezone = timezone.strip()
    if not timezone:
        raise ValueError("timezone cannot be empty")

    return timezone