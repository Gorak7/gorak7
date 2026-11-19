"""Quality checks, robust anomaly flags, site-level forecasting, charts, and SQLite."""
from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "utility_readings.csv"
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)


def robust_anomalies(series: pd.Series, window: int = 28, threshold: float = 3.5):
    """Flag outliers against prior observations; handle a zero-MAD baseline explicitly."""
    prior = series.shift(1)
    median = prior.rolling(window, min_periods=14).median()
    mad = prior.rolling(window, min_periods=14).apply(
        lambda values: np.median(np.abs(values - np.median(values))), raw=True
    )
    deviation = series - median
    scaled_mad = 1.4826 * mad
    score = deviation / scaled_mad.replace(0, np.nan)

    # If prior observations are constant (MAD=0), any non-zero deviation is flagged.
    zero_mad = (scaled_mad == 0) & median.notna()
    score = score.where(~zero_mad, np.where(deviation == 0, 0.0, np.inf))
    flags = score.abs() >= threshold
    return pd.DataFrame({
        "actual": series,
        "baseline_median": median,
        "robust_z_score": score,
        "is_anomaly": flags.fillna(False),
    })


def calculate_forecast_metrics(actual: pd.Series, forecast: pd.Series) -> dict:
    """Return common forecast metrics, excluding missing pairs and zero actuals for MAPE."""
    pairs = pd.concat(
        [actual.rename("actual"), forecast.rename("forecast")], axis=1
    ).dropna()
    if pairs.empty:
        return {"test_rows": 0, "MAE_kWh": np.nan, "RMSE_kWh": np.nan, "MAPE_percent": np.nan}
    error = pairs["actual"] - pairs["forecast"]
    nonzero = pairs["actual"] != 0
    mape = (
        (error[nonzero].abs() / pairs.loc[nonzero, "actual"].abs()).mean() * 100
        if nonzero.any() else np.nan
    )
    return {
        "test_rows": len(pairs),
        "MAE_kWh": float(error.abs().mean()),
        "RMSE_kWh": float(np.sqrt(np.mean(error ** 2))),
        "MAPE_percent": float(mape) if pd.notna(mape) else np.nan,
    }


def clean_readings(raw: pd.DataFrame):
    required = ["date", "site_id", "electricity_kwh", "water_m3"]
    missing_columns = sorted(set(required) - set(raw.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    df = raw.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for column in ["electricity_kwh", "water_m3"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    duplicate_rows = int(df.duplicated(["date", "site_id"], keep="first").sum())
    invalid_date_rows = int(df["date"].isna().sum())
    missing_rows = int(df[required].isna().any(axis=1).sum())
    invalid_numeric_rows = int(
        ((df["electricity_kwh"] <= 0) | (df["water_m3"] <= 0)).fillna(False).sum()
    )
    clean = df.dropna(subset=required).copy()
    clean = clean[(clean["electricity_kwh"] > 0) & (clean["water_m3"] > 0)]
    clean = clean.drop_duplicates(["date", "site_id"], keep="first")
    clean = clean.sort_values(["site_id", "date"]).copy()
    quality = {
        "input_rows": len(df),
        "duplicate_date_site_rows": duplicate_rows,
        "invalid_date_rows": invalid_date_rows,
        "rows_with_missing_required_values": missing_rows,
        "rows_with_nonpositive_values": invalid_numeric_rows,
        "retained_rows": len(clean),
        "rejected_rows": len(df) - len(clean),
    }
    return clean, quality


def build_site_forecasts(clean: pd.DataFrame):
    """Create a chronological 80/20 holdout and 7-day seasonal-naive forecast per site."""
    forecasts = []
    metric_rows = []
    for site, group in clean.groupby("site_id"):
        daily = (
            group.set_index("date")["electricity_kwh"]
            .sort_index()
            .asfreq("D")
            .interpolate(limit=2)
            .dropna()
        )
        if len(daily) < 35:
            continue
        split = int(len(daily) * 0.8)
        test = daily.iloc[split:].to_frame("actual_kwh")
        test["forecast_kwh"] = daily.shift(7).reindex(test.index)
        test = test.dropna()
        test["site_id"] = site
        forecasts.append(test.reset_index())
        metrics = calculate_forecast_metrics(test["actual_kwh"], test["forecast_kwh"])
        metric_rows.append({"site_id": site, "model": "7-day seasonal naive", **metrics})
    if not forecasts:
        raise ValueError("No site has enough daily history for a 7-day holdout forecast.")
    return pd.concat(forecasts, ignore_index=True), pd.DataFrame(metric_rows)


def main():
    if not DATA.exists():
        raise FileNotFoundError("Run python src/generate_data.py first.")
    raw = pd.read_csv(DATA)
    clean, quality = clean_readings(raw)
    pd.DataFrame([quality]).to_csv(OUT / "data_quality_report.csv", index=False)
    if clean.empty:
        raise ValueError("No valid records remain after data-quality checks.")
    clean.to_csv(OUT / "clean_utility_readings.csv", index=False)

    anomaly_frames = []
    for site, group in clean.groupby("site_id"):
        group = group.sort_values("date")
        for metric in ["electricity_kwh", "water_m3"]:
            result = robust_anomalies(group.set_index("date")[metric])
            part = result.reset_index()
            part["site_id"] = site
            part["metric"] = metric
            anomaly_frames.append(part)
    anomalies = pd.concat(anomaly_frames, ignore_index=True)
    anomalies.to_csv(OUT / "anomaly_flags.csv", index=False)

    forecasts, metrics = build_site_forecasts(clean)
    forecasts.to_csv(OUT / "forecast_test_results.csv", index=False)
    metrics.to_csv(OUT / "forecast_metrics.csv", index=False)

    daily = clean.groupby("date", as_index=False)["electricity_kwh"].sum()
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(daily["date"], daily["electricity_kwh"])
    ax.set(title="Daily Portfolio Electricity Consumption", xlabel="Date", ylabel="kWh")
    fig.tight_layout()
    fig.savefig(OUT / "daily_consumption.png", dpi=150)
    plt.close(fig)

    # Plot site-level anomaly markers against the same site's readings.
    sites = sorted(clean["site_id"].unique())
    fig, axes = plt.subplots(len(sites), 1, figsize=(11, max(4, 3 * len(sites))), squeeze=False)
    for ax, site in zip(axes[:, 0], sites):
        readings = clean[clean["site_id"] == site].sort_values("date")
        flagged = anomalies[
            (anomalies["site_id"] == site)
            & (anomalies["metric"] == "electricity_kwh")
            & anomalies["is_anomaly"]
        ]
        ax.plot(readings["date"], readings["electricity_kwh"], label="Electricity use")
        ax.scatter(flagged["date"], flagged["actual"], label="Flagged readings", zorder=3)
        ax.set_title(site)
        ax.set_ylabel("kWh")
        ax.legend()
    axes[-1, 0].set_xlabel("Date")
    fig.suptitle("Site-level Electricity Anomaly Review", y=1.01)
    fig.tight_layout()
    fig.savefig(OUT / "anomalies_by_site.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(len(sites), 1, figsize=(11, max(4, 3 * len(sites))), squeeze=False)
    for ax, site in zip(axes[:, 0], sites):
        site_forecast = forecasts[forecasts["site_id"] == site]
        ax.plot(site_forecast["date"], site_forecast["actual_kwh"], label="Actual")
        ax.plot(site_forecast["date"], site_forecast["forecast_kwh"], label="7-day baseline")
        ax.set_title(site)
        ax.set_ylabel("kWh")
        ax.legend()
    axes[-1, 0].set_xlabel("Date")
    fig.suptitle("Site-level Forecast Holdout Comparison", y=1.01)
    fig.tight_layout()
    fig.savefig(OUT / "forecast_comparison_by_site.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with sqlite3.connect(OUT / "energy_analytics.db") as conn:
        clean.to_sql("utility_readings", conn, if_exists="replace", index=False)
        anomalies.to_sql("anomaly_flags", conn, if_exists="replace", index=False)
        forecasts.to_sql("forecast_test_results", conn, if_exists="replace", index=False)
        metrics.to_sql("forecast_metrics", conn, if_exists="replace", index=False)
        pd.DataFrame([quality]).to_sql("data_quality_report", conn, if_exists="replace", index=False)

    print(f"Analysis complete. Retained {len(clean):,} of {len(raw):,} rows.")
    print(f"Rejected rows: {quality['rejected_rows']:,}")
    print(metrics.to_string(index=False))
    print(f"Outputs: {OUT}")


if __name__ == "__main__":
    main()
