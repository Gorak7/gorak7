# Bot Monitoring & Failure Alert Tool

Python utility for importing exported RPA execution logs, validating the log contract, classifying incidents, persisting records, producing reports, and optionally sending SMTP alerts.

> Bundled logs and reports are synthetic demonstration data. The tool does not currently connect directly to Automation Anywhere Control Room. Export logs from an authorized A360 tenant to CSV first.

## Quick start
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/monitor.py --input data/execution_logs_demo.csv --out reports
```
Default database is SQLite (bot_monitor.db). Configure DATABASE_URL to use a provisioned SQLAlchemy-compatible database.

## Optional email alerts
Copy .env.example to .env, set SMTP host/port, username/password and sender/recipient, then run:
```bash
python src/monitor.py --input data/execution_logs_demo.csv --out reports --send-email
```
Email is disabled by default. Never commit .env or production credentials. SMTP failures are reported and cause a non-zero process exit.

## Dashboard
```bash
streamlit run dashboard/app.py
```
The dashboard uses synthetic bundled logs by default. Upload a sanitized A360-exported CSV to inspect actual logs.

## Required CSV columns
`run_id,bot_name,invoice_id,status,started_at,completed_at,duration_seconds,error_message`.
Statuses: SUCCESS, FAILED, COMPLETED, ERROR, TIMEOUT. Timestamps must be parseable and duration must be non-negative.

## Incident categories
DATA_ERROR, APPLICATION_ERROR, TIMEOUT, DATABASE_ERROR, FILE_SYSTEM_ERROR, AUTHENTICATION_ERROR, UNKNOWN_ERROR.

## Tests
From this project directory: `python -m pytest -q tests`. From repository root: `python -m pytest -q Bot-Monitoring-Failure-Alert-Tool/tests`.

## Integration limitations
See [INTEGRATION.md](docs/INTEGRATION.md). SQLite persistence is idempotent by (run_id, invoice_id). Non-SQLite databases currently use append-only persistence and require provisioned tables plus dialect-specific unique constraints before production use.

## Security
Use sanitized logs, protect invoice data, store secrets in a vault, and monitor only systems you are authorized to access.
