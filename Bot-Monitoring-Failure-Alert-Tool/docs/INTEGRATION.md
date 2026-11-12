# A360 → CSV → Python monitoring integration

1. In A360, write one log row per invoice/run to a CSV using the agreed schema.
2. Include stable run ID, bot name, invoice ID, status, timestamps, duration, and error text.
3. Export/copy the CSV to the monitoring machine's input folder after each run or on a schedule.
4. Run: `python src/monitor.py --input path/to/a360_execution_logs.csv --out reports`.
5. Review failure_analysis.csv and daily_monitoring_summary.csv.
6. To enable SMTP, set SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, MAIL_FROM, MAIL_TO in environment variables and explicitly pass --send-email.
7. For continuous monitoring, schedule the command with Windows Task Scheduler or cron. Avoid overlapping runs; archive processed logs.

## Production hardening backlog
- Add an authenticated ingestion API or queue instead of shared-folder polling.
- Add idempotency key (run_id + invoice_id) to avoid duplicate DB rows.
- Add retry/backoff for transient DB/SMTP errors.
- Store secrets in a vault; encrypt data in transit and at rest.
- Add role-based access and audit trail before multi-user deployment.
- Connect A360 Control Room API only after confirming tenant/API access and authorization.
