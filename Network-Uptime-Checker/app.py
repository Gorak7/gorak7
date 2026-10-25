"""Flask dashboard and background monitoring scheduler."""
from __future__ import annotations
import logging, os
from pathlib import Path
from flask import Flask, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import yaml, requests
from checks import check_target
import db
ROOT=Path(__file__).resolve().parent
app=Flask(__name__); scheduler=BackgroundScheduler(daemon=True); STATE={}; logger=logging.getLogger("uptime")

def config():
    return yaml.safe_load((ROOT/"targets.yaml").read_text(encoding="utf-8")) or {}

def run_checks():
    cfg=config(); threshold=int(cfg.get("consecutive_failures_for_down",3))
    for target in cfg.get("targets",[]):
        result=check_target(target); name=result["target_name"]; db.record(result); prev=STATE.get(name,{"failures":0,"down":False})
        prev["failures"]=0 if result["ok"] else prev["failures"]+1
        if not result["ok"] and prev["failures"] >= threshold and not prev["down"]:
            prev["down"]=True; send_alert(f"OUTAGE: {name} failed {prev['failures']} consecutive checks")
        elif result["ok"] and prev["down"]:
            prev["down"]=False; send_alert(f"RECOVERY: {name} is responding again")
        STATE[name]=prev

def send_alert(message):
    url=os.getenv("ALERT_WEBHOOK_URL")
    if not url: logger.warning(message); return
    try: requests.post(url,json={"text":message},timeout=5).raise_for_status()
    except requests.RequestException: logger.exception("Alert webhook failed")

@app.get("/")
def dashboard():
    rows=db.recent(); latest={}
    for row in rows:
        if row["target_name"] not in latest: latest[row["target_name"]]=row
    targets=[]
    for t in config().get("targets",[]):
        name=t.get("name",t.get("address",t.get("host"))); row=latest.get(name); state=STATE.get(name,{"down":False})
        targets.append({"name":name,"ok":bool(row["ok"]) if row else None,"latency":row["latency_ms"] if row else None,"last_checked":row["checked_at"] if row else None,"down":state["down"],"uptime":db.uptime_percent(name)})
    return render_template("dashboard.html",targets=targets,history=list(reversed(rows[:60])))

@app.get("/api/health")
def health(): return jsonify({"status":"ok"})

@app.get("/api/status")
def status():
    rows=db.recent(); return jsonify({"targets":config().get("targets",[]),"recent_checks":rows,"state":STATE})

def start_scheduler():
    if not scheduler.running:
        interval=max(15,int(config().get("interval_seconds",60))); scheduler.add_job(run_checks,"interval",seconds=interval,id="checks",replace_existing=True); scheduler.start()

if __name__=="__main__":
    logging.basicConfig(level=logging.INFO); db.init_db(); start_scheduler(); run_checks(); app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")),debug=False)
