"""Flask dashboard and background monitoring scheduler."""
from __future__ import annotations
import logging, os
from pathlib import Path
from flask import Flask, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import yaml, requests
from checks import check_target
import db

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)
scheduler = BackgroundScheduler(daemon=True)
logger = logging.getLogger("uptime")

def config():
    return yaml.safe_load((ROOT / "targets.yaml").read_text(encoding="utf-8")) or {}

def run_checks():
    cfg = config()
    threshold = int(cfg.get("consecutive_failures_for_down", 3))
    for target in cfg.get("targets", []):
        result = check_target(target)
        state = db.record_check(result, threshold=threshold, path=db.DB_PATH)
        name = result["target_name"]
        if state["outage_started"]:
            send_alert(f"OUTAGE: {name} failed {state['consecutive_failures']} consecutive checks")
        elif state["outage_recovered"]:
            send_alert(f"RECOVERY: {name} is responding again")

def send_alert(message):
    """Send optional webhook alert; report delivery success/failure without crashing checks."""
    url = os.getenv("ALERT_WEBHOOK_URL")
    if not url:
        logger.warning("Alert not delivered (ALERT_WEBHOOK_URL is unset): %s", message)
        return False
    try:
        response = requests.post(url, json={"text": message}, timeout=5)
        response.raise_for_status()
        logger.info("Alert webhook delivered")
        return True
    except requests.RequestException:
        logger.exception("Alert webhook delivery failed")
        return False

@app.get("/")
def dashboard():
    rows = db.recent(path=db.DB_PATH)
    latest = {}
    for row in rows:
        if row["target_name"] not in latest:
            latest[row["target_name"]] = row
    states = db.target_states(path=db.DB_PATH)
    targets = []
    for t in config().get("targets", []):
        name = t.get("name", t.get("address", t.get("host")))
        row = latest.get(name)
        state = states.get(name, {})
        targets.append({"name": name, "ok": bool(row["ok"]) if row else None,
                        "latency": row["latency_ms"] if row else None,
                        "last_checked": row["checked_at"] if row else None,
                        "down": bool(state.get("is_down", 0)),
                        "uptime": db.uptime_percent(name, path=db.DB_PATH)})
    return render_template("dashboard.html", targets=targets, history=list(reversed(rows[:60])))

@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/api/status")
def status():
    return jsonify({"targets": config().get("targets", []),
                    "recent_checks": db.recent(path=db.DB_PATH),
                    "state": db.target_states(path=db.DB_PATH),
                    "outages": db.outage_history(path=db.DB_PATH)})

def start_scheduler():
    if not scheduler.running:
        interval = max(15, int(config().get("interval_seconds", 60)))
        scheduler.add_job(run_checks, "interval", seconds=interval, id="checks", replace_existing=True)
        scheduler.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    db.init_db()
    start_scheduler()
    run_checks()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
