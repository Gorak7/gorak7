"""Runnable invoice processor; bundled inputs are synthetic demo data."""
from __future__ import annotations
import argparse, os, re, uuid
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

REQUIRED = ["invoice_id","vendor_name","invoice_date","due_date","gst_number","amount","tax_amount","currency","source_file"]
OUTPUT_COLUMNS = REQUIRED + ["run_id","processed_at","status","error_codes"]
GST_RE = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$")

def _blank(value):
    if value is None: return True
    try:
        if pd.isna(value): return True
    except (TypeError, ValueError): pass
    return str(value).strip() == ""

def _decimal(value):
    if _blank(value): raise InvalidOperation
    return Decimal(str(value).strip().replace(",", ""))

def _date(value):
    if _blank(value): raise ValueError("missing date")
    return pd.to_datetime(str(value).strip(), errors="raise").date()

def validate(row: dict, seen: set[str]) -> list[str]:
    errors = []
    for field in REQUIRED:
        if _blank(row.get(field)): errors.append(f"MISSING_{field.upper()}")
    invoice_id = str(row.get("invoice_id", "")).strip()
    if invoice_id and invoice_id in seen: errors.append("DUPLICATE_INVOICE_ID")
    gst = str(row.get("gst_number", "")).strip().upper()
    if gst and not GST_RE.fullmatch(gst): errors.append("INVALID_GST_FORMAT")
    try:
        amount = _decimal(row.get("amount"))
        if amount <= 0: errors.append("NON_POSITIVE_AMOUNT")
    except (InvalidOperation, ValueError, TypeError): errors.append("INVALID_AMOUNT")
    try:
        tax = _decimal(row.get("tax_amount"))
        if tax < 0: errors.append("NEGATIVE_TAX")
    except (InvalidOperation, ValueError, TypeError): errors.append("INVALID_TAX_AMOUNT")
    invoice_date = due_date = None
    try: invoice_date = _date(row.get("invoice_date"))
    except (ValueError, TypeError, OverflowError):
        if not _blank(row.get("invoice_date")): errors.append("INVALID_INVOICE_DATE")
    try: due_date = _date(row.get("due_date"))
    except (ValueError, TypeError, OverflowError):
        if not _blank(row.get("due_date")): errors.append("INVALID_DUE_DATE")
    if invoice_date and due_date and due_date < invoice_date: errors.append("DUE_DATE_BEFORE_INVOICE_DATE")
    currency = str(row.get("currency", "")).strip().upper()
    if currency and not re.fullmatch(r"[A-Z]{3}", currency): errors.append("INVALID_CURRENCY")
    if invoice_id: seen.add(invoice_id)
    return errors

def read_input(source: Path) -> pd.DataFrame:
    suffix = source.suffix.lower()
    if suffix == ".csv": return pd.read_csv(source, dtype=str, keep_default_na=False)
    if suffix in {".xlsx", ".xls"}: return pd.read_excel(source, dtype=str, keep_default_na=False)
    raise ValueError(f"Unsupported input format: {suffix or '(no extension)'}. Use CSV or Excel.")

def write_outputs(out, accepted, rejected, logs, summary):
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(accepted, columns=OUTPUT_COLUMNS).to_csv(out/"processed_invoices.csv", index=False)
    pd.DataFrame(rejected, columns=OUTPUT_COLUMNS).to_csv(out/"invoice_exceptions.csv", index=False)
    log_cols = ["run_id","invoice_id","status","error_category","error_message","started_at","completed_at"]
    pd.DataFrame(logs, columns=log_cols).to_csv(out/"execution_logs.csv", index=False)
    pd.DataFrame([summary]).to_csv(out/"daily_summary.csv", index=False)

def persist_sqlite(engine, accepted, rejected, logs):
    with engine.begin() as conn:
        conn.execute(text("""CREATE TABLE IF NOT EXISTS invoices (
            invoice_id TEXT PRIMARY KEY, vendor_name TEXT, invoice_date TEXT, due_date TEXT,
            gst_number TEXT, amount TEXT, tax_amount TEXT, currency TEXT, source_file TEXT,
            run_id TEXT, processed_at TEXT)"""))
        conn.execute(text("""CREATE TABLE IF NOT EXISTS invoice_exceptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, invoice_id TEXT, vendor_name TEXT,
            error_codes TEXT, run_id TEXT, processed_at TEXT)"""))
        conn.execute(text("""CREATE TABLE IF NOT EXISTS bot_execution_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT, invoice_id TEXT, status TEXT,
            error_category TEXT, error_message TEXT, started_at TEXT, completed_at TEXT)"""))
        if accepted:
            conn.execute(text("""INSERT OR IGNORE INTO invoices
                (invoice_id,vendor_name,invoice_date,due_date,gst_number,amount,tax_amount,currency,source_file,run_id,processed_at)
                VALUES (:invoice_id,:vendor_name,:invoice_date,:due_date,:gst_number,:amount,:tax_amount,:currency,:source_file,:run_id,:processed_at)"""), accepted)
        if rejected:
            params = [{"invoice_id":r.get("invoice_id",""),"vendor_name":r.get("vendor_name",""),
                       "error_codes":r["error_codes"],"run_id":r["run_id"],"processed_at":r["processed_at"]} for r in rejected]
            conn.execute(text("""INSERT INTO invoice_exceptions (invoice_id,vendor_name,error_codes,run_id,processed_at)
                VALUES (:invoice_id,:vendor_name,:error_codes,:run_id,:processed_at)"""), params)
        if logs:
            conn.execute(text("""INSERT INTO bot_execution_logs
                (run_id,invoice_id,status,error_category,error_message,started_at,completed_at)
                VALUES (:run_id,:invoice_id,:status,:error_category,:error_message,:started_at,:completed_at)"""), logs)

def process_file(source: Path, out: Path, database_url: str | None = None) -> dict:
    if not source.is_file(): raise FileNotFoundError(f"Input file not found: {source}")
    df = read_input(source)
    for col in REQUIRED:
        if col not in df.columns: df[col] = ""
    run_id = "INV-" + uuid.uuid4().hex[:8].upper()
    started = datetime.now(timezone.utc).isoformat()
    seen, accepted, rejected, logs = set(), [], [], []
    for _, series in df.iterrows():
        row = {key:series.get(key,"") for key in REQUIRED}
        row["currency"] = str(row.get("currency","")).strip().upper()
        row["gst_number"] = str(row.get("gst_number","")).strip().upper()
        errors = validate(row, seen)
        completed = datetime.now(timezone.utc).isoformat()
        record = {**row,"run_id":run_id,"processed_at":completed}
        if errors:
            record.update(status="REJECTED",error_codes=";".join(errors)); rejected.append(record); status="FAILED"
        else:
            record.update(status="ACCEPTED",error_codes=""); accepted.append(record); status="SUCCESS"
        logs.append({"run_id":run_id,"invoice_id":row.get("invoice_id",""),"status":status,
                     "error_category":"DATA_ERROR" if errors else "","error_message":";".join(errors),
                     "started_at":started,"completed_at":completed})
    summary={"run_id":run_id,"total":len(df),"accepted":len(accepted),"rejected":len(rejected),
             "success_rate_pct":round(len(accepted)/len(df)*100,2) if len(df) else 0.0}
    write_outputs(out,accepted,rejected,logs,summary)
    engine=create_engine(database_url or os.getenv("DATABASE_URL","sqlite:///invoice_bot.db"))
    try:
        if engine.dialect.name == "sqlite": persist_sqlite(engine,accepted,rejected,logs)
        else:
            with engine.begin() as conn:
                for row in accepted:
                    conn.execute(text("""INSERT IGNORE INTO invoices
                      (invoice_id,vendor_name,invoice_date,due_date,gst_number,amount,tax_amount,currency,source_file,run_id,processed_at)
                      VALUES (:invoice_id,:vendor_name,:invoice_date,:due_date,:gst_number,:amount,:tax_amount,:currency,:source_file,:run_id,:processed_at)"""),row)
                for row in rejected:
                    conn.execute(text("""INSERT INTO invoice_exceptions
                      (invoice_id,vendor_name,error_codes,run_id,processed_at) VALUES (:invoice_id,:vendor_name,:error_codes,:run_id,:processed_at)"""),
                      {"invoice_id":row.get("invoice_id",""),"vendor_name":row.get("vendor_name",""),"error_codes":row["error_codes"],"run_id":run_id,"processed_at":row["processed_at"]})
                for row in logs:
                    conn.execute(text("""INSERT INTO bot_execution_logs
                      (run_id,invoice_id,status,error_category,error_message,started_at,completed_at)
                      VALUES (:run_id,:invoice_id,:status,:error_category,:error_message,:started_at,:completed_at)"""),row)
    finally: engine.dispose()
    return summary

def main():
    parser=argparse.ArgumentParser(description="Validate and process invoice CSV/XLSX files.")
    parser.add_argument("--input",required=True); parser.add_argument("--out",default="output")
    args=parser.parse_args()
    try: summary=process_file(Path(args.input),Path(args.out))
    except Exception as exc: parser.exit(2,f"Processing failed: {exc}\n")
    print("INVOICE PROCESSING COMPLETE"); print(summary); print(f"Outputs: {Path(args.out).resolve()}")
    print("Email delivery is not performed by this reference processor; configure the A360 email action separately.")
if __name__ == "__main__": main()
