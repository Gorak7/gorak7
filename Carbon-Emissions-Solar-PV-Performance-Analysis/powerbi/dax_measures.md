# Power BI dashboard guide

Import outputs/processed_energy_solar.csv and name the table EnergySolar. Set date to Date type and numeric columns to numeric types.

~~~DAX
Total Demand (kWh) =
SUM(EnergySolar[electricity_demand_kwh])

Solar Generation (kWh) =
SUM(EnergySolar[solar_generation_kwh])

Grid Electricity (kWh) =
SUM(EnergySolar[grid_electricity_kwh])

Estimated Grid Emissions (kg CO2e) =
SUM(EnergySolar[estimated_grid_emissions_kg_co2e])

Solar Contribution (%) =
DIVIDE(
    SUM(EnergySolar[solar_used_on_site_kwh]),
    SUM(EnergySolar[electricity_demand_kwh])
)

Solar Yield (kWh/kWp) =
DIVIDE(
    SUM(EnergySolar[solar_generation_kwh]),
    SUM(EnergySolar[solar_capacity_kwp])
)
~~~

Format Solar Contribution as Percentage. The Solar Yield measure above is suitable for quick exploration but summing installed capacity across daily rows can overcount capacity. Use the monthly KPI export or a separate site-capacity dimension for robust reporting.

## Suggested report pages
- Executive Overview: KPI cards for demand, solar generation, grid electricity, estimated emissions.
- Site Benchmarking: site comparison bars and period EUI.
- Solar Performance: monthly solar generation and yield by site.
- Emissions Trend: estimated emissions over time.
- Slicers: site, year, and month.

Treat emissions as estimates using the configured factor, not audited inventory values.
