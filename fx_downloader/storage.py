from pathlib import Path
import pandas as pd

from fx_downloader.logger_config import setup_logger


logger = setup_logger(__name__)


def save_fx_data(df: pd.DataFrame, output_path: str | Path, output_format: str) -> None:
    """
    Save FX data to CSV, JSON, or Parquet.

    Args:
        df: DataFrame with FX data.
        output_path: Path where the file should be saved.
        output_format: csv, json, or parquet.
    """

    output_file_path = Path(output_path)
    output_file_path.parent.mkdir(parents=True, exist_ok=True)

    output_format = output_format.lower()

    logger.info(
        "Saving FX data | path=%s | format=%s",
        output_file_path,
        output_format
    )

    if output_format == "csv":
        df.to_csv(output_file_path, index=False)

    elif output_format == "json":
        df.to_json(
            output_file_path,
            orient="records",
            indent=2,
            date_format="iso",
        )

    elif output_format == "parquet":
        df.to_parquet(output_file_path, index=False)

    else:
        raise ValueError("Unsupported output format. Use csv, json, or parquet.")

    logger.info("FX data saved successfully.")


def load_fx_data(input_path: str | Path, input_format: str) -> pd.DataFrame:
    """
    Load FX data from CSV, JSON, or Parquet.

    Args:
        input_path: Path to the input file.
        input_format: Input file format: csv, json, or parquet.

    Returns:
        Loaded FX data as a pandas DataFrame.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the input format is unsupported.
    """

    input_file_path = Path(input_path)

    if not input_file_path.exists():
        raise FileNotFoundError(f"Input file does not exist: {input_file_path}")

    input_format = input_format.lower()

    logger.info(
        "Loading FX data | path=%s | format=%s",
        input_file_path,
        input_format,
    )

    if input_format == "csv":
        return pd.read_csv(input_file_path)

    elif input_format == "json":
        return pd.read_json(input_file_path)

    elif input_format == "parquet":
        return pd.read_parquet(input_file_path)

    else:
        raise ValueError("Unsupported input format. Use csv, json, or parquet.")