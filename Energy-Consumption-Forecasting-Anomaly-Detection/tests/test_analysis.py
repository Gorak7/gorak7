import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analyze_energy import (
    build_site_forecasts,
    calculate_forecast_metrics,
    clean_readings,
    robust_anomalies,
)


class EnergyAnalysisTests(unittest.TestCase):
    def test_zero_mad_flags_nonzero_deviation(self):
        values = pd.Series([10.0] * 14 + [30.0])
        result = robust_anomalies(values)
        self.assertTrue(bool(result.iloc[-1]["is_anomaly"]))

    def test_quality_report_counts_rejected_rows(self):
        raw = pd.DataFrame([
            {"date": "2025-01-01", "site_id": "A", "electricity_kwh": 10, "water_m3": 2},
            {"date": "bad-date", "site_id": "A", "electricity_kwh": 10, "water_m3": 2},
        ])
        clean, report = clean_readings(raw)
        self.assertEqual(len(clean), 1)
        self.assertEqual(report["retained_rows"], 1)
        self.assertEqual(report["rejected_rows"], 1)

    def test_forecast_metrics(self):
        actual = pd.Series([10.0, 20.0])
        forecast = pd.Series([8.0, 18.0])
        metrics = calculate_forecast_metrics(actual, forecast)
        self.assertEqual(metrics["test_rows"], 2)
        self.assertAlmostEqual(metrics["MAE_kWh"], 2.0)
        self.assertAlmostEqual(metrics["RMSE_kWh"], 2.0)
        self.assertAlmostEqual(metrics["MAPE_percent"], 15.0)

    def test_forecasts_are_created_per_site(self):
        dates = pd.date_range("2025-01-01", periods=60, freq="D")
        rows = []
        for site, base in [("A", 100), ("B", 200)]:
            rows.extend({"date": date, "site_id": site, "electricity_kwh": base + i,
                         "water_m3": 5} for i, date in enumerate(dates))
        forecasts, metrics = build_site_forecasts(pd.DataFrame(rows))
        self.assertEqual(set(metrics["site_id"]), {"A", "B"})
        self.assertEqual(set(forecasts["site_id"]), {"A", "B"})
        self.assertEqual(
            set(metrics["model"]),
            {"7-day seasonal naive", "7-day trailing mean"},
        )


if __name__ == "__main__":
    unittest.main()
