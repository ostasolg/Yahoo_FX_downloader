import pandas as pd

from fx_downloader.logger_config import setup_logger


logger = setup_logger(__name__)


REQUIRED_COLUMNS = {
    "datetime",
    "open",
    "high",
    "low",
    "close",
}

PRICE_COLUMNS = ["open", "high", "low", "close"]

def validate_fx_data(df: pd.DataFrame) -> None:
    """
    Validate normalized FX data.

    Raises:
        ValueError: If the data is empty, invalid, or contains duplicate timestamps.
    """

    logger.info("Validating FX data.")

    if df.empty:
        raise ValueError("Downloaded data is empty.")

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df["datetime"].isnull().any():
        raise ValueError("Datetime column contains missing values.")

    for column in PRICE_COLUMNS:
        if df[column].isnull().any():
            raise ValueError(f"{column} column contains missing values.")

    if df["datetime"].duplicated().any():
        raise ValueError("Data contains duplicate timestamps.")

    for column in PRICE_COLUMNS:
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError(f"{column} column must be numeric.")

    logger.info("FX data validation passed.")