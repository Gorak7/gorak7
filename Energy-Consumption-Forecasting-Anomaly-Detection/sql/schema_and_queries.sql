-- Run these queries after analyze_energy.py creates outputs/energy_analytics.db.
SELECT strftime('%Y-%m', date) AS month,
       ROUND(SUM(electricity_kwh), 2) AS electricity_kwh,
       ROUND(SUM(water_m3), 2) AS water_m3
FROM utility_readings
GROUP BY strftime('%Y-%m', date)
ORDER BY month;

SELECT site_id,
       ROUND(AVG(electricity_kwh), 2) AS avg_daily_kwh,
       ROUND(MAX(electricity_kwh), 2) AS peak_daily_kwh
FROM utility_readings
GROUP BY site_id
ORDER BY avg_daily_kwh DESC;

SELECT date, site_id, metric, actual, baseline_median, robust_z_score
FROM anomaly_flags
WHERE is_anomaly = 1
ORDER BY ABS(robust_z_score) DESC;

SELECT * FROM data_quality_report;
