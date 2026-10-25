import importlib.util
from pathlib import Path
from unittest.mock import Mock
SPEC=importlib.util.spec_from_file_location("checks",Path(__file__).parents[1]/"checks.py")
mod=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(mod)

def test_http_status_and_latency(monkeypatch):
    response=Mock(status_code=200)
    monkeypatch.setattr(mod.requests,"get",lambda *a,**k:response)
    result=mod.check_target({"name":"test","type":"http","address":"https://example.invalid"})
    assert result["ok"] is True and result["status_code"] == 200

def test_tcp_failure_is_reported(monkeypatch):
    def fail(*a,**k): raise OSError("connection refused")
    monkeypatch.setattr(mod.socket,"create_connection",fail)
    result=mod.check_target({"name":"test","type":"tcp","host":"127.0.0.1","port":9})
    assert result["ok"] is False and "refused" in result["error"]
