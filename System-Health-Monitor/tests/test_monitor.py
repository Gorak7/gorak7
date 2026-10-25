import importlib.util
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("monitor", Path(__file__).parents[1] / "monitor.py")
monitor = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(monitor)

def test_alert_cooldown(monkeypatch):
    monitor.STATE.clear()
    cfg = {"alert_cooldown_seconds": 60, "webhook_enabled": False}
    assert monitor.deliver_alert("cpu_percent", 90, 85, cfg, now=1000)
    assert not monitor.deliver_alert("cpu_percent", 91, 85, cfg, now=1010)
    assert monitor.deliver_alert("cpu_percent", 92, 85, cfg, now=1061)

def test_config_thresholds():
    cfg = monitor.load_config()
    assert cfg["thresholds"]["cpu_percent"] > 0
