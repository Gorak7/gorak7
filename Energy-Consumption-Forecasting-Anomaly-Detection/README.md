# Energy Consumption Forecasting and Anomaly Detection

A reproducible Python + SQL project for facility-level electricity and water analysis, anomaly review, forecasting, and reporting.

**Data note:** The generator creates synthetic demo data. Outputs are illustrative, not actual facility measurements or verified savings.

## Features
- Synthetic daily readings for multiple facilities.
- Data-quality checks for missing values, duplicate records, invalid dates, non-positive consumption, and retained/rejected row counts.
- Rolling-median / median-absolute-deviation anomaly flags using prior observations only, including a documented zero-MAD fallback.
- Site-level chronological holdout evaluation with a 7-day seasonal-naive forecasting baseline.
- MAE, RMSE, and MAPE metrics per site, charts, CSV outputs, and SQLite tables.

## Structure
```text
Energy-Consumption-Forecasting-Anomaly-Detection/
├── README.md
├── requirements.txt
├── data/
├── outputs/
├── src/
│   ├── generate_data.py
│   └── analyze_energy.py
├── tests/
│   └── test_analysis.py
├── sql/schema_and_queries.sql
└── docs/methodology.md
```

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py
python src/analyze_energy.py
python -m unittest discover -s tests -v
```

## Outputs
- `data/utility_readings.csv`
- `outputs/clean_utility_readings.csv`
- `outputs/anomaly_flags.csv`
- `outputs/forecast_test_results.csv` (site-level holdout results)
- `outputs/forecast_metrics.csv` (metrics by site)
- `outputs/data_quality_report.csv` (includes rejected-row counts)
- `outputs/energy_analytics.db`
- `outputs/daily_consumption.png`
- `outputs/anomalies_by_site.png`
- `outputs/forecast_comparison_by_site.png`

## Method
1. Validate and clean records; deduplicate date/site combinations.
2. Calculate rolling median and robust z-score using prior readings only.
3. Flag absolute robust z-scores >= 3.5 after at least 14 prior observations; when MAD is zero, flag non-zero deviations for review.
4. Forecast each site's held-out period using both consumption from seven days earlier and the trailing seven-day mean; compare per-site metrics.
5. Evaluate with MAE, RMSE, and MAPE; store analysis tables in SQLite.

An anomaly is an investigation signal, not proof of wastage or equipment failure. Consider operating hours, weather, occupancy, meter quality, and maintenance before drawing conclusions. Compare other forecasting baselines before selecting a model for operational use.
