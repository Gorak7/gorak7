import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analyze_sustainability import calculate_monthly_kpis, prepare_data


class SustainabilityAnalysisTests(unittest.TestCase):
    def test_quality_report_counts_rejected_rows(self):
        raw = pd.DataFrame([
            {"date": "2025-01-01", "site_id": "A", "electricity_demand_kwh": 10,
             "solar_generation_kwh": 5, "solar_capacity_kwp": 2, "floor_area_m2": 100},
            {"date": "not-a-date", "site_id": "A", "electricity_demand_kwh": 10,
             "solar_generation_kwh": 5, "solar_capacity_kwp": 2, "floor_area_m2": 100},
        ])
        clean, report = prepare_data(raw)
        self.assertEqual(len(clean), 1)
        self.assertEqual(report["input_rows"], 2)
        self.assertEqual(report["retained_rows"], 1)
        self.assertEqual(report["rejected_rows"], 1)

    def test_monthly_yield_uses_capacity_once(self):
        data = pd.DataFrame({
            "date": pd.to_datetime(["2025-01-01", "2025-01-02"]),
            "site_id": ["A", "A"],
            "electricity_demand_kwh": [20, 20],
            "solar_generation_kwh": [10, 10],
            "solar_used_on_site_kwh": [10, 10],
            "grid_electricity_kwh": [10, 10],
            "estimated_grid_emissions_kg_co2e": [7, 7],
            "floor_area_m2": [100, 100],
            "solar_capacity_kwp": [2, 2],
        })
        result = calculate_monthly_kpis(data).iloc[0]
        self.assertAlmostEqual(result["solar_yield_kwh_per_kwp"], 10.0)
        self.assertAlmostEqual(result["period_eui_kwh_per_m2"], 0.4)


if __name__ == "__main__":
    unittest.main()
