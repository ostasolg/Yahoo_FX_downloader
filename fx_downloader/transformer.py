import pandas as pd

from fx_downloader.logger_config import setup_logger


logger = setup_logger(__name__)


REQUIRED_PRICE_COLUMNS = [
    "datetime",
    "open",
    "high",
    "low",
    "close",
]

MISSING_VALUE_MARKERS = [
    "?",
    "N/A",
    "NA",
    "None",
    "null",
    "",
]


def normalize_fx_data(df: pd.DataFrame, ticker: str, currency_pair: str) -> pd.DataFrame:
    """
    Normalize raw Yahoo Finance FX data.

    Cleans column names, standardizes datetime, removes missing critical values
    and duplicate timestamps, adds metadata, and sorts by datetime.

    Args:
        df: Raw Yahoo Finance DataFrame.
        ticker: Yahoo Finance ticker symbol.
        currency_pair: Human-readable currency pair.

    Returns:
        Normalized DataFrame ready for validation and saving.
    """

    logger.info("Normalizing downloaded data.")

    normalized_df = df.copy()

    # yfinance returns Datetime as index
    normalized_df = normalized_df.reset_index()

    # Normalize column names
    normalized_df.columns = [
        str(column).lower().replace(" ", "_")
        for column in normalized_df.columns
    ]

    # For hourly data yfinance usually returns "datetime".
    # For daily data it may return "date".
    if "date" in normalized_df.columns and "datetime" not in normalized_df.columns:
        normalized_df = normalized_df.rename(columns={"date": "datetime"})

    # Convert custom missing-value markers to pandas missing values
    normalized_df.replace(MISSING_VALUE_MARKERS, pd.NA, inplace=True)

    # Make sure datetime column is really datetime type
    normalized_df["datetime"] = pd.to_datetime(normalized_df["datetime"], utc=True, errors="coerce")

    # Remove rows with missing critical values
    rows_before = len(normalized_df)
    normalized_df.dropna(subset=REQUIRED_PRICE_COLUMNS, inplace=True)
    rows_after = len(normalized_df)

    logger.info(
        "Removed %s rows with missing critical values.",
        rows_before - rows_after,
    )

    # Remove duplicate datetime, keep the last occurrence
    rows_before_dedup = len(normalized_df)
    normalized_df = normalized_df.drop_duplicates(subset=["datetime"], keep="last")
    rows_after_dedup = len(normalized_df)

    logger.info(
        "Removed %s duplicate timestamp rows.",
        rows_before_dedup - rows_after_dedup,
    )


    # Add metadata
    normalized_df["ticker"] = ticker
    normalized_df["currency_pair"] = currency_pair

    # Sort by time
    normalized_df = normalized_df.sort_values("datetime")

    return normalized_df