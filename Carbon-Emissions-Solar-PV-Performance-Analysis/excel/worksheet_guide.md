# Excel workbook guide

Use outputs/processed_energy_solar.csv as the source. Convert the imported range to an Excel Table named EnergySolar.

## Suggested sheets
- Raw_Data: imported source table.
- KPI_Summary: portfolio totals and selected-period metrics.
- Monthly_Trends: PivotTable and line charts.
- Site_Benchmarking: compare demand, grid electricity, solar contribution, EUI, and solar yield.
- Data_Quality: import outputs/data_quality_report.csv.

## Formulas
Total demand:
~~~excel
=SUM(EnergySolar[electricity_demand_kwh])
~~~

Total solar generation:
~~~excel
=SUM(EnergySolar[solar_generation_kwh])
~~~

Total estimated emissions:
~~~excel
=SUM(EnergySolar[estimated_grid_emissions_kg_co2e])
~~~

Solar contribution:
~~~excel
=IFERROR(SUM(EnergySolar[solar_used_on_site_kwh])/SUM(EnergySolar[electricity_demand_kwh]),0)
~~~

For period EUI, divide total electricity demand for the selected period by facility floor area. Do not sum daily EUI values.

## PivotTable ideas
- Rows: month; columns: site_id; values: sum of demand, solar generation, grid electricity, emissions.
- Rows: site_id; values: sum of demand, solar generation, estimated emissions.
- Use line charts for monthly trends and clustered bars for site comparisons.

Label the emission factor, source, year, unit, and reporting boundary in any real report. The default factor is illustrative.
