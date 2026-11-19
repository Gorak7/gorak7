"""Assemble reproducible analysis outputs into the tracked Results folder."""
from pathlib import Path
import shutil
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
RESULTS = ROOT / "Results"
RESULTS.mkdir(parents=True, exist_ok=True)

FILES = {
    "forecast_metrics.csv": "forecast_metrics.csv",
    "forecast_test_results.csv": "forecast_test_results.csv",
    "anomaly_flags.csv": "anomaly_flags.csv",
    "data_quality_report.csv": "data_quality_report.csv",
    "daily_consumption.png": "daily_consumption.png",
    "anomalies_by_site.png": "anomalies_by_site.png",
    "forecast_comparison_by_site.png": "forecast_comparison_by_site.png",
}

for source_name, result_name in FILES.items():
    source = OUTPUTS / source_name
    if not source.is_file():
        raise FileNotFoundError(f"Expected analysis output was not created: {source}")
    shutil.copy2(source, RESULTS / result_name)

flags = pd.read_csv(OUTPUTS / "anomaly_flags.csv")
summary = (
    flags.groupby(["site_id", "metric"], as_index=False)
    .agg(
        readings_reviewed=("is_anomaly", "size"),
        anomalies_flagged=("is_anomaly", "sum"),
    )
)
summary["anomaly_rate_percent"] = (
    summary["anomalies_flagged"] / summary["readings_reviewed"] * 100
).round(2)
summary.to_csv(RESULTS / "anomaly_summary.csv", index=False)

print(f"Exported {len(FILES) + 1} result files to {RESULTS}")
