# RPA Invoice Processing Bot — Automation Anywhere A360

An end-to-end invoice automation portfolio project. The repository contains a Python reference runner and a detailed A360 implementation blueprint. Use the reference runner to exercise file handling, extraction, validation, routing, persistence and reporting locally; build and execute the actual bot in your own A360 Community workspace for platform evidence.

## End-to-end workflow

`Input → Working → extract → validate supplier/invoice → duplicate check → Approved / Review / Rejected → database → reports → email`

The folders are created automatically under the workspace root:
- `Input/`: incoming PDF invoices and/or a CSV/XLSX manifest
- `Working/`: temporary working copies
- `Approved/`, `Review/`, `Rejected/`: routed source files
- `Exceptions/`: reserved for unreadable/corrupt source files and A360 file-level exceptions
- `Logs/`: rotating execution log
- `Reports/`: CSV, XLSX, PDF and JSON processing reports
- `database/`: SQLite database

## Implemented in the Python reference runner

- **Input:** CSV and Excel manifests; folder discovery for PDF invoices.
- **PDF extraction:** selectable PDF text extraction using pdfplumber; optional Tesseract OCR fallback. OCR results are routed to Review for human verification. Extraction uses configurable field patterns and is not a universal invoice parser.
- **Supplier checks:** optional supplier master CSV with `vendor_name`, `gst_number`, and `status`. Unknown supplier and GST mismatch go to Review; inactive supplier is rejected.
- **Validation:** mandatory invoice ID/supplier/date/amount, GST format, positive amount, non-negative tax, currency format and date ordering.
- **Duplicate protection:** duplicate invoice IDs within a batch and across previous runs, plus source-file SHA-256 duplicate detection, backed by SQLite unique keys.
- **Routing:** Approved / Review / Rejected folders. Missing and unreadable source files are recorded as exceptions in the processing report.
- **Database:** parameterized SQLite writes for approved invoices and processing events.
- **Reports:** CSV and Excel detail reports, PDF summary/detail report and JSON processing summary.
- **Logging and errors:** rotating logs, file-level error reasons, extraction failures, database duplicate handling, filesystem handling and optional email error logs.
- **Email:** optional SMTP notification with report attachments. Delivery is only claimed after a successful SMTP send.

## Setup (Windows PowerShell)

From this project directory:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Run a CSV/XLSX manifest

The manifest must contain `source_file` paths. Relative paths resolve under `Input/`.

```powershell
python src/invoice_pipeline.py --root . --input data/invoice_manifest_demo.csv --suppliers data/suppliers_demo.csv
```

### Process PDFs from the Input folder

Put PDFs in `Input/`, then run:

```powershell
python src/invoice_pipeline.py --root . --input Input --suppliers data/suppliers_demo.csv
```

### Optional OCR

Install Tesseract OCR and Poppler separately on Windows, ensure their executables are on PATH, then install optional Python packages:

```powershell
pip install pdf2image pytesseract
python src/invoice_pipeline.py --root . --input Input --ocr
```

Scanned PDFs without OCR configured are routed to Review with a PDF extraction reason. OCR-extracted invoices also go to Review.

### Optional email

Set SMTP values in the current terminal session; never commit credentials or a populated `.env` file:

```powershell
$env:SMTP_HOST="smtp.example.com"
$env:SMTP_PORT="587"
$env:SMTP_USER="your-account"
$env:SMTP_PASSWORD="app-password"
$env:SMTP_TO="recipient@example.com"
$env:SMTP_FROM="your-account"
python src/invoice_pipeline.py --root . --input Input --email
```

The example host/account above are placeholders. Use your provider's SMTP settings and app password. A successful local run is not proof of A360 email automation.

### Folder monitoring

```powershell
python src/invoice_pipeline.py --root . --watch --interval 10 --suppliers data/suppliers_demo.csv
```

The reference watcher polls for new PDFs and CSV/XLSX manifests. It is a local polling process, not a cloud event trigger or A360 Control Room integration.

## Database

The local reference runner uses `database/invoices.sqlite3`. It stores approved invoice rows, file hashes and processing events. `database/schema.sql` is the MySQL schema for the A360/database deployment path. Use parameterized queries and a unique invoice ID constraint; store credentials in A360 Credential Vault or environment secrets.

## Tests

```powershell
python -m pytest -q tests
```

Tests cover manifest reading, approved routing, report creation, cross-run duplicate rejection, unknown supplier review and missing-file rejection. PDF/OCR and SMTP require separate environment-level integration tests.

## A360 build guide

Follow [docs/A360_BUILD_GUIDE.md](docs/A360_BUILD_GUIDE.md) for the task sequence and action-level checklist. The A360 bot itself still needs to be built and run in your tenant.

## Evidence checklist

See [evidence/README.md](evidence/README.md). Capture genuine screenshots from your own A360 run and mask supplier/customer data. Do not upload credentials, real invoices or personal data.
