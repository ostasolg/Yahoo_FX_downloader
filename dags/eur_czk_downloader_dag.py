# from datetime import datetime
#
# from airflow import DAG
# from airflow.operators.bash import BashOperator
#
#
# with DAG(
#     dag_id="eur_czk_yahoo_downloader",
#     description="Download hourly EUR/CZK data from Yahoo Finance.",
#     start_date=datetime(2026, 1, 1),
#     schedule="@hourly",
#     catchup=False,
#     tags=["fx", "yahoo", "eur_czk"],
# ) as dag:
#
#     download_eur_czk = BashOperator(
#         task_id="download_eur_czk_hourly_data",
#         bash_command=(
#             "cd /path/to/yahoo_fx_downloader && "
#             "python -m fx_downloader.cli "
#             "--ticker EURCZK=X "
#             "--interval 1h "
#             "--format parquet"
#         ),
#     )