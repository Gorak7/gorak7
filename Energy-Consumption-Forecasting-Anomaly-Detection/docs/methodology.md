# Methodology and assumptions

## Data dictionary
- date: daily date for a synthetic reading.
- site_id: stable facility identifier.
- electricity_kwh: daily electricity consumption in kWh.
- water_m3: daily water consumption in cubic metres.

## Quality rules
The script reports missing/invalid values and duplicate date/site keys, then excludes rows missing required fields, duplicate keys, and non-positive values. In real facilities, zero can be valid; investigate before excluding it.

## Anomaly detection
For each site and metric, calculate a rolling median from up to 28 prior observations and a median absolute deviation (MAD). Scale MAD by 1.4826 and flag absolute robust z-scores >= 3.5. At least 14 prior observations are required. Zero MAD results in an undefined score and no flag.

## Forecasting
A 7-day seasonal-naive forecast predicts each holdout day using the value seven days earlier. The last 20% of the chronological series is held out. MAE and RMSE measure errors in kWh; MAPE is unstable around zero. This is a baseline, not a claim of best model performance.

## Operational cautions
Alerts require investigation. Check operating hours, weather, occupancy, maintenance, meter accuracy, billing periods, and facility changes before recommending action. Use walk-forward validation and contextual features for production forecasting.
