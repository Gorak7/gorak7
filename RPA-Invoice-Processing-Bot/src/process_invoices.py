"""Runnable reference invoice processor. Synthetic demo data only."""
from __future__ import annotations
import argparse, csv, os, re, uuid
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

REQUIRED = ["invoice_id", "vendor_name", "invoice_date", "due_date", "gst_number",
            "amount", "tax_amount", "currency", "source_file"]
GST_RE = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$")

def validate(row: dict, seen: set[str]) -> list[str]:
    errors = []
    for field in REQUIRED:
        if field not in row or pd.isna(row.get(field)) or str(row.get(field)).strip() == "":
            errors.append(f"MISSING_{field.upper()}")
    invoice_id = str(row.get("invoice_id", "")).strip()
    if invoice_id and invoice_id in seen:
        errors.append("DUPLICATE_INVOICE_ID")
    gst = str(row.get("gst_number", "")).strip().upper()
    if gst and not GST_RE.match(gst):
        errors.append("INVALID_GST_FORMAT")
    try:
        amount = float(row.get("amount"))
        if amount <= 0: errors.append("NON_POSITIVE_AMOUNT")
    except (TypeError, ValueError):
        errors.append("INVALID_AMOUNT")
    try:
        tax = float(row.get("tax_amount"))
        if tax < 0: errors.append("NEGATIVE_TAX")
    except (TypeError, ValueError):
        errors.append("INVALID_TAX_AMOUNT")
    if invoice_id: seen.add(invoice_id)
    return errors

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="output")
    args = ap.parse_args()
    source = Path(args.input)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(source, dtype=str) if source.suffix.lower() in {".xlsx", ".xls"} else pd.read_csv(source, dtype=str)
    for col in REQUIRED:
        if col not in df.columns: df[col] = ""
    seen, accepted, rejected, logs = set(), [], [], []
    run_id = "INV-" + uuid.uuid4().hex[:8].upper()
    started = datetime.now(timezone.utc).isoformat()
    for _, series in df.iterrows():
        row = series.to_dict()
        errors = validate(row, seen)
        record = {**row, "run_id": run_id, "processed_at": datetime.now(timezone.utc).isoformat()}
        if errors:
            record.update({"status":"REJECTED", "error_codes":";".join(errors)})
            rejected.append(record)
            status = "FAILED"
        else:
            record.update({"status":"ACCEPTED", "error_codes":""})
            accepted.append(record)
            status = "SUCCESS"
        logs.append({"run_id":run_id,"invoice_id":row.get("invoice_id",""),"status":status,
                     "error_category":"DATA_ERROR" if errors else "",
                     "error_message":";".join(errors),"started_at":started,
                     "completed_at":datetime.now(timezone.utc).isoformat()})
    pd.DataFrame(accepted).to_csv(out/"processed_invoices.csv", index=False)
    pd.DataFrame(rejected).to_csv(out/"invoice_exceptions.csv", index=False)
    pd.DataFrame(logs).to_csv(out/"execution_logs.csv", index=False)
    summary = {"run_id":run_id,"total":len(df),"accepted":len(accepted),"rejected":len(rejected),
               "success_rate_pct":round(len(accepted)/len(df)*100,2) if len(df) else 0}
    pd.DataFrame([summary]).to_csv(out/"daily_summary.csv", index=False)
    db_url = os.getenv("DATABASE_URL", "sqlite:///invoice_bot.db")
    engine = create_engine(db_url)
    with engine.begin() as conn:
        if accepted:
            pd.DataFrame(accepted).to_sql("invoices", conn, if_exists="append", index=False)
        if rejected:
            pd.DataFrame(rejected).to_sql("invoice_exceptions", conn, if_exists="append", index=False)
        if logs:
            pd.DataFrame(logs).to_sql("bot_execution_logs", conn, if_exists="append", index=False)
    print("INVOICE PROCESSING COMPLETE")
    print(summary)
    print(f"Outputs: {out.resolve()}")
    print("Email is intentionally not sent by this reference script; configure A360 email action or monitoring SMTP separately.")

if __name__ == "__main__": main()
