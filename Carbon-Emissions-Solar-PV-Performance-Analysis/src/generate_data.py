"""Generate synthetic facility electricity and solar PV data."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def main():
    rng = np.random.default_rng(7)
    dates = pd.date_range("2025-01-01", periods=365, freq="D")
    sites = {
        "STORE_001": {"demand": 760, "capacity_kwp": 95, "area_m2": 2800},
        "STORE_002": {"demand": 640, "capacity_kwp": 80, "area_m2": 2300},
        "STORE_003": {"demand": 900, "capacity_kwp": 120, "area_m2": 3400},
    }
    rows = []
    for site, cfg in sites.items():
        for i, day in enumerate(dates):
            weekend = 0.88 if day.dayofweek >= 5 else 1.0
            demand = cfg["demand"] * weekend * (1 + 0.08 * np.sin(2 * np.pi * i / 365)) + rng.normal(0, 28)
            season = 0.62 + 0.38 * np.sin(np.pi * (i + 1) / 365)
            weather = rng.uniform(0.55, 1.12)
            solar = cfg["capacity_kwp"] * 4.2 * max(0.12, season) * weather
            rows.append({
                "date": day.date().isoformat(),
                "site_id": site,
                "electricity_demand_kwh": round(max(20, demand), 2),
                "solar_generation_kwh": round(max(0, solar), 2),
                "solar_capacity_kwp": cfg["capacity_kwp"],
                "floor_area_m2": cfg["area_m2"],
            })
    df = pd.DataFrame(rows)
    path = DATA_DIR / "facility_energy_solar.csv"
    df.to_csv(path, index=False)
    print(f"Wrote {len(df):,} synthetic rows to {path}")


if __name__ == "__main__":
    main()
