# Energy Consumption Forecasting and Anomaly Detection

A reproducible Python + SQL project for facility-level electricity and water analysis, anomaly review, forecasting, and reporting.

**Data note:** The generator creates synthetic demo data. Outputs are illustrative, not actual store measurements or verified savings.

## Features
- Synthetic daily readings for multiple facilities.
- Data-quality checks for missing values, duplicate records, invalid dates, and non-positive consumption.
- Rolling-median / median-absolute-deviation anomaly flags using prior observations only.
- Chronological holdout evaluation with a 7-day seasonal-naive forecast baseline.
- MAE, RMSE, and MAPE metrics, charts, CSV outputs, and SQLite tables.

## Structure
~~~text
Energy-Consumption-Forecasting-Anomaly-Detection/
├── README.md
├── requirements.txt
├── data/                 # generated input CSV
├── outputs/              # generated reports, charts, SQLite DB
├── src/
│   ├── generate_data.py
│   └── analyze_energy.py
├── sql/schema_and_queries.sql
└── docs/methodology.md
~~~

## Run
~~~bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py
python src/analyze_energy.py
~~~

## Outputs
- data/utility_readings.csv
- outputs/clean_utility_readings.csv
- outputs/anomaly_flags.csv
- outputs/forecast_test_results.csv
- outputs/forecast_metrics.csv
- outputs/data_quality_report.csv
- outputs/energy_analytics.db
- outputs/daily_consumption.png, anomalies.png, forecast_comparison.png

## Method
1. Validate and clean records; deduplicate date/site combinations.
2. Aggregate daily readings and calculate rolling median and robust z-score.
3. Flag absolute robust z-scores >= 3.5 after at least 14 prior observations.
4. Forecast the held-out period using consumption from seven days earlier.
5. Evaluate with MAE, RMSE, and MAPE; store analysis tables in SQLite.

An anomaly is an investigation signal, not proof of wastage or equipment failure. Consider operating hours, weather, occupancy, meter quality, and maintenance before drawing conclusions. Extend the project with weather features, walk-forward validation, and Power BI.

## License
MIT.
