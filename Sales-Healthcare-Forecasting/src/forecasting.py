"""US healthcare demand forecasting with a simple ML baseline."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA_PATH = Path("data") / "healthcare_demand.csv"


def evaluate(actual: pd.Series, predicted: np.ndarray) -> dict:
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape}


def main() -> None:
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df["patients"] = pd.to_numeric(df["patients"], errors="coerce")
    df = df.dropna(subset=["date", "patients"]).sort_values("date")
    df["month_index"] = np.arange(len(df))
    df["rolling_3m"] = df["patients"].rolling(3).mean()

    # Time-based split avoids data leakage from future observations.
    split = int(len(df) * 0.8)
    train, test = df.iloc[:split], df.iloc[split:]

    model = LinearRegression()
    model.fit(train[["month_index"]], train["patients"])
    predictions = model.predict(test[["month_index"]])

    metrics = evaluate(test["patients"], predictions)
    print("US Healthcare Demand Forecasting")
    for name, value in metrics.items():
        print(f"{name}: {value:.2f}")

    future = pd.DataFrame({"month_index": np.arange(len(df), len(df) + 6)})
    future["forecast_patients"] = model.predict(future[["month_index"]])
    print("\nNext 6-month forecast:")
    print(future.round(0).to_string(index=False))

    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df["patients"], label="Historical demand")
    plt.plot(test["date"], predictions, label="ML test forecast")
    plt.title("US Healthcare Demand Forecasting")
    plt.xlabel("Month")
    plt.ylabel("Patient Demand")
    plt.legend()
    plt.tight_layout()
    plt.savefig("forecast.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    main()
