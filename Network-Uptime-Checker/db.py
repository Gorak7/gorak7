"""SQLite persistence and uptime calculations."""
import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta
DB_PATH = Path(__file__).resolve().parent / "uptime.db"

def connect(path=DB_PATH):
    db=sqlite3.connect(path); db.row_factory=sqlite3.Row; return db

def init_db(path=DB_PATH):
    with connect(path) as db:
        db.execute('''CREATE TABLE IF NOT EXISTS checks(id INTEGER PRIMARY KEY, target_name TEXT NOT NULL, checked_at TEXT NOT NULL, ok INTEGER NOT NULL, latency_ms REAL NOT NULL, status_code INTEGER, error TEXT)''')
        db.execute('''CREATE TABLE IF NOT EXISTS outages(id INTEGER PRIMARY KEY, target_name TEXT NOT NULL, started_at TEXT NOT NULL, ended_at TEXT)''')

def record(result, path=DB_PATH):
    with connect(path) as db:
        db.execute("INSERT INTO checks(target_name,checked_at,ok,latency_ms,status_code,error) VALUES(?,?,?,?,?,?)",(result["target_name"],datetime.now(timezone.utc).isoformat(),int(result["ok"]),result["latency_ms"],result.get("status_code"),result.get("error")))

def recent(path=DB_PATH, hours=24):
    since=(datetime.now(timezone.utc)-timedelta(hours=hours)).isoformat()
    with connect(path) as db: return [dict(r) for r in db.execute("SELECT * FROM checks WHERE checked_at >= ? ORDER BY id DESC LIMIT 500",(since,))]

def uptime_percent(target_name, path=DB_PATH, hours=24):
    since=(datetime.now(timezone.utc)-timedelta(hours=hours)).isoformat()
    with connect(path) as db: row=db.execute("SELECT COUNT(*) total, COALESCE(SUM(ok),0) good FROM checks WHERE target_name=? AND checked_at>=?",(target_name,since)).fetchone()
    return round(100*row["good"]/row["total"],2) if row["total"] else None
