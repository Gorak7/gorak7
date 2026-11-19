# Power BI dashboard guide

Import `outputs/processed_energy_solar.csv` and name the table `EnergySolar`. Set `date` to Date type and numeric columns to numeric types. Create a one-to-many date table relationship if using a dedicated calendar.

## Measures

```DAX
Total Demand (kWh) =
SUM(EnergySolar[electricity_demand_kwh])

Solar Generation (kWh) =
SUM(EnergySolar[solar_generation_kwh])

Solar Used On Site (kWh) =
SUM(EnergySolar[solar_used_on_site_kwh])

Grid Electricity (kWh) =
SUM(EnergySolar[grid_electricity_kwh])

Estimated Grid Emissions (kg CO2e) =
SUM(EnergySolar[estimated_grid_emissions_kg_co2e])

Solar Contribution (%) =
DIVIDE(
    [Solar Used On Site (kWh)],
    [Total Demand (kWh)]
)

Installed Solar Capacity (kWp) =
SUMX(
    VALUES(EnergySolar[site_id]),
    CALCULATE(MAX(EnergySolar[solar_capacity_kwp]))
)

Solar Yield (kWh/kWp) =
DIVIDE(
    [Solar Generation (kWh)],
    [Installed Solar Capacity (kWp)]
)

Period EUI (kWh/m2) =
DIVIDE(
    [Total Demand (kWh)],
    SUMX(
        VALUES(EnergySolar[site_id]),
        CALCULATE(MAX(EnergySolar[floor_area_m2]))
    )
)
```

The capacity and floor-area measures count each selected site once, rather than summing the repeated daily values. Format Solar Contribution as Percentage.

## Suggested report pages
- Executive Overview: cards for demand, solar generation, grid electricity, solar contribution, and estimated emissions.
- Site Benchmarking: compare site demand, period EUI, and solar contribution.
- Solar Performance: monthly generation and yield by site.
- Emissions Trend: monthly estimated emissions.
- Slicers: site, year, and month.

The Python output includes sample charts, not a finished Power BI report. Save the completed report as `dashboard/energy_solar_performance.pbix` and add genuine screenshots to `screenshots/` after building it in Power BI Desktop.

Treat emissions as estimates using the configured factor, not audited inventory values.
