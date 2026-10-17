# Evidence Checklist

Capture evidence from a real local run. Use synthetic test data and never include real passwords, personal data, or secret tokens.

## Screenshots to capture
1. 01-dashboard.png — application UI with database-backed records.
2. 02-create-record.png — form before submitting synthetic data.
3. 03-update-record.png — updated record in the table.
4. 04-delete-record.png — record removed from the table.
5. 05-postman-positive.png — successful API response and assertion results.
6. 06-postman-negative-auth.png — missing/invalid API key returns 401.
7. 07-postman-validation.png — invalid payload or duplicate email response.
8. 08-sql-validation.png — SQL validation query results.
9. 09-test-run-summary.png — actual Postman collection run summary.

## Reports
Export the Postman run report to reports/postman-run.json. Add reports/execution-summary.md with run date, environment, total/passed/failed/blocked counts, defects and evidence links. Update CSV execution statuses only after running tests.

## Evidence integrity
No fabricated screenshots, test results, or performance metrics. Tests not run must remain Not Run.
