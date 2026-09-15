# US Healthcare Demand Forecasting with Machine Learning

**Python | Pandas | NumPy | Statistics | Time Series | scikit-learn | Matplotlib**

An end-to-end portfolio project using **synthetic US healthcare demand data** to demonstrate data preprocessing, trend analysis, time-series forecasting, machine learning, model evaluation, and visualization.

> **Important:** The dataset is synthetic and does not contain real patient information, PHI, or clinical records. The project demonstrates technical skills in a US healthcare-domain scenario; it is not evidence of professional US healthcare experience.

## Project Objectives

- Prepare and validate healthcare demand time-series data
- Analyze demand trends using rolling statistics
- Build an ML forecasting baseline using Linear Regression
- Use chronological train/test splitting to reduce time-series leakage
- Evaluate predictions using MAE, RMSE, and MAPE
- Generate a six-month demand forecast
- Visualize historical demand and model predictions

## Healthcare Domain

The project models **monthly patient demand/volume** for a hypothetical US healthcare service. This type of forecasting can support operational planning such as staffing, capacity planning, and resource allocation. It intentionally uses aggregated synthetic demand rather than individual patient data.

## Machine Learning Workflow

1. Load synthetic healthcare demand data.
2. Parse dates and validate numeric demand values.
3. Sort observations chronologically and remove invalid rows.
4. Create a month-index feature and 3-month rolling trend.
5. Split the dataset chronologically into training and testing sets.
6. Train a `LinearRegression` forecasting model with scikit-learn.
7. Predict demand for the held-out test period.
8. Evaluate using MAE, RMSE, and MAPE.
9. Forecast the next six months.
10. Visualize historical demand and forecast results.

## Project Structure

```text
Sales-Healthcare-Forecasting/
├── data/
│   └── healthcare_demand.csv
├── src/
│   └── forecasting.py
├── visualizations/
├── requirements.txt
├── LICENSE
└── README.md
```

## Run Locally

```bash
git clone https://github.com/Gorak7/gorak7.git
cd gorak7/Sales-Healthcare-Forecasting
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\\Scripts\\activate      # Windows
pip install -r requirements.txt
python src/forecasting.py
```

The script prints **MAE, RMSE, MAPE**, and the next six-month forecast, then displays the forecast visualization.

## Technologies

- Python
- Pandas
- NumPy
- scikit-learn
- Matplotlib
- Statistics / Time-Series Analysis

## Resume-Ready Project Description

**US Healthcare Demand Forecasting | Python, Pandas, NumPy, scikit-learn, Matplotlib**

- Built an ML-based forecasting pipeline using synthetic US healthcare demand data, including preprocessing, trend analysis, chronological train/test splitting, and feature engineering.
- Developed a Linear Regression forecasting model and evaluated performance using MAE, RMSE, and MAPE while generating six-month demand forecasts and visualizations.

## License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.
