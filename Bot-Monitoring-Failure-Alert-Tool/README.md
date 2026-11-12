# Bot Monitoring & Failure Alert Tool

Python monitoring utility for the invoice bot. Reads execution-log CSV files, classifies failures, stores runs/incidents in SQLite (or configured SQLAlchemy database), exports daily reports, and optionally sends SMTP alerts.

> Bundled logs and reports are synthetic demonstration data. SMTP is disabled unless configured. This tool does not connect to A360 Control Room directly; export A360 execution logs to the documented CSV format first.

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/monitor.py --input data/execution_logs_demo.csv --out reports
```
Default database: `sqlite:///bot_monitor.db`. Set `DATABASE_URL` for MySQL, and configure SMTP variables only if you want real email alerts. Use `--send-email` to opt in.

## Dashboard
```bash
streamlit run dashboard/app.py
```
The Streamlit dashboard loads the bundled sample CSVs; upload your own log CSV to inspect actual exported runs.

## Expected log columns
`run_id,bot_name,invoice_id,status,started_at,completed_at,duration_seconds,error_message`.
Accepted status values: SUCCESS, FAILED, COMPLETED, ERROR, TIMEOUT.

## Failure categories
DATA_ERROR, APPLICATION_ERROR, TIMEOUT, DATABASE_ERROR, FILE_SYSTEM_ERROR, AUTHENTICATION_ERROR, UNKNOWN_ERROR.

## Tests
```bash
pytest -q
```

## Lovable dashboard workspace
A Lovable project shell was created for the visual operations console: [FlowOps Operations Console](https://lovable.dev/projects/18544cd7-df22-4cc5-af5d-297389a8f1b2). Its AI build turn is pending because the Lovable workspace currently reports no remaining credits. The Streamlit dashboard in this repository is runnable now; the Lovable UI can be completed after credits are available.

## Security
Never commit real invoices, credentials, SMTP passwords, or production logs. Use environment variables and sanitized logs. Monitor only systems you are authorized to monitor.
