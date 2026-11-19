# Carbon Emissions and Solar PV Performance Analysis

A reproducible sustainability analytics project combining facility electricity demand, solar photovoltaic generation, estimated grid electricity emissions, Energy Use Intensity (EUI), and solar yield.

**Data note:** The scripts generate synthetic data. The default grid emission factor is illustrative only. Replace it with a documented factor appropriate to the geography, reporting year, and accounting boundary before using real reporting.

## Features
- Synthetic daily facility demand and solar generation for multiple sites.
- Data-quality checks with input, retained, and rejected row counts.
- Grid electricity estimate assuming solar offsets demand first; no export or storage model.
- Estimated grid emissions, solar contribution, period EUI, and solar yield.
- Monthly site KPI export, genuinely monthly portfolio charts, and Power BI / Excel guidance.

## Structure
```text
Carbon-Emissions-Solar-PV-Performance-Analysis/
├── README.md
├── requirements.txt
├── data/
├── outputs/
├── src/
│   ├── generate_data.py
│   └── analyze_sustainability.py
├── tests/
│   └── test_analysis.py
├── powerbi/dax_measures.md
└── excel/worksheet_guide.md
```

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py
python src/analyze_sustainability.py
python -m unittest discover -s tests -v
```

## Outputs
- `data/facility_energy_solar.csv`
- `outputs/processed_energy_solar.csv`
- `outputs/sustainability_kpis.csv`
- `outputs/data_quality_report.csv` (includes rejected-row counts)
- `outputs/monthly_sustainability_trends.png` (monthly portfolio values)
- `outputs/solar_performance.png`

## KPI definitions
- Grid electricity (kWh) = demand less solar used on site, with a zero floor.
- Solar contribution (%) = solar used on site / electricity demand.
- Estimated emissions (kg CO2e) = grid electricity × configured emission factor.
- Period EUI (kWh/m²) = total period electricity demand / floor area.
- Solar yield (kWh/kWp) = solar generation / installed capacity.
- Solar-vs-expected (%) compares generated energy with a configurable capacity-based expected-yield proxy.

## Power BI and Excel
Import `outputs/processed_energy_solar.csv` into Power BI and use `powerbi/dax_measures.md`. The DAX measures count each site's capacity and floor area once. For Excel, follow `excel/worksheet_guide.md`.

The repository contains chart outputs and dashboard guidance, not a completed Power BI `.pbix` file. Build and save the report in Power BI Desktop, then add genuine screenshots before describing it as a completed dashboard.

## Limitations
This is not an audited greenhouse-gas inventory or engineering-grade PV simulation. It excludes exports, batteries, certificates, market-based Scope 2 accounting, lifecycle emissions, and detailed weather/irradiance modelling. Document emission-factor source, year, unit, and boundary in any real report.
