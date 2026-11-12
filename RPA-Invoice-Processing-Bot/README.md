# Invoice Processing Bot — Automation Anywhere A360

A portfolio implementation blueprint for an A360 Community Edition invoice workflow, with reproducible sample data, validation rules, SQL schema, and a local Python reference processor.

> **Evidence integrity:** bundled records are synthetic. The Python reference processor is runnable; the A360 bot must be built/imported and run in your own A360 Community Edition workspace. Do not describe the A360 workflow as executed until you capture your own run evidence.

## What it demonstrates
- Folder-based invoice intake (CSV/XLSX; PDF extraction via A360 document/OCR actions)
- Required-field, amount, GST-format, and duplicate-invoice validation
- Accepted/rejected routing and exception reasons
- SQL persistence and structured execution logs
- Daily summary output for email delivery

## Quick start (reference processor)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/process_invoices.py --input data/invoices_demo.csv --out output
```
The reference processor writes `processed_invoices.csv`, `invoice_exceptions.csv`, `execution_logs.csv`, and a summary. SQLite is used by default; set `DATABASE_URL` for a SQLAlchemy-supported database.

## A360 implementation
Follow [A360_BUILD_GUIDE.md](docs/A360_BUILD_GUIDE.md). Use a dedicated input/archive/error folder and configure credentials through A360 Credential Vault, never hard-code passwords.

## Data contract
Required columns: `invoice_id,vendor_name,invoice_date,due_date,gst_number,amount,tax_amount,currency,source_file`.
Rules: non-empty invoice/vendor/date/GST; positive amount; amount numeric; GST format check; duplicate invoice ID rejected within the batch. GST validation is a demo format check, not a government verification.

## Evidence to capture after your own A360 run
1. Bot task editor showing the workflow and exception branches.
2. Input folder before/after processing.
3. A360 run details and execution log.
4. Accepted output and exception report.
5. SQL query results and daily email received (if configured).

## Repository layout
- `src/process_invoices.py`: runnable reference processor.
- `data/invoices_demo.csv`: synthetic test invoices.
- `database/schema.sql`: MySQL schema.
- `docs/A360_BUILD_GUIDE.md`: A360 build steps and control flow.
- `evidence/README.md`: evidence capture checklist.

MIT License.
