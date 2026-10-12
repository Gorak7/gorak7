"""Generate reproducible synthetic daily electricity and water readings."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def main():
    rng = np.random.default_rng(42)
    dates = pd.date_range("2024-01-01", periods=540, freq="D")
    sites = {
        "STORE_001": (720, 42),
        "STORE_002": (610, 36),
        "STORE_003": (850, 51),
        "WAREHOUSE_001": (1100, 24),
    }
    rows = []
    for site, (electric_base, water_base) in sites.items():
        for i, day in enumerate(dates):
            weekend = 0.86 if day.dayofweek >= 5 else 1.0
            season = 1.0 + 0.10 * np.sin(2 * np.pi * i / 365.25)
            electric = electric_base * weekend * season + rng.normal(0, electric_base * 0.055)
            water = water_base * weekend + rng.normal(0, water_base * 0.08)
            rows.append({
                "date": day.date().isoformat(),
                "site_id": site,
                "electricity_kwh": round(max(10, electric), 2),
                "water_m3": round(max(0.5, water), 2),
            })
    df = pd.DataFrame(rows)
    for site, date in [("STORE_001", "2024-05-12"), ("STORE_002", "2024-10-18"),
                       ("STORE_003", "2025-02-05")]:
        mask = (df.site_id == site) & (df.date == date)
        df.loc[mask, "electricity_kwh"] *= 1.9
    path = DATA_DIR / "utility_readings.csv"
    df.to_csv(path, index=False)
    print(f"Wrote {len(df):,} synthetic records to {path}")


if __name__ == "__main__":
    main()
