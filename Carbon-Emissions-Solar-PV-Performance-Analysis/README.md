# Carbon Emissions and Solar PV Performance Analysis

A reproducible sustainability analytics project combining facility electricity demand, solar photovoltaic generation, estimated grid electricity emissions, Energy Use Intensity (EUI), and solar yield.

**Data note:** The scripts generate synthetic data. The default grid emission factor is illustrative only. Replace it with a documented factor appropriate to the geography, reporting year, and accounting boundary before using real reporting.

## Features
- Synthetic daily facility demand and solar generation for multiple sites.
- Data-quality checks and consistent units.
- Grid electricity estimate assuming solar offsets demand first; no export or storage model.
- Estimated grid emissions, solar contribution, period EUI, and solar yield.
- Monthly site KPI export, charts, and Power BI / Excel instructions.

## Structure
~~~text
Carbon-Emissions-Solar-PV-Performance-Analysis/
├── README.md
├── requirements.txt
├── data/
├── outputs/
├── src/
│   ├── generate_data.py
│   └── analyze_sustainability.py
├── powerbi/dax_measures.md
└── excel/worksheet_guide.md
~~~

## Run
~~~bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py
python src/analyze_sustainability.py
~~~

## Outputs
- data/facility_energy_solar.csv
- outputs/processed_energy_solar.csv
- outputs/sustainability_kpis.csv
- outputs/data_quality_report.csv
- outputs/monthly_sustainability_trends.png
- outputs/solar_performance.png

## KPI definitions
- Grid electricity (kWh) = demand less solar used on site, with a zero floor.
- Solar contribution (%) = solar used on site / electricity demand.
- Estimated emissions (kg CO2e) = grid electricity × configured emission factor.
- Period EUI (kWh/m²) = total period electricity demand / floor area.
- Solar yield (kWh/kWp) = solar generation / installed capacity.
- Solar-vs-expected (%) compares generated energy with a configurable capacity-based expected-yield proxy.

## Power BI and Excel
Import outputs/processed_energy_solar.csv into Power BI and use powerbi/dax_measures.md. For Excel, convert the CSV to a Table and follow excel/worksheet_guide.md.

## Limitations
This is not an audited greenhouse-gas inventory or engineering-grade PV simulation. It excludes exports, batteries, certificates, market-based Scope 2 accounting, lifecycle emissions, and detailed weather/irradiance modeling. Document emission-factor source, year, unit, and boundary in any real report.
