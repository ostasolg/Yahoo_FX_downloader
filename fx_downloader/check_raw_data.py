import yfinance as yf


df = yf.download(
    tickers="EURCZK=X",
    period="5d",
    interval="1h",
    auto_adjust=False,
    progress=False,
)

print("DataFrame shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nColumn types:")
print(df.dtypes)

print("\nIndex:")
print(df.index)

print("\nFirst 5 rows:")
print(df.head())

print("\nStatistical summary:")
print(df.describe(include="all"))