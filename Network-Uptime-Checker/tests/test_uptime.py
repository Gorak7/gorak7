import importlib.util
from pathlib import Path
from unittest.mock import Mock
import pytest

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("uptime_db", ROOT / "db.py")
db = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(db)

def result(ok, name="demo", error=None):
    return {"target_name": name, "ok": ok, "latency_ms": 12.3, "status_code": 200 if ok else None, "error": error}

def test_outage_opens_after_threshold_and_survives_reopen(tmp_path):
    path = tmp_path / "history.sqlite"
    db.init_db(path)
    assert not db.record_check(result(False), threshold=3, path=path)["outage_started"]
    assert not db.record_check(result(False), threshold=3, path=path)["outage_started"]
    state = db.record_check(result(False), threshold=3, path=path)
    assert state["outage_started"] and state["is_down"]
    # Simulate process restart by reinitializing and querying a fresh connection.
    db.init_db(path)
    assert db.target_states(path)["demo"]["is_down"] == 1
    outages = db.outage_history(path)
    assert len(outages) == 1 and outages[0]["ended_at"] is None

def test_recovery_closes_persistent_outage(tmp_path):
    path = tmp_path / "history.sqlite"
    db.init_db(path)
    for _ in range(3): db.record_check(result(False), threshold=3, path=path)
    state = db.record_check(result(True), threshold=3, path=path)
    assert state["outage_recovered"] and not state["is_down"]
    outage = db.outage_history(path)[0]
    assert outage["ended_at"] is not None
    assert db.target_states(path)["demo"]["consecutive_failures"] == 0

def test_uptime_percentage_is_calculated(tmp_path):
    path = tmp_path / "history.sqlite"
    db.init_db(path)
    db.record_check(result(True), path=path)
    db.record_check(result(False), path=path)
    assert db.uptime_percent("demo", path=path) == 50.0

def test_http_check_and_tcp_error(monkeypatch):
    spec = importlib.util.spec_from_file_location("checks", ROOT / "checks.py")
    checks = importlib.util.module_from_spec(spec); spec.loader.exec_module(checks)
    monkeypatch.setattr(checks.requests, "get", lambda *a, **k: Mock(status_code=200))
    assert checks.check_target({"name":"http","type":"http","address":"https://example.invalid"})["ok"]
    monkeypatch.setattr(checks.socket, "create_connection", lambda *a, **k: (_ for _ in ()).throw(OSError("refused")))
    out = checks.check_target({"name":"tcp","type":"tcp","host":"127.0.0.1","port":9})
    assert not out["ok"] and "refused" in out["error"]

def test_webhook_delivery_success_and_failure(monkeypatch):
    spec = importlib.util.spec_from_file_location("uptime_app", ROOT / "app.py")
    appmod = importlib.util.module_from_spec(spec); spec.loader.exec_module(appmod)
    monkeypatch.setenv("ALERT_WEBHOOK_URL", "https://webhook.example/test")
    monkeypatch.setattr(appmod.requests, "post", lambda *a, **k: Mock(raise_for_status=lambda: None))
    assert appmod.send_alert("OUTAGE: demo")
    def fail(*a, **k):
        import requests
        raise requests.Timeout("simulated timeout")
    monkeypatch.setattr(appmod.requests, "post", fail)
    assert not appmod.send_alert("RECOVERY: demo")
