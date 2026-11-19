"""Calculate facility sustainability KPIs from synthetic demand and solar data."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "facility_energy_solar.csv"
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

# Illustrative only. Replace with a cited, geography/year-specific factor for real reporting.
GRID_EMISSION_FACTOR_KG_CO2E_PER_KWH = 0.70
EXPECTED_DAILY_YIELD_KWH_PER_KWP = 4.2

REQUIRED_COLUMNS = [
    "date", "site_id", "electricity_demand_kwh", "solar_generation_kwh",
    "solar_capacity_kwp", "floor_area_m2",
]


def prepare_data(raw: pd.DataFrame):
    """Validate input and return clean data plus a transparent quality summary."""
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(raw.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = raw.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    numeric = REQUIRED_COLUMNS[2:]
    for column in numeric:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    duplicate_rows = int(df.duplicated(["date", "site_id"], keep="first").sum())
    invalid_date_rows = int(df["date"].isna().sum())
    missing_rows = int(df[REQUIRED_COLUMNS].isna().any(axis=1).sum())
    invalid_numeric_rows = int(
        ((df["electricity_demand_kwh"] < 0)
         | (df["solar_generation_kwh"] < 0)
         | (df["solar_capacity_kwp"] <= 0)
         | (df["floor_area_m2"] <= 0)).fillna(False).sum()
    )
    before = len(df)
    clean = df.dropna(subset=REQUIRED_COLUMNS).copy()
    clean = clean.drop_duplicates(["date", "site_id"], keep="first")
    clean = clean[
        (clean["electricity_demand_kwh"] >= 0)
        & (clean["solar_generation_kwh"] >= 0)
        & (clean["solar_capacity_kwp"] > 0)
        & (clean["floor_area_m2"] > 0)
    ].sort_values(["site_id", "date"]).copy()

    quality = {
        "input_rows": before,
        "duplicate_date_site_rows": duplicate_rows,
        "invalid_date_rows": invalid_date_rows,
        "rows_with_missing_required_values": missing_rows,
        "rows_with_invalid_numeric_values": invalid_numeric_rows,
        "retained_rows": len(clean),
        "rejected_rows": before - len(clean),
    }
    return clean, quality


def calculate_monthly_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate monthly site KPIs without summing daily EUI or installed capacity."""
    monthly = df.groupby(
        [pd.Grouper(key="date", freq="MS"), "site_id"], as_index=False
    ).agg(
        electricity_demand_kwh=("electricity_demand_kwh", "sum"),
        solar_generation_kwh=("solar_generation_kwh", "sum"),
        solar_used_on_site_kwh=("solar_used_on_site_kwh", "sum"),
        grid_electricity_kwh=("grid_electricity_kwh", "sum"),
        estimated_grid_emissions_kg_co2e=("estimated_grid_emissions_kg_co2e", "sum"),
        floor_area_m2=("floor_area_m2", "first"),
        solar_capacity_kwp=("solar_capacity_kwp", "first"),
    )
    monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
    monthly["solar_contribution_pct"] = np.where(
        monthly["electricity_demand_kwh"] > 0,
        monthly["solar_used_on_site_kwh"] / monthly["electricity_demand_kwh"] * 100,
        np.nan,
    )
    monthly["period_eui_kwh_per_m2"] = (
        monthly["electricity_demand_kwh"] / monthly["floor_area_m2"]
    )
    monthly["solar_yield_kwh_per_kwp"] = (
        monthly["solar_generation_kwh"] / monthly["solar_capacity_kwp"]
    )
    return monthly


def main():
    if not DATA.exists():
        raise FileNotFoundError("Run python src/generate_data.py first.")

    raw = pd.read_csv(DATA)
    df, quality = prepare_data(raw)
    pd.DataFrame([quality]).to_csv(OUT / "data_quality_report.csv", index=False)
    if df.empty:
        raise ValueError("No valid records remain after data-quality checks.")

    # Assumption: solar offsets facility demand first. Exports and storage are not modelled.
    df["solar_used_on_site_kwh"] = np.minimum(
        df["solar_generation_kwh"], df["electricity_demand_kwh"]
    )
    df["grid_electricity_kwh"] = (
        df["electricity_demand_kwh"] - df["solar_used_on_site_kwh"]
    ).clip(lower=0)
    df["solar_contribution_pct"] = np.where(
        df["electricity_demand_kwh"] > 0,
        df["solar_used_on_site_kwh"] / df["electricity_demand_kwh"] * 100,
        np.nan,
    )
    df["estimated_grid_emissions_kg_co2e"] = (
        df["grid_electricity_kwh"] * GRID_EMISSION_FACTOR_KG_CO2E_PER_KWH
    )
    df["eui_kwh_per_m2_day"] = (
        df["electricity_demand_kwh"] / df["floor_area_m2"]
    )
    df["solar_yield_kwh_per_kwp"] = (
        df["solar_generation_kwh"] / df["solar_capacity_kwp"]
    )
    df["expected_solar_kwh"] = (
        df["solar_capacity_kwp"] * EXPECTED_DAILY_YIELD_KWH_PER_KWP
    )
    df["solar_vs_expected_pct"] = np.where(
        df["expected_solar_kwh"] > 0,
        df["solar_generation_kwh"] / df["expected_solar_kwh"] * 100,
        np.nan,
    )
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df.to_csv(OUT / "processed_energy_solar.csv", index=False)

    monthly = calculate_monthly_kpis(df)
    monthly.to_csv(OUT / "sustainability_kpis.csv", index=False)

    portfolio = df.groupby("date", as_index=False).agg(
        demand=("electricity_demand_kwh", "sum"),
        solar=("solar_generation_kwh", "sum"),
        emissions=("estimated_grid_emissions_kg_co2e", "sum"),
    )
    portfolio["month"] = portfolio["date"].dt.to_period("M").astype(str)
    monthly_portfolio = portfolio.groupby("month", as_index=False).agg(
        demand=("demand", "sum"),
        solar=("solar", "sum"),
        emissions=("emissions", "sum"),
    )
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
    axes[0].plot(monthly_portfolio["month"], monthly_portfolio["demand"], label="Demand")
    axes[0].plot(monthly_portfolio["month"], monthly_portfolio["solar"], label="Solar generation")
    axes[0].set_ylabel("kWh/month")
    axes[0].set_title("Monthly Portfolio Electricity Demand and Solar Generation")
    axes[0].legend()
    axes[1].plot(monthly_portfolio["month"], monthly_portfolio["emissions"])
    axes[1].set_ylabel("kg CO2e/month")
    axes[1].set_title("Monthly Estimated Grid Electricity Emissions")
    axes[1].tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(OUT / "monthly_sustainability_trends.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    for site, group in monthly.groupby("site_id"):
        ax.plot(group["month"], group["solar_yield_kwh_per_kwp"], marker="o", label=site)
    ax.set(title="Monthly Solar Yield by Site", xlabel="Month", ylabel="kWh/kWp per month")
    ax.tick_params(axis="x", rotation=60)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "solar_performance.png", dpi=150)
    plt.close(fig)

    print(f"Analysis complete. Retained {len(df):,} of {len(raw):,} rows.")
    print(f"Rejected rows: {quality['rejected_rows']:,}")
    print(f"Emission factor: {GRID_EMISSION_FACTOR_KG_CO2E_PER_KWH} kg CO2e/kWh (illustrative)")
    print(f"Outputs: {OUT}")


if __name__ == "__main__":
    main()
