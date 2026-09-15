"""Baseline time-series forecasting workflow for the project."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


def preprocess(df: pd.DataFrame, date_col: str, value_col: str) -> pd.DataFrame:
    """Parse dates, remove invalid rows, sort chronologically, and aggregate."""
    data = df.copy()
    data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
    data[value_col] = pd.to_numeric(data[value_col], errors="coerce")
    data = data.dropna(subset=[date_col, value_col]).sort_values(date_col)
    return data.groupby(date_col, as_index=False)[value_col].sum()


def evaluate(actual: pd.Series, predicted: pd.Series) -> dict:
    """Return common forecasting error metrics."""
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    non_zero = actual != 0
    mape = np.mean(
        np.abs((actual[non_zero] - predicted[non_zero]) / actual[non_zero])
    ) * 100
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape}


def naive_forecast(train: pd.Series, test: pd.Series) -> pd.Series:
    """Simple last-observation baseline for a transparent benchmark."""
    return pd.Series(train.iloc[-1], index=test.index, dtype=float)


if __name__ == "__main__":
    data_path = Path("data") / "data.csv"
    if data_path.exists():
        raw = pd.read_csv(data_path)
        prepared = preprocess(raw, "Date", "Value")
        split = int(len(prepared) * 0.8)
        train = prepared.iloc[:split]
        test = prepared.iloc[split:]
        predictions = naive_forecast(train["Value"], test["Value"])
        print(evaluate(test["Value"], predictions))
    else:
        print("Add a dataset at data/data.csv with Date and Value columns to run the baseline.")
