# Methodology and assumptions

## Data dictionary
- `date`: daily date for a synthetic reading.
- `site_id`: stable facility identifier.
- `electricity_kwh`: daily electricity consumption in kWh.
- `water_m3`: daily water consumption in cubic metres.

## Data quality
The analysis reports invalid dates, missing required values, duplicate date/site keys, and non-positive readings. It retains the first record for each date/site key and excludes invalid or incomplete rows. The report includes input, retained, and rejected row counts. In a real facility, a zero reading may be valid; investigate it before excluding it.

## Anomaly detection
For each site and metric, the script calculates a rolling median from up to 28 prior observations and a median absolute deviation (MAD). The scaled MAD is 1.4826 × MAD; absolute robust z-scores of 3.5 or higher are flagged. At least 14 prior observations are required. If the prior window has zero MAD, a non-zero deviation from the constant median is flagged for investigation. This fallback can be sensitive and should be reviewed with operational context.

## Forecasting
Two baselines are evaluated for each site: (1) 7-day seasonal naive, using the value seven days earlier, and (2) a trailing 7-day mean using the seven immediately preceding observations. The final 20% of each site’s chronological daily series is held out. The trailing mean is shifted by one day to avoid using the target day's value. Short gaps of up to two days are interpolated; longer gaps are excluded from the continuous series. MAE and RMSE measure errors in kWh; MAPE excludes zero actuals and can be unstable near zero. This is a baseline, not a claim of best model performance.

## Outputs and interpretation
Forecast metrics are reported separately for each site. Anomaly charts show site-level readings and flags on the same scale. Alerts are investigation signals, not proof of waste or equipment failure. Check operating hours, weather, occupancy, maintenance, meter accuracy, billing periods, and facility changes before recommending action.

For production forecasting, compare multiple baselines, use walk-forward validation, and consider contextual features.
