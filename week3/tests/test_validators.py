# week3/tests/test_validators.py

from __future__ import annotations

import pytest

from week3.utils.validators import (
    validate_count,
    validate_forecast_days,
    validate_language,
    validate_latitude,
    validate_longitude,
    validate_query,
    validate_temperature_unit,
    validate_timezone,
    validate_wind_speed_unit,
)


# ---------------------------------------------------------
# validate_query
# ---------------------------------------------------------
def test_validate_query_returns_stripped_query() -> None:
    assert validate_query("  Taipei  ") == "Taipei"


def test_validate_query_raises_for_empty_string() -> None:
    with pytest.raises(ValueError, match="query cannot be empty"):
        validate_query("   ")


def test_validate_query_raises_for_non_string() -> None:
    with pytest.raises(ValueError, match="query must be a string"):
        validate_query(123)  # type: ignore[arg-type]


# ---------------------------------------------------------
# validate_count
# ---------------------------------------------------------
def test_validate_count_accepts_valid_integer() -> None:
    assert validate_count(5) == 5


def test_validate_count_raises_for_zero() -> None:
    with pytest.raises(ValueError, match="count must be greater than 0"):
        validate_count(0)


def test_validate_count_raises_for_too_large_value() -> None:
    with pytest.raises(ValueError, match="count must be less than or equal to 10"):
        validate_count(11)


def test_validate_count_raises_for_non_integer() -> None:
    with pytest.raises(ValueError, match="count must be an integer"):
        validate_count("5")  # type: ignore[arg-type]


# ---------------------------------------------------------
# validate_language
# ---------------------------------------------------------
def test_validate_language_accepts_supported_language() -> None:
    assert validate_language("EN") == "en"


def test_validate_language_raises_for_empty_string() -> None:
    with pytest.raises(ValueError, match="language cannot be empty"):
        validate_language("   ")


def test_validate_language_raises_for_unsupported_language() -> None:
    with pytest.raises(ValueError, match="language must be one of:"):
        validate_language("fr")


# ---------------------------------------------------------
# validate_latitude
# ---------------------------------------------------------
def test_validate_latitude_accepts_valid_number() -> None:
    assert validate_latitude(25.03) == 25.03


def test_validate_latitude_accepts_integer_and_returns_float() -> None:
    assert validate_latitude(25) == 25.0


def test_validate_latitude_raises_for_out_of_range_value() -> None:
    with pytest.raises(ValueError, match="latitude must be between -90 and 90"):
        validate_latitude(100)


# ---------------------------------------------------------
# validate_longitude
# ---------------------------------------------------------
def test_validate_longitude_accepts_valid_number() -> None:
    assert validate_longitude(121.56) == 121.56


def test_validate_longitude_raises_for_out_of_range_value() -> None:
    with pytest.raises(ValueError, match="longitude must be between -180 and 180"):
        validate_longitude(200)


# ---------------------------------------------------------
# validate_forecast_days
# ---------------------------------------------------------
def test_validate_forecast_days_accepts_valid_integer() -> None:
    assert validate_forecast_days(3) == 3


def test_validate_forecast_days_raises_for_zero() -> None:
    with pytest.raises(ValueError, match="forecast_days must be greater than 0"):
        validate_forecast_days(0)


def test_validate_forecast_days_raises_for_too_large_value() -> None:
    with pytest.raises(
        ValueError, match="forecast_days must be less than or equal to 7"
    ):
        validate_forecast_days(8)


# ---------------------------------------------------------
# validate_temperature_unit
# ---------------------------------------------------------
def test_validate_temperature_unit_accepts_supported_unit() -> None:
    assert validate_temperature_unit("Celsius") == "celsius"


def test_validate_temperature_unit_raises_for_unsupported_unit() -> None:
    with pytest.raises(ValueError, match="temperature_unit must be one of:"):
        validate_temperature_unit("kelvin")


# ---------------------------------------------------------
# validate_wind_speed_unit
# ---------------------------------------------------------
def test_validate_wind_speed_unit_accepts_supported_unit() -> None:
    assert validate_wind_speed_unit("MPH") == "mph"


def test_validate_wind_speed_unit_raises_for_unsupported_unit() -> None:
    with pytest.raises(ValueError, match="wind_speed_unit must be one of:"):
        validate_wind_speed_unit("miles_per_hour")


# ---------------------------------------------------------
# validate_timezone
# ---------------------------------------------------------
def test_validate_timezone_accepts_valid_string() -> None:
    assert validate_timezone("auto") == "auto"


def test_validate_timezone_raises_for_empty_string() -> None:
    with pytest.raises(ValueError, match="timezone cannot be empty"):
        validate_timezone("   ")