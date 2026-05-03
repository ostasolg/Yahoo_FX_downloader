import argparse
from datetime import datetime, timedelta, timezone

from fx_downloader.config import (
    DEFAULT_CURRENCY_PAIR,
    DEFAULT_INTERVAL,
    DEFAULT_LOOKBACK_DAYS,
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_TICKER,
    get_bronze_file_path,
    get_silver_file_path,
)

from fx_downloader.yahoo_client import download_fx_data
from fx_downloader.transformer import normalize_fx_data
from fx_downloader.validator import validate_fx_data
from fx_downloader.storage import load_fx_data, save_fx_data
from fx_downloader.logger_config import setup_logger

logger = setup_logger(__name__)


def get_default_date_range() -> tuple[str, str]:
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=DEFAULT_LOOKBACK_DAYS)

    return start_date.isoformat(), end_date.isoformat()


def parse_args() -> argparse.Namespace:
    default_start_date, default_end_date = get_default_date_range()

    parser = argparse.ArgumentParser(
        description="Download EUR/CZK hourly exchange-rate data from Yahoo Finance."
    )

    parser.add_argument(
        "--ticker",
        default=DEFAULT_TICKER,
        help=f"Yahoo Finance ticker. Default: {DEFAULT_TICKER}",
    )

    parser.add_argument(
        "--start-date",
        default=default_start_date,
        help=f"Start date in YYYY-MM-DD format. Default: {default_start_date}",
    )

    parser.add_argument(
        "--end-date",
        default=default_end_date,
        help=f"End date in YYYY-MM-DD format. Default: {default_end_date}",
    )

    parser.add_argument(
        "--interval",
        default=DEFAULT_INTERVAL,
        help=f"Data interval. Default: {DEFAULT_INTERVAL}",
    )

    parser.add_argument(
        "--format",
        choices=["csv", "json", "parquet"],
        default=DEFAULT_OUTPUT_FORMAT,
        help=f"Output format. Default: {DEFAULT_OUTPUT_FORMAT}",
    )

    parser.add_argument(
        "--overwrite-bronze",
        action="store_true",
        help="Download raw Bronze data again even if it already exists.",
    )

    parser.add_argument(
        "--overwrite-silver",
        action="store_true",
        help="Create Silver data again even if it already exists.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logger.info("Starting Yahoo FX downloader.")

    bronze_path = get_bronze_file_path(
        ticker=args.ticker,
        start_date=args.start_date,
        end_date=args.end_date,
        interval=args.interval,
        output_format=args.format,
    )

    silver_path = get_silver_file_path(
        ticker=args.ticker,
        start_date=args.start_date,
        end_date=args.end_date,
        interval=args.interval,
        output_format=args.format,
    )

    logger.info("Bronze path: %s", bronze_path)
    logger.info("Silver path: %s", silver_path)

    # Step 1: Get Bronze data
    if bronze_path.exists() and not args.overwrite_bronze:
        logger.info("Bronze data already exists. Loading from file.")

        bronze_df = load_fx_data(
            input_path=bronze_path,
            input_format=args.format,
        )

    else:
        logger.info("Downloading raw data from Yahoo Finance.")

        raw_df = download_fx_data(
            ticker=args.ticker,
            start_date=args.start_date,
            end_date=args.end_date,
            interval=args.interval,
        )

        bronze_df = raw_df.reset_index()

        save_fx_data(
            df=bronze_df,
            output_path=bronze_path,
            output_format=args.format,
        )

        logger.info("Bronze data saved.")

    # Step 2: Create Silver data
    if silver_path.exists() and not args.overwrite_silver:
        logger.info("Silver data already exists. Nothing to do.")
        return

    silver_df = normalize_fx_data(
        df=bronze_df,
        ticker=args.ticker,
        currency_pair=DEFAULT_CURRENCY_PAIR,
    )

    validate_fx_data(silver_df)

    save_fx_data(
        df=silver_df,
        output_path=silver_path,
        output_format=args.format,
    )

    logger.info("Silver data saved.")
    logger.info("Finished successfully. Rows saved: %s", len(silver_df))


if __name__ == "__main__":
    main()