"""Quality checks, robust anomaly flags, baseline forecasting, charts, and SQLite."""
from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "utility_readings.csv"
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)


def robust_anomalies(series, window=28, threshold=3.5):
    prior = series.shift(1)  # do not include the current observation in its baseline
    median = prior.rolling(window, min_periods=14).median()
    mad = prior.rolling(window, min_periods=14).apply(
        lambda x: np.median(np.abs(x - np.median(x))), raw=True
    )
    score = (series - median) / (1.4826 * mad).replace(0, np.nan)
    return pd.DataFrame({
        "actual": series,
        "baseline_median": median,
        "robust_z_score": score,
        "is_anomaly": (score.abs() >= threshold).fillna(False),
    })


def main():
    if not DATA.exists():
        raise FileNotFoundError("Run python src/generate_data.py first.")
    raw = pd.read_csv(DATA)
    raw["date"] = pd.to_datetime(raw["date"], errors="coerce")
    for col in ["electricity_kwh", "water_m3"]:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    quality = {
        "input_rows": len(raw),
        "duplicate_date_site": int(raw.duplicated(["date", "site_id"]).sum()),
        "invalid_dates": int(raw.date.isna().sum()),
        "missing_values": int(raw[["site_id", "electricity_kwh", "water_m3"]].isna().any(axis=1).sum()),
        "nonpositive_electricity": int((raw.electricity_kwh <= 0).sum()),
        "nonpositive_water": int((raw.water_m3 <= 0).sum()),
    }
    pd.DataFrame([quality]).to_csv(OUT / "data_quality_report.csv", index=False)
    clean = raw.dropna(subset=["date", "site_id", "electricity_kwh", "water_m3"]).copy()
    clean = clean[(clean.electricity_kwh > 0) & (clean.water_m3 > 0)]
    clean = clean.drop_duplicates(["date", "site_id"]).sort_values(["site_id", "date"])
    clean.to_csv(OUT / "clean_utility_readings.csv", index=False)

    frames = []
    for site, group in clean.groupby("site_id"):
        group = group.sort_values("date")
        for metric in ["electricity_kwh", "water_m3"]:
            result = robust_anomalies(group[metric])
            part = result.reset_index(drop=True)
            part["date"] = group["date"].to_numpy()
            part["site_id"] = site
            part["metric"] = metric
            frames.append(part)
    anomalies = pd.concat(frames, ignore_index=True)
    anomalies.to_csv(OUT / "anomaly_flags.csv", index=False)

    daily = clean.groupby("date")["electricity_kwh"].sum().sort_index().asfreq("D")
    daily = daily.interpolate(limit=2).dropna()
    split = int(len(daily) * 0.8)
    test = daily.iloc[split:].to_frame("actual_kwh")
    test["forecast_kwh"] = daily.shift(7).reindex(test.index)
    test = test.dropna()
    error = test.actual_kwh - test.forecast_kwh
    metrics = pd.DataFrame([{
        "model": "7-day seasonal naive",
        "test_rows": len(test),
        "MAE_kWh": float(np.abs(error).mean()),
        "RMSE_kWh": float(np.sqrt(np.mean(error ** 2))),
        "MAPE_percent": float((np.abs(error) / test.actual_kwh.replace(0, np.nan)).mean() * 100),
    }])
    test.reset_index().to_csv(OUT / "forecast_test_results.csv", index=False)
    metrics.to_csv(OUT / "forecast_metrics.csv", index=False)

    fig, ax = plt.subplots(figsize=(11, 5))
    daily.plot(ax=ax)
    ax.set(title="Daily Portfolio Electricity Consumption", xlabel="Date", ylabel="kWh")
    fig.tight_layout()
    fig.savefig(OUT / "daily_consumption.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(daily.index, daily.values, label="Portfolio daily electricity")
    flagged_dates = pd.to_datetime(anomalies.loc[
        (anomalies.metric == "electricity_kwh") & anomalies.is_anomaly, "date"
    ].unique())
    flagged_dates = flagged_dates[flagged_dates.isin(daily.index)]
    ax.scatter(flagged_dates, daily.reindex(flagged_dates), label="Investigation dates", zorder=3)
    ax.set(title="Consumption and Anomaly Review Dates", xlabel="Date", ylabel="kWh")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "anomalies.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(test.index, test.actual_kwh, label="Actual")
    ax.plot(test.index, test.forecast_kwh, label="7-day seasonal-naive forecast")
    ax.set(title="Forecast Baseline: Holdout Period", xlabel="Date", ylabel="kWh")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "forecast_comparison.png", dpi=150)
    plt.close(fig)

    with sqlite3.connect(OUT / "energy_analytics.db") as conn:
        clean.to_sql("utility_readings", conn, if_exists="replace", index=False)
        anomalies.to_sql("anomaly_flags", conn, if_exists="replace", index=False)
        metrics.to_sql("forecast_metrics", conn, if_exists="replace", index=False)
        pd.DataFrame([quality]).to_sql("data_quality_report", conn, if_exists="replace", index=False)
    print(f"Analysis complete. Retained {len(clean):,} rows; flagged {int(anomalies.is_anomaly.sum()):,} anomalies.")
    print(metrics.to_string(index=False))
    print(f"Outputs: {OUT}")


if __name__ == "__main__":
    main()
