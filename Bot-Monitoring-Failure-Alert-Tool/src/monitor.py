"""CSV execution-log monitor with incident classification and opt-in SMTP alerts."""
from __future__ import annotations
import argparse, os, smtplib
from email.message import EmailMessage
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

REQUIRED=["run_id","bot_name","invoice_id","status","started_at","completed_at","duration_seconds","error_message"]
CATEGORIES={
"TIMEOUT":["timeout","timed out","exceeded limit"],
"DATABASE_ERROR":["database","sql","connection refused","integrityerror"],
"FILE_SYSTEM_ERROR":["file not found","no such file","permission denied","cannot open"],
"AUTHENTICATION_ERROR":["unauthorized","authentication","login failed","invalid credentials"],
"APPLICATION_ERROR":["application not responding","application error","element not found","window not found"],
"DATA_ERROR":["invalid invoice","missing invoice","duplicate","invalid gst","negative amount"]}

def classify(message: str,status: str="")->str:
    msg=str(message or "").lower()
    for category,phrases in CATEGORIES.items():
        if any(p in msg for p in phrases): return category
    if str(status).strip().upper()=="TIMEOUT": return "TIMEOUT"
    if msg or str(status).strip().upper() in {"FAILED","ERROR"}: return "UNKNOWN_ERROR"
    return ""

def normalize_logs(frame: pd.DataFrame)->pd.DataFrame:
    missing=[c for c in REQUIRED if c not in frame.columns]
    if missing: raise ValueError("Missing required columns: "+", ".join(missing))
    df=frame.copy().fillna("")
    for col in ["run_id","bot_name","invoice_id","status"]:
        df[col]=df[col].astype(str).str.strip()
    if (df.run_id=="").any(): raise ValueError("run_id cannot be blank")
    if (df.bot_name=="").any(): raise ValueError("bot_name cannot be blank")
    df["status"]=df.status.str.upper()
    allowed={"SUCCESS","FAILED","COMPLETED","ERROR","TIMEOUT"}
    invalid=sorted(set(df.loc[~df.status.isin(allowed),"status"]))
    if invalid: raise ValueError("Unsupported status value(s): "+", ".join(invalid))
    for col in ["started_at","completed_at"]:
        parsed=pd.to_datetime(df[col],errors="coerce",utc=True)
        if parsed.isna().any(): raise ValueError(f"Invalid or missing timestamp in {col}")
        df[col]=parsed.astype(str)
    duration=pd.to_numeric(df.duration_seconds,errors="coerce")
    if duration.isna().any() or (duration<0).any(): raise ValueError("duration_seconds must be a non-negative number")
    df["duration_seconds"]=duration
    df["error_message"]=df.error_message.astype(str)
    df["error_category"]=[classify(m,s) for m,s in zip(df.error_message,df.status)]
    return df

def send_alert(row: dict)->None:
    host=os.getenv("SMTP_HOST"); sender=os.getenv("MAIL_FROM"); recipient=os.getenv("MAIL_TO")
    if not all([host,sender,recipient]): raise RuntimeError("SMTP_HOST, MAIL_FROM and MAIL_TO must be configured")
    msg=EmailMessage()
    msg["Subject"]=f"[BOT ALERT] {row.get('bot_name')} failed — {row.get('run_id')}"
    msg["From"]=sender; msg["To"]=recipient
    msg.set_content(f"Bot: {row.get('bot_name')}\nRun: {row.get('run_id')}\nInvoice: {row.get('invoice_id')}\nCategory: {row.get('error_category')}\nError: {row.get('error_message')}\nInspect the source record and execution log; verify recovery before resolving.")
    with smtplib.SMTP(host,int(os.getenv("SMTP_PORT","587")),timeout=15) as server:
        server.starttls()
        user=os.getenv("SMTP_USERNAME")
        if user: server.login(user,os.getenv("SMTP_PASSWORD",""))
        server.send_message(msg)

def persist(engine,df,failed):
    if engine.dialect.name=="sqlite":
        with engine.begin() as conn:
            conn.execute(text("""CREATE TABLE IF NOT EXISTS bot_execution_runs (
            run_id TEXT NOT NULL,bot_name TEXT NOT NULL,invoice_id TEXT NOT NULL,status TEXT NOT NULL,
            started_at TEXT NOT NULL,completed_at TEXT NOT NULL,duration_seconds REAL NOT NULL,
            error_message TEXT,error_category TEXT,PRIMARY KEY(run_id,invoice_id))"""))
            conn.execute(text("""CREATE TABLE IF NOT EXISTS bot_incidents (
            run_id TEXT NOT NULL,invoice_id TEXT NOT NULL,bot_name TEXT NOT NULL,status TEXT NOT NULL,
            started_at TEXT NOT NULL,completed_at TEXT NOT NULL,duration_seconds REAL NOT NULL,
            error_message TEXT,error_category TEXT,incident_status TEXT NOT NULL DEFAULT 'OPEN',
            PRIMARY KEY(run_id,invoice_id))"""))
            records=df.to_dict("records")
            if records:
                conn.execute(text("""INSERT OR IGNORE INTO bot_execution_runs
                (run_id,bot_name,invoice_id,status,started_at,completed_at,duration_seconds,error_message,error_category)
                VALUES (:run_id,:bot_name,:invoice_id,:status,:started_at,:completed_at,:duration_seconds,:error_message,:error_category)"""),records)
            incidents=failed.to_dict("records")
            if incidents:
                conn.execute(text("""INSERT OR IGNORE INTO bot_incidents
                (run_id,invoice_id,bot_name,status,started_at,completed_at,duration_seconds,error_message,error_category)
                VALUES (:run_id,:invoice_id,:bot_name,:status,:started_at,:completed_at,:duration_seconds,:error_message,:error_category)"""),incidents)
    else:
        df.to_sql("bot_execution_runs",engine,if_exists="append",index=False)
        if not failed.empty:
            incidents=failed.copy(); incidents["incident_status"]="OPEN"
            incidents.to_sql("bot_incidents",engine,if_exists="append",index=False)

def monitor_file(source: Path,out: Path,database_url: str|None=None,send_email: bool=False)->dict:
    if not source.is_file(): raise FileNotFoundError(f"Log file not found: {source}")
    df=normalize_logs(pd.read_csv(source,keep_default_na=False))
    failed=df[df.status.isin(["FAILED","ERROR","TIMEOUT"])].copy()
    failed["incident_status"]="OPEN"
    out.mkdir(parents=True,exist_ok=True)
    engine=create_engine(database_url or os.getenv("DATABASE_URL","sqlite:///bot_monitor.db"))
    try: persist(engine,df,failed)
    finally: engine.dispose()
    failed.to_csv(out/"failure_analysis.csv",index=False)
    df.to_csv(out/"normalized_execution_logs.csv",index=False)
    total=len(df)
    summary={"total_runs":total,"successful_runs":int(df.status.isin(["SUCCESS","COMPLETED"]).sum()),
    "failed_runs":len(failed),"failure_rate_pct":round(len(failed)/total*100,2) if total else 0.0}
    pd.DataFrame([summary]).to_csv(out/"daily_monitoring_summary.csv",index=False)
    alert_errors=[]
    if send_email:
        for row in failed.to_dict("records"):
            try: send_alert(row)
            except Exception as exc: alert_errors.append(f"{row.get('run_id')}: {exc}")
    return {**summary,"alert_errors":alert_errors,"alerts_requested":bool(send_email)}

def main()->int:
    parser=argparse.ArgumentParser(description="Classify bot execution logs and create incident reports.")
    parser.add_argument("--input",required=True); parser.add_argument("--out",default="reports")
    parser.add_argument("--send-email",action="store_true",help="Explicitly enable SMTP alerts")
    args=parser.parse_args()
    try:
        from dotenv import load_dotenv
        load_dotenv()
        result=monitor_file(Path(args.input),Path(args.out),send_email=args.send_email)
    except Exception as exc: parser.exit(2,f"Monitoring failed: {exc}\n")
    print("MONITORING COMPLETE"); print(result)
    if result["alert_errors"]: return 1
    return 0
if __name__=="__main__": raise SystemExit(main())
