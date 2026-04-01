# week3/tools/weather.py

from __future__ import annotations

from week3.utils.validators import (
    validate_forecast_days,
    validate_latitude,
    validate_longitude,
    validate_temperature_unit,
    validate_timezone,
    validate_wind_speed_unit,
)


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

    return {
        "status": "ok",
        "data": {
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "timezone": timezone,
            },
            "forecast_days": forecast_days,
            "temperature_unit": temperature_unit,
            "wind_speed_unit": wind_speed_unit,
            "current": {},
            "daily_forecast": [],
        },
    }