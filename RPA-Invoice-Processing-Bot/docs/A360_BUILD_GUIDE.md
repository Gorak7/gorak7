# Automation Anywhere A360 Community Edition — Build Guide

## Folder contract
Create `Input/`, `Working/`, `Processed/`, `Exceptions/`, `Logs/`, and `Reports/`. Copy each file from Input to Working before processing. Move to Processed only after all rows are handled; move unreadable files to Exceptions with a reason.

## Bot task outline
1. **Initialize:** create run ID and timestamp; initialize counters; create run log.
2. **Discover files:** use Folder > Get files; filter supported extensions. Record no-file condition as a successful no-op.
3. **Read source:** CSV/Excel via A360 file/Excel actions. For PDF, use the available document extraction/OCR capability in your A360 Community workspace; extraction quality must be reviewed. Do not silently treat OCR output as verified.
4. **Normalize:** trim strings, standardize date to YYYY-MM-DD, normalize GST to uppercase, parse amounts as decimals.
5. **Validate each row:** required fields; numeric positive amount; non-negative tax; GST pattern; duplicate invoice ID using a dictionary/list or database unique key.
6. **Route:** valid -> insert into invoices; invalid -> append exception row with error codes. Use Try/Catch or Error Handler around file read, DB insert, and file move.
7. **Database:** connect using secured credential/connection configuration; parameterized insert; commit per invoice or controlled batch. Treat unique-key violations as duplicate exceptions.
8. **Logging:** append run ID, invoice ID, start/end time, status, category, and error message to bot_execution_logs.
9. **Summary:** calculate totals and success rate; create CSV/XLSX daily report.
10. **Email:** send summary via A360 email action only when SMTP is configured; attach exception report. Log mail success/failure separately.
11. **Cleanup:** close workbook/DB resources; archive source; ensure failed files remain recoverable.

## Suggested exception categories
DATA_ERROR, FILE_SYSTEM_ERROR, PDF_EXTRACTION_ERROR, DATABASE_ERROR, APPLICATION_ERROR, TIMEOUT, EMAIL_ERROR.

## Test scenarios
- Valid CSV/XLSX row; valid PDF extraction; missing invoice ID; malformed GST; duplicate invoice ID; zero/negative amount; missing vendor; unreadable/corrupt file; database unavailable; duplicate-key database response; SMTP unavailable; rerun same input.

## A360 evidence to capture
Screenshots must come from your own Community Edition run: bot workflow, variables, sample input, run details, accepted output, exception output, database query result, and actual email inbox. Never use the synthetic dashboard as proof that A360 ran.
