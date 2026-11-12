"""CSV bot-log monitor with classification, SQL persistence and opt-in SMTP."""
from __future__ import annotations
import argparse, os, re, smtplib
from email.message import EmailMessage
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

CATEGORIES = {
 "TIMEOUT": ["timeout", "timed out", "exceeded limit"],
 "DATABASE_ERROR": ["database", "sql", "connection refused", "integrityerror"],
 "FILE_SYSTEM_ERROR": ["file not found", "no such file", "permission denied", "cannot open"],
 "AUTHENTICATION_ERROR": ["unauthorized", "authentication", "login failed", "invalid credentials"],
 "APPLICATION_ERROR": ["application not responding", "application error", "element not found", "window not found"],
 "DATA_ERROR": ["invalid invoice", "missing invoice", "duplicate", "invalid gst", "negative amount"]
}
REQUIRED = ["run_id","bot_name","invoice_id","status","started_at","completed_at","duration_seconds","error_message"]

def classify(message: str, status: str = "") -> str:
    msg = str(message or "").lower()
    for category, phrases in CATEGORIES.items():
        if any(p in msg for p in phrases): return category
    if str(status).upper() == "TIMEOUT": return "TIMEOUT"
    return "UNKNOWN_ERROR" if msg or str(status).upper() in {"FAILED","ERROR"} else ""

def send_alert(row: dict) -> bool:
    host=os.getenv("SMTP_HOST"); sender=os.getenv("MAIL_FROM"); recipient=os.getenv("MAIL_TO")
    if not all([host,sender,recipient]): return False
    msg=EmailMessage()
    msg["Subject"]=f"[BOT ALERT] {row.get('bot_name')} failed — {row.get('run_id')}"
    msg["From"]=sender; msg["To"]=recipient
    msg.set_content(
        f"Bot: {row.get('bot_name')}\nRun: {row.get('run_id')}\nInvoice: {row.get('invoice_id')}\n"
        f"Category: {row.get('error_category')}\nError: {row.get('error_message')}\n"
        "Action: inspect the source record and bot execution log; verify recovery before resolving."
    )
    with smtplib.SMTP(host, int(os.getenv("SMTP_PORT","587")), timeout=15) as server:
        server.starttls()
        user=os.getenv("SMTP_USERNAME"); password=os.getenv("SMTP_PASSWORD")
        if user: server.login(user,password or "")
        server.send_message(msg)
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True); ap.add_argument("--out",default="reports")
    ap.add_argument("--send-email",action="store_true",help="Explicitly enable SMTP alerts")
    args=ap.parse_args()
    path=Path(args.input); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(path).fillna("")
    missing=[c for c in REQUIRED if c not in df.columns]
    if missing: raise SystemExit("Missing required columns: "+", ".join(missing))
    df["error_category"]=[classify(m,s) for m,s in zip(df.error_message,df.status)]
    failed=df[df.status.astype(str).str.upper().isin(["FAILED","ERROR","TIMEOUT"])].copy()
    failed["incident_status"]="OPEN"
    db=os.getenv("DATABASE_URL","sqlite:///bot_monitor.db")
    engine=create_engine(db)
    with engine.begin() as conn:
        df.to_sql("bot_execution_runs",conn,if_exists="append",index=False)
        if not failed.empty: failed.to_sql("bot_incidents",conn,if_exists="append",index=False)
    failed.to_csv(out/"failure_analysis.csv",index=False)
    df.to_csv(out/"normalized_execution_logs.csv",index=False)
    summary=pd.DataFrame([{
      "total_runs":len(df),"successful_runs":int(df.status.astype(str).str.upper().isin(["SUCCESS","COMPLETED"]).sum()),
      "failed_runs":len(failed),"failure_rate_pct":round(len(failed)/len(df)*100,2) if len(df) else 0
    }])
    summary.to_csv(out/"daily_monitoring_summary.csv",index=False)
    if args.send_email:
        for _,r in failed.iterrows():
            try: send_alert(r.to_dict())
            except Exception as exc: print(f"Alert send failed for {r.run_id}: {exc}")
    print("MONITORING COMPLETE")
    print(summary.to_string(index=False))
    print(f"Failure categories: {failed.error_category.value_counts().to_dict()}")
    print(f"Reports written to {out.resolve()}")
    if args.send_email: print("SMTP alert option enabled; check output for delivery errors.")

if __name__=="__main__": main()
