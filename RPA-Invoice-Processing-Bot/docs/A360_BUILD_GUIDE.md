# Automation Anywhere A360 Community Edition — End-to-End Build Guide

This is the platform build plan for the bot. Menu/action names can differ by A360 package/version. Use the equivalent actions available in your tenant; do not claim a package/action ran until tested.

## 1. Create the workspace folders

Create `Input`, `Working`, `Approved`, `Review`, `Rejected`, `Exceptions`, `Logs`, and `Reports`. Add a supplier master file with columns:

`vendor_name,gst_number,status`

Use synthetic supplier records for portfolio demonstrations. Define status values such as ACTIVE and INACTIVE.

## 2. Create the A360 task and variables

Suggested task name: `Invoice_Processing_Bot`.

Create variables:
- `runId` (text), `runStartedAt` / `runCompletedAt` (date-time)
- `totalCount`, `approvedCount`, `reviewCount`, `rejectedCount` (number)
- `invoiceId`, `supplierName`, `supplierGst`, `invoiceDate`, `dueDate`, `amount`, `taxAmount`, `currency` (text/number as appropriate)
- `status`, `reasonCodes`, `sourcePath`, `workingPath`, `destinationPath` (text)
- `fileHash` (text, if your available package supports SHA-256)

Generate a unique run ID at start. Initialize counters and append a START event to the run log.

## 3. Monitor and discover files

For a scheduled bot, poll the Input folder at a configured interval:
1. Use Folder/Get Files to enumerate PDF, CSV and XLSX files.
2. Ignore temporary/partial files (for example, files still being written); check size stability before processing.
3. If no files exist, log NO_FILES and end the cycle successfully.
4. Copy each file to Working before opening it.
5. If the source is missing or cannot be copied, log FILE_SYSTEM_ERROR and create a file-level exception. Do not silently skip it.

A360 Control Room scheduling is separate from the local Python `--watch` polling example.

## 4. Read CSV and Excel input

- Use CSV actions to read headers and rows, or Excel actions to open the workbook and read the used range.
- Map columns to the canonical fields: invoice_id, vendor_name, invoice_date, due_date, gst_number, amount, tax_amount, currency, source_file.
- Validate required headers before starting the row loop.
- For Excel-to-database processing, map each validated row to a parameterized database insert. Never concatenate user-controlled invoice values into SQL.
- Close workbook/file handles in a finally/cleanup path.

## 5. Extract PDF fields (PDF-to-CSV)

Use the document/PDF extraction or OCR capability available in your A360 tenant:
1. Extract text/fields for invoice number, supplier name, invoice date, due date, GSTIN, taxable amount, tax and grand total.
2. Normalize whitespace, dates, decimal separators and GSTIN casing.
3. If extraction fails, the PDF is corrupt/password-protected, or required fields are not confidently extracted, route to Review or Exceptions with PDF_EXTRACTION_ERROR.
4. OCR output must be human-reviewed; do not automatically approve low-confidence extraction.
5. Append extracted fields to the invoice data table and generate the CSV/XLSX processing output.

If your Community Edition workspace does not expose a document extraction/OCR action, use the Python reference as a local demonstration and keep the A360 PDF extraction step marked pending until you configure a supported package/service.

## 6. Supplier and business validation

Look up supplier by normalized vendor name in the supplier master/database:
- Supplier absent: Review with UNKNOWN_SUPPLIER.
- Supplier inactive/blocked: Reject with SUPPLIER_NOT_ACTIVE.
- Supplier GSTIN differs from master: Review with SUPPLIER_GST_MISMATCH.
- Missing invoice ID, supplier, invoice date or amount: Reject.
- Invalid GSTIN format, amount <= 0, negative tax, invalid currency or due date before invoice date: Reject.
- OCR-extracted values: Review pending human verification.

GST format checks are not a live GST portal registration verification.

## 7. Duplicate detection across runs

Use both:
- In-memory collection/dictionary for duplicate invoice IDs in the current batch.
- Database unique constraint on normalized invoice ID for cross-run detection.

Before insert, query for an existing invoice ID. Still enforce the unique constraint to protect against concurrent runs. Route duplicate IDs/files to Rejected with DUPLICATE_INVOICE_ID or DUPLICATE_FILE. Do not overwrite an existing approved invoice.

## 8. Route files and records

- All mandatory checks pass and supplier is active: insert and route to Approved.
- Supplier unknown/GST mismatch/OCR uncertainty: route to Review.
- Invalid required data, inactive supplier or duplicate: route to Rejected.
- Corrupt/unreadable/missing file or unrecoverable file-level error: Exceptions, with a reason in the exception log.

Move only after the record outcome is persisted. If moving fails, log FILE_SYSTEM_ERROR and leave the original recoverable in Working/Input. Never delete the only copy.

## 9. Database actions

Use Database package/connection to MySQL (or an approved database). The schema is in `database/schema.sql`.
- Create/use `invoices`, `invoice_exceptions`, and `bot_execution_logs`.
- Use Credential Vault for database credentials.
- Use parameterized insert/select/update actions.
- Commit per invoice or in controlled batches.
- Catch connection timeout, constraint violation and transaction failures as DATABASE_ERROR.
- On DB failure, do not move an invoice to Approved; leave it recoverable and retry or route to Exceptions.

## 10. Logging and exception handling

Log at least: run ID, invoice ID, source file, start/end timestamps, status, reason code, error category and message.

Wrap file read/copy/move, PDF extraction, Excel/CSV parsing, supplier lookup, DB operations and email in error handlers. Suggested categories:
- DATA_ERROR
- FILE_SYSTEM_ERROR
- PDF_EXTRACTION_ERROR
- SUPPLIER_VALIDATION_ERROR
- DUPLICATE_ERROR
- DATABASE_ERROR
- APPLICATION_ERROR
- TIMEOUT
- EMAIL_ERROR

Continue to the next invoice for row-level errors. Stop safely on configuration/system errors that make further processing unsafe.

## 11. Processing reports and email automation

At end of run generate:
- `invoice_processing_<timestamp>.csv` — row-level extracted values, status and reason.
- `invoice_processing_<timestamp>.xlsx` — same data, with summary counts.
- `invoice_processing_<timestamp>.pdf` — run summary and invoice decision table.
- `processing_summary.json` or equivalent run summary.
- Exception CSV with failed/review rows and error reasons.

Use A360 Email action to send run totals and attach reports. Store credentials securely. Log email success only after the send action succeeds; on SMTP/auth/attachment failure log EMAIL_ERROR without losing the reports.

## 12. Rerun safety and cleanup

Close database connections and workbooks. Preserve original inputs until processing and persistence succeed. A rerun of the same invoice must be detected by database uniqueness; it must not create a second approved row.

## 13. Required test matrix

| Test | Expected outcome |
|---|---|
| Valid CSV row | Approved, DB row and reports |
| Valid XLSX row | Approved, DB row and reports |
| Text PDF with required fields | Extract fields, then validate |
| Scanned PDF with OCR configured | Extract then Review for human check |
| Corrupt/password-protected PDF | Review/Exceptions with extraction reason |
| Missing source file | Rejected/Exceptions with missing-file reason |
| Unknown supplier | Review |
| Inactive supplier | Rejected |
| Supplier GST mismatch | Review |
| Missing mandatory field | Rejected |
| Invalid GST/amount/date | Rejected |
| Duplicate within batch | Rejected |
| Same invoice on later run | Rejected; no duplicate DB row |
| Same file content under a new filename | Duplicate file detected |
| Database unavailable | No Approved move; recoverable exception |
| Folder move failure | Log and preserve source |
| SMTP unavailable | Reports retained; EMAIL_ERROR logged |

## 14. Evidence to capture from your own A360 workspace

1. Task canvas showing folder discovery and loop.
2. CSV/Excel read actions and variable mappings.
3. PDF extraction/OCR configuration and extracted fields.
4. Supplier lookup and validation branches.
5. Duplicate check and database unique constraint.
6. Approved, Review, Rejected and Exceptions folders with synthetic sample files.
7. A360 run details with run ID and final status.
8. Database SELECT results proving one-row-per-invoice behavior across two runs.
9. CSV, XLSX and PDF reports generated by the run.
10. Actual received email and attachment list, if email is configured.

Do not use Python screenshots, mock data, or a dashboard screenshot as proof of an A360 execution.
