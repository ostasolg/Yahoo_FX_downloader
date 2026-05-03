from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
BRONZE_DATA_DIR = DATA_DIR / "bronze"
SILVER_DATA_DIR = DATA_DIR / "silver"
GOLD_DATA_DIR = DATA_DIR / "gold"

# Yahoo Finance settings
DEFAULT_TICKER = "EURCZK=X"
DEFAULT_CURRENCY_PAIR = "EUR/CZK"

# Download settings
DEFAULT_LOOKBACK_DAYS = 60
DEFAULT_INTERVAL = "1h"

# Output settings
DEFAULT_OUTPUT_FORMAT = "parquet"

def normalize_ticker_for_filename(ticker: str) -> str:
    return (
        ticker.lower()
        .replace("=", "_")
        .replace("/", "_")
        .replace("-", "_")
        .replace(".", "_")
    )


def get_dataset_name(ticker: str, start_date: str, end_date: str, interval: str) -> str:
    clean_ticker = normalize_ticker_for_filename(ticker)
    return f"{clean_ticker}_{start_date}_{end_date}_{interval}"


def get_bronze_file_path(ticker: str, start_date: str, end_date: str, interval: str, output_format: str) -> Path:

    dataset_name = get_dataset_name(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
    )

    return BRONZE_DATA_DIR / f"{dataset_name}_raw.{output_format}"


def get_silver_file_path(ticker: str, start_date: str, end_date: str, interval: str, output_format: str) -> Path:

    dataset_name = get_dataset_name(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
    )

    return SILVER_DATA_DIR / f"{dataset_name}_clean.{output_format}"