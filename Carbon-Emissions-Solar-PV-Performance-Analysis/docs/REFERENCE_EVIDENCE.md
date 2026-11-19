# Reference research and evidence

This document records public repositories reviewed as learning and design references while planning this independent project. They are **not dependencies, data sources, copied implementations, or endorsements**. The project code, synthetic datasets, metrics, and visualisations in this repository are independently developed. No numerical results or screenshots from these repositories are represented as our own.

## Energy consumption, forecasting and anomaly detection

1. **[GlawinAlva24/Energy-Consumption-Forecasting-Anomaly-Detection](https://github.com/GlawinAlva24/Energy-Consumption-Forecasting-Anomaly-Detection)** — Hybrid forecasting with SWT-LSTM and multiple unsupervised anomaly detectors; use as methodological comparison context.
2. **[jaira26/SMART-GRID-ENERGY-ANALYTICS](https://github.com/jaira26/SMART-GRID-ENERGY-ANALYTICS)** — Smart-meter analytics combining data-quality checks, Isolation Forest anomaly detection and demand forecasting.
3. **[frederikcodes/energy-forecasting](https://github.com/frederikcodes/energy-forecasting)** — Time-series forecasting comparison across SARIMA, Prophet and LSTM with MAE/RMSE evaluation.
4. **[mfgray/Timeseries-anomaly-detection](https://github.com/mfgray/Timeseries-anomaly-detection)** — Forecast-interval and sustained-deviation approaches for detecting abnormal electricity-use patterns.
5. **[furkanak1n/energy-consumption-forecasting](https://github.com/furkanak1n/energy-consumption-forecasting)** — Comparative energy-demand forecasting using ARIMA, Prophet and LSTM.

## Carbon, solar PV and sustainability analytics

6. **[Azizi-Salma/CO2-Analyst](https://github.com/Azizi-Salma/CO2-Analyst)** — Interactive carbon-emissions exploration, country filters, historical trends and CSV export.
7. **[jasonjowtien/PV_Performance_Analysis](https://github.com/jasonjowtien/PV_Performance_Analysis)** — Solar PV performance-ratio analysis, irradiance data and time-based performance visualisation.
8. **[evinnisa35/solar-power-generation-analysis](https://github.com/evinnisa35/solar-power-generation-analysis)** — Solar power generation exploratory analysis reference; README content could not be independently retrieved during this review, so inspect before relying on implementation details.
9. **[Musthafa-D/Solar-operations-analytics](https://github.com/Musthafa-D/Solar-operations-analytics)** — PV telemetry quality, forecasting baselines, residual anomalies, data provenance and automated tests.
10. **[brinesolution/solar-pv-forecasting](https://github.com/brinesolution/solar-pv-forecasting)** — Physics-guided XGBoost solar forecasting using weather, solar geometry and plant context.
11. **[reyhancankaya/Global-Sustainability-Data-Project](https://github.com/reyhancankaya/Global-Sustainability-Data-Project)** — Synthetic sustainability analytics with Python, Excel and Tableau executive KPI dashboards.

## How these references informed the project

- Forecasting: compare simple chronological baselines and report error metrics rather than presenting an unvalidated forecast as operational.
- Anomaly review: show flagged observations in context and distinguish an investigation signal from a confirmed fault.
- Data quality: make rejected rows, missing values and duplicate keys visible.
- Solar analytics: separate energy generation, onsite use, grid import, yield and performance-ratio concepts.
- Sustainability reporting: communicate assumptions, units, filters and KPI definitions alongside charts.
- Dashboard UX: provide interactive filters, comparison views and downloadable filtered data.

Not every technique in the reference repositories is implemented here. In particular, the current Python projects use their documented methods and synthetic input data; the dashboard should only describe capabilities supported by the CSV outputs actually loaded.

## Our project repositories

- [Carbon Emissions & Solar PV Performance Analysis](https://github.com/Gorak7/gorak7/tree/main/Carbon-Emissions-Solar-PV-Performance-Analysis)
- [Energy Consumption Forecasting & Anomaly Detection](https://github.com/Gorak7/gorak7/tree/main/Energy-Consumption-Forecasting-Anomaly-Detection)

## Evidence integrity

- Reference links are provided for attribution and further learning.
- The project is independently implemented; there is no affiliation with or endorsement by the referenced authors.
- The current datasets are synthetic demonstration data. Do not claim real-world savings, measured facility performance, or validated emissions inventory results.
- Dashboard screenshots, if added later, must be captured from the actual running dashboard and must identify demo data or user-uploaded outputs accurately.
