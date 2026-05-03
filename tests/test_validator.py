import pandas as pd
import pytest

from fx_downloader.validator import validate_fx_data


def test_validate_fx_data_passes_for_valid_data():
    df = pd.DataFrame(
        {
            "datetime": pd.to_datetime(["2026-05-01 10:00:00"], utc=True),
            "open": [24.8],
            "high": [24.9],
            "low": [24.7],
            "close": [24.85],
        }
    )

    validate_fx_data(df)


def test_validate_fx_data_fails_for_empty_data():
    df = pd.DataFrame()

    with pytest.raises(ValueError, match="empty"):
        validate_fx_data(df)


def test_validate_fx_data_fails_for_duplicate_timestamps():
    df = pd.DataFrame(
        {
            "datetime": pd.to_datetime(
                ["2026-05-01 10:00:00", "2026-05-01 10:00:00"],
                utc=True,
            ),
            "open": [24.8, 24.8],
            "high": [24.9, 24.9],
            "low": [24.7, 24.7],
            "close": [24.85, 24.86],
        }
    )

    with pytest.raises(ValueError, match="duplicate"):
        validate_fx_data(df)