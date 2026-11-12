# Invoice Processing Bot — Automation Anywhere A360

Portfolio blueprint for building an invoice-processing workflow in Automation Anywhere A360, with a runnable Python reference processor, synthetic test data, validation rules and a database schema.

> Bundled input/output records are synthetic. The Python reference processor is runnable locally. The A360 task itself still needs to be built and run in your authorized A360 Community workspace before claiming A360 execution evidence.

## Capabilities
- CSV/XLSX invoice intake in the Python reference processor; PDF/OCR extraction belongs in the A360 workflow.
- Required-field, GST-format, positive amount, non-negative tax, date-order and currency validation.
- Duplicate invoice detection within a batch.
- Accepted/rejected CSV reports, structured execution logs and daily summary.
- SQLite persistence by default; MySQL schema is supplied.

## Quick start
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/process_invoices.py --input data/invoices_demo.csv --out output
```
Set DATABASE_URL to select a database. SQLite writes are idempotent by invoice ID. The MySQL schema uses a unique invoice ID and the reference processor uses INSERT IGNORE for accepted rows.

## Required input columns
`invoice_id,vendor_name,invoice_date,due_date,gst_number,amount,tax_amount,currency,source_file`.
GST validation checks format only; it does not verify registration against government services.

## A360 workflow
Follow [A360_BUILD_GUIDE.md](docs/A360_BUILD_GUIDE.md). Use A360 Credential Vault for secrets, parameterized database actions, exception branches, and explicit handling for OCR, email and file-system failures.

## Evidence checklist
Capture genuine screenshots from your own A360 run: bot task, input folder, execution details, accepted/rejected outputs, database results and actual email inbox if configured. Do not present synthetic CSVs or Python output as A360 execution evidence.

MIT License.
