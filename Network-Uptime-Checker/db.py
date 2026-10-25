"""SQLite persistence for check history and outage state across restarts."""
import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta

DB_PATH = Path(__file__).resolve().parent / "data" / "uptime.db"

def connect(path=DB_PATH):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    return db

def init_db(path=DB_PATH):
    with connect(path) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS checks(
            id INTEGER PRIMARY KEY, target_name TEXT NOT NULL, checked_at TEXT NOT NULL,
            ok INTEGER NOT NULL, latency_ms REAL NOT NULL, status_code INTEGER, error TEXT)""")
        db.execute("""CREATE TABLE IF NOT EXISTS outages(
            id INTEGER PRIMARY KEY, target_name TEXT NOT NULL, started_at TEXT NOT NULL, ended_at TEXT)""")
        db.execute("""CREATE TABLE IF NOT EXISTS target_state(
            target_name TEXT PRIMARY KEY, consecutive_failures INTEGER NOT NULL DEFAULT 0,
            is_down INTEGER NOT NULL DEFAULT 0, last_checked_at TEXT)""")

def record_check(result, threshold=3, path=DB_PATH):
    """Persist a check and atomically update outage state. Returns transition details."""
    init_db(path)
    now = datetime.now(timezone.utc).isoformat()
    name = result["target_name"]
    with connect(path) as db:
        db.execute("INSERT INTO checks(target_name,checked_at,ok,latency_ms,status_code,error) VALUES(?,?,?,?,?,?)",
                   (name, now, int(result["ok"]), result["latency_ms"], result.get("status_code"), result.get("error")))
        old = db.execute("SELECT consecutive_failures,is_down FROM target_state WHERE target_name=?", (name,)).fetchone()
        failures = 0 if result["ok"] else (old["consecutive_failures"] + 1 if old else 1)
        was_down = bool(old["is_down"]) if old else False
        is_down = was_down
        outage_started = outage_recovered = False
        if not result["ok"] and failures >= max(1, int(threshold)) and not was_down:
            is_down = True
            outage_started = True
            db.execute("INSERT INTO outages(target_name,started_at,ended_at) VALUES(?,?,NULL)", (name, now))
        elif result["ok"] and was_down:
            is_down = False
            outage_recovered = True
            db.execute("UPDATE outages SET ended_at=? WHERE target_name=? AND ended_at IS NULL", (now, name))
        db.execute("""INSERT INTO target_state(target_name,consecutive_failures,is_down,last_checked_at)
                      VALUES(?,?,?,?) ON CONFLICT(target_name) DO UPDATE SET
                      consecutive_failures=excluded.consecutive_failures,
                      is_down=excluded.is_down,last_checked_at=excluded.last_checked_at""",
                   (name, failures, int(is_down), now))
    return {"is_down": is_down, "consecutive_failures": failures,
            "outage_started": outage_started, "outage_recovered": outage_recovered}

def record(result, path=DB_PATH):
    """Compatibility helper for recording a raw check without outage transitions."""
    init_db(path)
    with connect(path) as db:
        db.execute("INSERT INTO checks(target_name,checked_at,ok,latency_ms,status_code,error) VALUES(?,?,?,?,?,?)",
                   (result["target_name"], datetime.now(timezone.utc).isoformat(), int(result["ok"]),
                    result["latency_ms"], result.get("status_code"), result.get("error")))

def recent(path=DB_PATH, hours=24):
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    with connect(path) as db:
        return [dict(r) for r in db.execute(
            "SELECT * FROM checks WHERE checked_at >= ? ORDER BY id DESC LIMIT 500", (since,))]

def uptime_percent(target_name, path=DB_PATH, hours=24):
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    with connect(path) as db:
        row = db.execute("SELECT COUNT(*) total, COALESCE(SUM(ok),0) good FROM checks WHERE target_name=? AND checked_at>=?",
                         (target_name, since)).fetchone()
    return round(100 * row["good"] / row["total"], 2) if row["total"] else None

def target_states(path=DB_PATH):
    with connect(path) as db:
        return {r["target_name"]: dict(r) for r in db.execute("SELECT * FROM target_state")}

def outage_history(path=DB_PATH, limit=100):
    with connect(path) as db:
        return [dict(r) for r in db.execute("SELECT * FROM outages ORDER BY id DESC LIMIT ?", (int(limit),))]
