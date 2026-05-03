import pandas as pd
import yfinance as yf

from fx_downloader.logger_config import setup_logger


logger = setup_logger(__name__)


def download_fx_data(ticker: str, start_date: str, end_date: str, interval: str) -> pd.DataFrame:
    """
      Download FX data from Yahoo Finance.

      Args:
          ticker: Yahoo Finance ticker symbol.
          start_date: Start date for the download.
          end_date: End date for the download.
          interval: Data interval, for example "1h" or "1d".

      Returns:
          Raw Yahoo Finance data as a pandas DataFrame.

      Raises:
          ValueError: If no data is downloaded.
      """
    logger.info(
        "Downloading data from Yahoo Finance | ticker=%s | start=%s | end=%s | interval=%s",
        ticker,
        start_date,
        end_date,
        interval,
    )

    df = yf.download(
        tickers=ticker,
        start=start_date,
        end=end_date,
        interval=interval,
        auto_adjust=False,
        progress=False,
    )

    if df is None or df.empty:
        raise ValueError("No data downloaded from Yahoo Finance.")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        df.columns.name = None

    logger.info("Downloaded %s rows from Yahoo Finance.", len(df))

    return df