# Yahoo FX Downloader

A small Python CLI tool for downloading EUR/CZK exchange-rate data from Yahoo Finance.

The tool downloads hourly data, saves raw data into the Bronze layer, transforms and validates it, and saves cleaned data into the Silver layer.

## Task

Download data from Yahoo Finance:

- currency pair: EUR/CZK
- ticker: `EURCZK=X`
- interval: `1h`
- output formats: CSV, JSON, Parquet

## Project structure

```text
yahoo_fx_downloader/
├── README.md
├── requirements.txt
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
└── fx_downloader/
    ├── cli.py
    ├── config.py
    ├── logger_config.py
    ├── yahoo_client.py
    ├── transformer.py
    ├── validator.py
    └── storage.py
