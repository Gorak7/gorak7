"""End-to-end invoice pipeline reference implementation.

The Python runner is a local reference for the A360 workflow. It supports PDF text
extraction (optional OCR fallback), CSV/XLSX manifests, persistent duplicate checks,
supplier allow-list checks, status routing, SQLite persistence, reports, logging,
and optional SMTP notifications. OCR/email are best-effort and must be configured.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import logging
from logging.handlers import RotatingFileHandler
import os
import re
import shutil
import smtplib
import sqlite3
import sys
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None

FIELDS = ("invoice_id", "vendor_name", "invoice_date", "due_date", "gst_number",
          "amount", "tax_amount", "currency", "source_file")
REPORT_FIELDS = FIELDS + ("run_id", "processed_at", "status", "decision_reason",
                          "extraction_method", "file_sha256")
GST_RE = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$")
PATTERNS = {
    "invoice_id": [r"(?:invoice\s*(?:no\.?|number|#|id))\s*[:#-]?\s*([A-Z0-9][A-Z0-9/-]{2,})"],
    "vendor_name": [r"(?:supplier|vendor|sold\s+by|from)\s*[:\-]\s*([^\r\n]+)"],
    "invoice_date": [r"(?:invoice\s*date|date)\s*[:\-]\s*([0-9]{1,4}[./-][A-Za-z0-9]{1,4}[./-][0-9]{2,4})"],
    "gst_number": [r"(?:GSTIN|GST\s*(?:NO|NUMBER))\s*[:\-]?\s*([0-9A-Z]{15})"],
    "amount": [r"(?:grand\s+total|invoice\s+total|total\s+amount|total)\s*[:\-]?\s*(?:INR|Rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{1,2})?)"],
    "tax_amount": [r"(?:total\s+tax|tax\s+amount|GST\s+amount)\s*[:\-]?\s*(?:INR|Rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{1,2})?)"],
}
LOG = logging.getLogger("invoice_pipeline")


@dataclass
class Result:
    invoice_id: str = ""
    vendor_name: str = ""
    invoice_date: str = ""
    due_date: str = ""
    gst_number: str = ""
    amount: str = ""
    tax_amount: str = "0"
    currency: str = "INR"
    source_file: str = ""
    run_id: str = ""
    processed_at: str = ""
    status: str = "REVIEW"
    decision_reason: str = ""
    extraction_method: str = "manifest"
    file_sha256: str = ""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def setup_logging(root: Path) -> None:
    log_dir = root / "Logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    for existing in list(LOG.handlers):
        existing.close()
        LOG.removeHandler(existing)
    LOG.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_dir / "invoice_pipeline.log", maxBytes=1_000_000,
                                  backupCount=5, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    LOG.addHandler(handler)
    LOG.addHandler(logging.StreamHandler(sys.stdout))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_pdf(path: Path, enable_ocr: bool = False) -> tuple[dict, str]:
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as exc:
        LOG.warning("PDF text extraction failed for %s: %s", path.name, exc)
    method = "pdf_text"
    if not text.strip() and enable_ocr:
        try:
            from pdf2image import convert_from_path
            import pytesseract
            text = "\n".join(pytesseract.image_to_string(image) for image in convert_from_path(path))
            method = "ocr"
        except Exception as exc:
            raise RuntimeError(f"PDF_EXTRACTION_ERROR: OCR unavailable or failed: {exc}") from exc
    if not text.strip():
        raise RuntimeError("PDF_EXTRACTION_ERROR: no selectable text; OCR is disabled or found no text")
    extracted = {}
    for field, expressions in PATTERNS.items():
        for expression in expressions:
            match = re.search(expression, text, re.IGNORECASE)
            if match:
                extracted[field] = match.group(1).strip()
                break
    return extracted, method


def read_manifest(path: Path) -> list[dict]:
    if pd is None:
        raise RuntimeError("pandas is required to read CSV/XLSX manifests")
    if not path.exists():
        raise FileNotFoundError(f"Manifest missing: {path}")
    suffix = path.suffix.lower()
    if suffix == ".csv":
        frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    elif suffix in {".xlsx", ".xls"}:
        frame = pd.read_excel(path, dtype=str, keep_default_na=False)
    else:
        raise ValueError("Manifest must be .csv or .xlsx")
    return frame.to_dict(orient="records")


def supplier_set(path: Path | None) -> dict[str, dict[str, str]]:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"Supplier master not found: {path}")
    if pd is None:
        raise RuntimeError("pandas is required to read supplier master")
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    if "vendor_name" not in frame.columns:
        raise ValueError("Supplier master must contain vendor_name")
    suppliers = {}
    for row in frame.to_dict(orient="records"):
        name = str(row.get("vendor_name", "")).strip().casefold()
        if name:
            suppliers[name] = {
                "gst_number": str(row.get("gst_number", "")).strip().upper(),
                "status": str(row.get("status", "ACTIVE")).strip().upper() or "ACTIVE",
            }
    return suppliers


def db_connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("""CREATE TABLE IF NOT EXISTS invoices (
        invoice_id TEXT PRIMARY KEY, vendor_name TEXT, invoice_date TEXT, due_date TEXT,
        gst_number TEXT, amount TEXT, tax_amount TEXT, currency TEXT, source_file TEXT,
        run_id TEXT, processed_at TEXT, file_sha256 TEXT)""")
    connection.execute("""CREATE TABLE IF NOT EXISTS file_hashes (
        file_sha256 TEXT PRIMARY KEY, source_file TEXT, invoice_id TEXT, run_id TEXT)""")
    connection.execute("""CREATE TABLE IF NOT EXISTS processing_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT, invoice_id TEXT, source_file TEXT,
        status TEXT, decision_reason TEXT, extraction_method TEXT, started_at TEXT, completed_at TEXT)""")
    connection.commit()
    return connection


def validate(record: Result, suppliers: dict[str, dict[str, str]], conn: sqlite3.Connection,
             seen_this_run: set[str]) -> tuple[str, str]:
    issues: list[str] = []
    warnings: list[str] = []
    invoice_id = record.invoice_id.strip()
    vendor = record.vendor_name.strip()
    if not invoice_id: issues.append("MISSING_INVOICE_ID")
    if not vendor: issues.append("MISSING_SUPPLIER")
    if not record.invoice_date: issues.append("MISSING_INVOICE_DATE")
    if not record.amount: issues.append("MISSING_AMOUNT")
    if not record.gst_number: warnings.append("MISSING_GST_NUMBER")
    if invoice_id:
        if invoice_id.casefold() in seen_this_run:
            issues.append("DUPLICATE_WITHIN_RUN")
        elif conn.execute("SELECT 1 FROM invoices WHERE lower(invoice_id)=lower(?)", (invoice_id,)).fetchone():
            issues.append("DUPLICATE_ACROSS_RUNS")
        seen_this_run.add(invoice_id.casefold())
    if record.file_sha256 and conn.execute("SELECT 1 FROM file_hashes WHERE file_sha256=?",
                                           (record.file_sha256,)).fetchone():
        issues.append("DUPLICATE_FILE_ACROSS_RUNS")
    supplier = suppliers.get(vendor.casefold()) if vendor else None
    if suppliers and vendor and supplier is None:
        warnings.append("UNKNOWN_SUPPLIER")
    elif supplier:
        if supplier.get("status") not in ("ACTIVE", "APPROVED", "ENABLED"):
            issues.append("SUPPLIER_NOT_ACTIVE")
        master_gst = supplier.get("gst_number", "")
        if master_gst and record.gst_number and master_gst != record.gst_number.strip().upper():
            warnings.append("SUPPLIER_GST_MISMATCH")
    if record.gst_number and not GST_RE.fullmatch(record.gst_number.strip().upper()):
        issues.append("INVALID_GST_FORMAT")
    try:
        if Decimal(record.amount.replace(",", "")) <= 0:
            issues.append("NON_POSITIVE_AMOUNT")
    except (InvalidOperation, AttributeError):
        issues.append("INVALID_AMOUNT")
    try:
        if Decimal((record.tax_amount or "0").replace(",", "")) < 0:
            issues.append("NEGATIVE_TAX")
    except (InvalidOperation, AttributeError):
        issues.append("INVALID_TAX_AMOUNT")
    if record.currency and not re.fullmatch(r"[A-Z]{3}", record.currency.upper()):
        issues.append("INVALID_CURRENCY")
    if record.invoice_date:
        try: datetime.fromisoformat(record.invoice_date)
        except ValueError:
            try:
                if pd is None: raise ValueError()
                pd.to_datetime(record.invoice_date, errors="raise")
            except Exception: issues.append("INVALID_INVOICE_DATE")
    if record.due_date and record.invoice_date:
        try:
            due = pd.to_datetime(record.due_date) if pd is not None else datetime.fromisoformat(record.due_date)
            inv = pd.to_datetime(record.invoice_date) if pd is not None else datetime.fromisoformat(record.invoice_date)
            if due < inv: issues.append("DUE_DATE_BEFORE_INVOICE_DATE")
        except Exception:
            issues.append("INVALID_DUE_DATE")
    if issues:
        return "REJECTED", ";".join(issues + warnings)
    if warnings or record.extraction_method == "ocr":
        return "REVIEW", ";".join(warnings + (["OCR_REVIEW_REQUIRED"] if record.extraction_method == "ocr" else []))
    return "APPROVED", "VALIDATED"


def write_reports(root: Path, run_id: str, rows: list[Result]) -> dict:
    if pd is None:
        raise RuntimeError("pandas is required for reports")
    reports = root / "Reports"
    reports.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = reports / f"invoice_processing_{stamp}"
    frame = pd.DataFrame([asdict(row) for row in rows], columns=REPORT_FIELDS)
    csv_path, xlsx_path, pdf_path = (base.with_suffix(ext) for ext in (".csv", ".xlsx", ".pdf"))
    frame.to_csv(csv_path, index=False)
    frame.to_excel(xlsx_path, index=False)
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        counts = frame["status"].value_counts().to_dict() if not frame.empty else {}
        doc = SimpleDocTemplate(str(pdf_path), pagesize=landscape(A4))
        styles = getSampleStyleSheet()
        story = [Paragraph("Invoice Processing Report", styles["Title"]),
                 Paragraph(f"Run: {run_id} | Generated: {now_iso()}", styles["Normal"]),
                 Spacer(1, 12),
                 Paragraph("Approved: %s | Review: %s | Rejected: %s" %
                           (counts.get("APPROVED", 0), counts.get("REVIEW", 0), counts.get("REJECTED", 0)),
                           styles["Heading2"])]
        data = [["Invoice", "Supplier", "Amount", "Status", "Reason"]]
        data += [[r.invoice_id[:24], r.vendor_name[:28], r.amount[:16], r.status, r.decision_reason[:60]]
                 for r in rows]
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#243b53")),
                                   ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                                   ("GRID", (0,0), (-1,-1), .3, colors.grey),
                                   ("FONTSIZE", (0,0), (-1,-1), 7),
                                   ("VALIGN", (0,0), (-1,-1), "TOP")]))
        story.append(table)
        doc.build(story)
    except ImportError:
        LOG.exception("PDF report generation dependency missing")
        pdf_path = None
    summary = {"run_id": run_id, "total": len(rows),
               "approved": sum(r.status == "APPROVED" for r in rows),
               "review": sum(r.status == "REVIEW" for r in rows),
               "rejected": sum(r.status == "REJECTED" for r in rows),
               "generated_at": now_iso()}
    (reports / f"processing_summary_{stamp}.json").write_text(
        __import__("json").dumps(summary, indent=2), encoding="utf-8")
    return {"csv": str(csv_path), "xlsx": str(xlsx_path),
            "pdf": str(pdf_path) if pdf_path else None, "summary": summary}


def send_email(summary: dict, attachments: Iterable[Path]) -> bool:
    host, user, password, recipient = (os.getenv(k, "") for k in
        ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "SMTP_TO"))
    if not all((host, user, password, recipient)):
        LOG.info("Email skipped: SMTP_HOST/USER/PASSWORD/TO are not all configured")
        return False
    message = EmailMessage()
    message["Subject"] = f"Invoice processing report — {summary['run_id']}"
    message["From"] = os.getenv("SMTP_FROM", user)
    message["To"] = recipient
    message.set_content("Invoice processing completed.\n" + "\n".join(
        f"{key}: {value}" for key, value in summary.items()))
    for path in attachments:
        if path and path.exists():
            message.add_attachment(path.read_bytes(), maintype="application",
                                   subtype="octet-stream", filename=path.name)
    try:
        with smtplib.SMTP(host, int(os.getenv("SMTP_PORT", "587")), timeout=20) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(message)
        LOG.info("Email sent to configured recipient")
        return True
    except Exception:
        LOG.exception("EMAIL_ERROR: notification failed")
        return False


def process_records(root: Path, records: list[dict], suppliers_file: Path | None = None,
                    database: Path | None = None, enable_ocr: bool = False,
                    send_notification: bool = False) -> dict:
    root = root.resolve()
    for name in ("Input", "Working", "Approved", "Review", "Rejected", "Exceptions", "Processed", "Logs", "Reports"):
        (root / name).mkdir(parents=True, exist_ok=True)
    setup_logging(root)
    run_id = "INV-" + uuid.uuid4().hex[:10].upper()
    try:
        conn = db_connect(database or root / "database" / "invoices.sqlite3")
    except sqlite3.Error as exc:
        error_file = root / "Exceptions" / f"database_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        error_file.write_text(f"DATABASE_ERROR: {exc}\nRun ID: {run_id}\n", encoding="utf-8")
        LOG.exception("DATABASE_ERROR: cannot open invoice database")
        raise RuntimeError(f"DATABASE_ERROR: {exc}") from exc
    suppliers = supplier_set(suppliers_file)
    seen: set[str] = set()
    results: list[Result] = []
    for source_record in records:
        started = now_iso()
        raw_path = str(source_record.get("source_file", "")).strip()
        source = Path(raw_path) if raw_path else Path("")
        if raw_path and not source.is_absolute():
            source = root / "Input" / source
        record = Result(run_id=run_id, processed_at=now_iso(), source_file=raw_path,
                        invoice_id=str(source_record.get("invoice_id", "")).strip(),
                        vendor_name=str(source_record.get("vendor_name", "")).strip(),
                        invoice_date=str(source_record.get("invoice_date", "")).strip(),
                        due_date=str(source_record.get("due_date", "")).strip(),
                        gst_number=str(source_record.get("gst_number", "")).strip().upper(),
                        amount=str(source_record.get("amount", "")).strip(),
                        tax_amount=str(source_record.get("tax_amount", "0") or "0").strip(),
                        currency=str(source_record.get("currency", "INR") or "INR").strip().upper())
        try:
            if raw_path:
                if not source.is_file():
                    raise FileNotFoundError(f"MISSING_SOURCE_FILE: {source}")
                working = root / "Working" / source.name
                if source.resolve() != working.resolve():
                    shutil.copy2(source, working)
                record.file_sha256 = sha256_file(working)
                if source.suffix.lower() == ".pdf" and any(
                    not getattr(record, field) for field in ("invoice_id", "vendor_name", "invoice_date", "amount")
                ):
                    extracted, method = parse_pdf(working, enable_ocr)
                    for key, value in extracted.items():
                        if value and not getattr(record, key): setattr(record, key, value)
                    record.extraction_method = method
            # source_file is optional for structured CSV/XLSX rows. If supplied,
            # it must exist; missing paths are handled as explicit file errors.
            record.status, record.decision_reason = validate(record, suppliers, conn, seen)
        except FileNotFoundError as exc:
            record.status, record.decision_reason = "REJECTED", str(exc)
        except Exception as exc:
            record.status = "REVIEW" if "PDF_EXTRACTION_ERROR" in str(exc) else "REJECTED"
            record.decision_reason = f"PROCESSING_ERROR: {type(exc).__name__}: {exc}"
            LOG.exception("Processing error for %s", raw_path)
        record.processed_at = now_iso()
        results.append(record)
        database_ok = True
        try:
            if record.status == "APPROVED":
                conn.execute("""INSERT INTO invoices VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (record.invoice_id, record.vendor_name, record.invoice_date, record.due_date,
                     record.gst_number, record.amount, record.tax_amount, record.currency,
                     record.source_file, record.run_id, record.processed_at, record.file_sha256))
            if record.file_sha256:
                conn.execute("INSERT OR IGNORE INTO file_hashes VALUES (?,?,?,?)",
                             (record.file_sha256, record.source_file, record.invoice_id, run_id))
            conn.execute("""INSERT INTO processing_events
                (run_id,invoice_id,source_file,status,decision_reason,extraction_method,started_at,completed_at)
                VALUES (?,?,?,?,?,?,?,?)""",
                (run_id, record.invoice_id, record.source_file, record.status,
                 record.decision_reason, record.extraction_method, started, record.processed_at))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.rollback()
            record.status = "REJECTED"
            record.decision_reason = "DUPLICATE_ACROSS_RUNS"
            LOG.warning("Duplicate invoice prevented by database unique key: %s", record.invoice_id)
            try:
                conn.execute("""INSERT INTO processing_events
                    (run_id,invoice_id,source_file,status,decision_reason,extraction_method,started_at,completed_at)
                    VALUES (?,?,?,?,?,?,?,?)""",
                    (run_id, record.invoice_id, record.source_file, record.status,
                     record.decision_reason, record.extraction_method, started, now_iso()))
                conn.commit()
            except sqlite3.Error:
                conn.rollback()
                LOG.exception("Could not persist duplicate event")
        except sqlite3.Error as exc:
            conn.rollback()
            database_ok = False
            record.status = "REVIEW"
            record.decision_reason = f"DATABASE_ERROR: {exc}"
            LOG.exception("DATABASE_ERROR for %s", record.invoice_id)

        if raw_path and source.exists():
            target_name = ("Exceptions" if (not database_ok or "PDF_EXTRACTION_ERROR" in record.decision_reason)
                           else {"APPROVED": "Approved", "REVIEW": "Review", "REJECTED": "Rejected"}[record.status])
            destination = root / target_name / source.name
            try:
                if source.resolve() != destination.resolve():
                    shutil.move(str(source), str(destination))
                working_file = root / "Working" / source.name
                if working_file.exists():
                    working_file.unlink()
            except OSError as exc:
                record.status = "REVIEW"
                record.decision_reason += f"; FILE_SYSTEM_ERROR: {exc}"
                LOG.exception("FILE_SYSTEM_ERROR while routing %s", source)
        LOG.info("%s %s %s %s", record.status, record.invoice_id, record.source_file, record.decision_reason)

    conn.close()
    report = write_reports(root, run_id, results)
    attachments = [Path(report["csv"]), Path(report["xlsx"])]
    if report["pdf"]: attachments.append(Path(report["pdf"]))
    email_sent = send_email(report["summary"], attachments) if send_notification else False
    report["email_sent"] = email_sent
    return report


def discover_folder_records(folder: Path) -> list[dict]:
    if not folder.exists():
        raise FileNotFoundError(f"Input folder does not exist: {folder}")
    records: list[dict] = []
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            records.append({"source_file": path.name})
        elif suffix in {".csv", ".xlsx", ".xls"}:
            records.extend(read_manifest(path))
    return records


def run_once(args) -> dict:
    root = Path(args.root)
    input_path = Path(args.input) if args.input else root / "Input"
    if input_path.is_file():
        records = read_manifest(input_path)
    else:
        records = discover_folder_records(input_path)
    return process_records(root, records, Path(args.suppliers) if args.suppliers else None,
                           Path(args.database) if args.database else None,
                           args.ocr, args.email)


def main() -> None:
    parser = argparse.ArgumentParser(description="Invoice intake, extraction, validation and reporting")
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", help="CSV/XLSX manifest or folder containing PDFs")
    parser.add_argument("--suppliers", help="CSV supplier master with vendor_name column")
    parser.add_argument("--database", help="SQLite database path")
    parser.add_argument("--ocr", action="store_true", help="Enable optional Tesseract OCR fallback")
    parser.add_argument("--email", action="store_true", help="Send report using SMTP environment variables")
    parser.add_argument("--watch", action="store_true", help="Poll Input folder and process new PDFs")
    parser.add_argument("--interval", type=int, default=10, help="Folder polling interval in seconds")
    args = parser.parse_args()
    if not args.watch:
        print(run_once(args))
        return
    root = Path(args.root).resolve()
    inbox = root / "Input"
    inbox.mkdir(parents=True, exist_ok=True)
    LOG.info("Watching %s every %ss", inbox, args.interval)
    processed: set[str] = set()
    try:
        while True:
            files = [p for p in inbox.iterdir() if p.is_file() and p.suffix.lower() in {".pdf", ".csv", ".xlsx", ".xls"}]
            fresh = [p for p in files if str(p.resolve()) not in processed]
            for path in fresh:
                if path.suffix.lower() == ".pdf":
                    records = [{"source_file": path.name}]
                else:
                    records = read_manifest(path)
                if records:
                    result = process_records(root, records, Path(args.suppliers) if args.suppliers else None,
                                              Path(args.database) if args.database else None, args.ocr, args.email)
                    LOG.info("Folder batch completed: %s", result["summary"])
                if path.suffix.lower() in {".csv", ".xlsx", ".xls"} and path.exists():
                    archive = root / "Processed" / f"manifest_{uuid.uuid4().hex[:8]}_{path.name}"
                    shutil.move(str(path), str(archive))
                processed.add(str(path.resolve()))
            time.sleep(max(2, args.interval))
    except KeyboardInterrupt:
        LOG.info("Folder watcher stopped by user")


if __name__ == "__main__":
    main()
