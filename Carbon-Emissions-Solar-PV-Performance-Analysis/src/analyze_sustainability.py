"""Calculate facility sustainability KPIs from synthetic demand and solar data."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "facility_energy_solar.csv"
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

# Illustrative only. Replace with a cited, geography/year-specific factor for real reporting.
GRID_EMISSION_FACTOR_KG_CO2E_PER_KWH = 0.70
EXPECTED_DAILY_YIELD_KWH_PER_KWP = 4.2


def main():
    if not DATA.exists():
        raise FileNotFoundError("Run python src/generate_data.py first.")
    df = pd.read_csv(DATA, parse_dates=["date"])
    required = ["date", "site_id", "electricity_demand_kwh", "solar_generation_kwh",
                "solar_capacity_kwp", "floor_area_m2"]
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    for col in required[2:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    quality = {
        "input_rows": len(df),
        "duplicate_date_site": int(df.duplicated(["date", "site_id"]).sum()),
        "rows_with_missing_values": int(df[required].isna().any(axis=1).sum()),
        "negative_demand": int((df.electricity_demand_kwh < 0).sum()),
        "negative_solar": int((df.solar_generation_kwh < 0).sum()),
        "nonpositive_capacity": int((df.solar_capacity_kwp <= 0).sum()),
        "nonpositive_floor_area": int((df.floor_area_m2 <= 0).sum()),
    }
    pd.DataFrame([quality]).to_csv(OUT / "data_quality_report.csv", index=False)
    df = df.dropna(subset=required).drop_duplicates(["date", "site_id"]).copy()
    df = df[(df.electricity_demand_kwh >= 0) & (df.solar_generation_kwh >= 0)
            & (df.solar_capacity_kwp > 0) & (df.floor_area_m2 > 0)].copy()

    # Assumption: solar offsets facility demand first. Exports and storage are not modeled.
    df["solar_used_on_site_kwh"] = np.minimum(df.solar_generation_kwh, df.electricity_demand_kwh)
    df["grid_electricity_kwh"] = (df.electricity_demand_kwh - df.solar_used_on_site_kwh).clip(lower=0)
    df["solar_contribution_pct"] = np.where(
        df.electricity_demand_kwh > 0,
        df.solar_used_on_site_kwh / df.electricity_demand_kwh * 100, np.nan)
    df["estimated_grid_emissions_kg_co2e"] = df.grid_electricity_kwh * GRID_EMISSION_FACTOR_KG_CO2E_PER_KWH
    df["eui_kwh_per_m2_day"] = df.electricity_demand_kwh / df.floor_area_m2
    df["solar_yield_kwh_per_kwp"] = df.solar_generation_kwh / df.solar_capacity_kwp
    df["expected_solar_kwh"] = df.solar_capacity_kwp * EXPECTED_DAILY_YIELD_KWH_PER_KWP
    df["solar_vs_expected_pct"] = np.where(
        df.expected_solar_kwh > 0, df.solar_generation_kwh / df.expected_solar_kwh * 100, np.nan)
    df["month"] = df.date.dt.to_period("M").astype(str)
    df.to_csv(OUT / "processed_energy_solar.csv", index=False)

    monthly = df.groupby(["month", "site_id"], as_index=False).agg(
        electricity_demand_kwh=("electricity_demand_kwh", "sum"),
        solar_generation_kwh=("solar_generation_kwh", "sum"),
        grid_electricity_kwh=("grid_electricity_kwh", "sum"),
        estimated_grid_emissions_kg_co2e=("estimated_grid_emissions_kg_co2e", "sum"),
        floor_area_m2=("floor_area_m2", "first"),
        solar_capacity_kwp=("solar_capacity_kwp", "first"))
    monthly["solar_contribution_pct"] = np.where(
        monthly.electricity_demand_kwh > 0,
        np.minimum(monthly.solar_generation_kwh, monthly.electricity_demand_kwh)
        / monthly.electricity_demand_kwh * 100, np.nan)
    monthly["period_eui_kwh_per_m2"] = monthly.electricity_demand_kwh / monthly.floor_area_m2
    monthly["solar_yield_kwh_per_kwp"] = monthly.solar_generation_kwh / monthly.solar_capacity_kwp
    monthly.to_csv(OUT / "sustainability_kpis.csv", index=False)

    portfolio = df.groupby("date", as_index=False).agg(
        demand=("electricity_demand_kwh", "sum"),
        solar=("solar_generation_kwh", "sum"),
        emissions=("estimated_grid_emissions_kg_co2e", "sum"))
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
    axes[0].plot(portfolio.date, portfolio.demand, label="Demand")
    axes[0].plot(portfolio.date, portfolio.solar, label="Solar generation")
    axes[0].set_ylabel("kWh/day")
    axes[0].set_title("Portfolio Electricity Demand and Solar Generation")
    axes[0].legend()
    axes[1].plot(portfolio.date, portfolio.emissions)
    axes[1].set_ylabel("kg CO2e/day")
    axes[1].set_title("Estimated Grid Electricity Emissions")
    fig.tight_layout()
    fig.savefig(OUT / "monthly_sustainability_trends.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    for site, group in monthly.groupby("site_id"):
        ax.plot(group.month, group.solar_yield_kwh_per_kwp, marker="o", label=site)
    ax.set(title="Monthly Solar Yield by Site", xlabel="Month", ylabel="kWh/kWp per month")
    ax.tick_params(axis="x", rotation=60)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "solar_performance.png", dpi=150)
    plt.close(fig)
    print(f"Analysis complete. Retained {len(df):,} rows.")
    print(f"Emission factor: {GRID_EMISSION_FACTOR_KG_CO2E_PER_KWH} kg CO2e/kWh (illustrative)")
    print(f"Outputs: {OUT}")


if __name__ == "__main__":
    main()
