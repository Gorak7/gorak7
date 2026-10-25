"""Local system health monitoring with configurable thresholds and alert cooldowns."""
from __future__ import annotations
import argparse, json, logging, os, time
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime, timezone
import psutil, requests, yaml

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
LOGS = ROOT / "logs"
STATE: dict[str, float] = {}

def setup_logging() -> None:
    LOGS.mkdir(exist_ok=True)
    handler = RotatingFileHandler(LOGS / "health-monitor.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", handlers=[handler, logging.StreamHandler()])

def load_config(path: Path = ROOT / "config.yaml") -> dict:
    with path.open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    cfg.setdefault("thresholds", {})
    cfg.setdefault("alert_cooldown_seconds", 900)
    return cfg

def collect_metrics() -> dict:
    disk = psutil.disk_usage(str(ROOT.anchor or "/"))
    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try: procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied): continue
    procs.sort(key=lambda p: float(p.get("cpu_percent") or 0), reverse=True)
    return {"timestamp": datetime.now(timezone.utc).isoformat(), "cpu_percent": psutil.cpu_percent(interval=0.2), "memory_percent": psutil.virtual_memory().percent, "disk_percent": disk.percent, "top_processes": procs[:5]}

def deliver_alert(metric: str, value: float, threshold: float, cfg: dict, now: float | None = None) -> bool:
    now = time.time() if now is None else now
    cooldown = int(cfg.get("alert_cooldown_seconds", 900))
    if now - STATE.get(metric, 0) < cooldown: return False
    logging.warning("Threshold crossed: %s=%.1f%% (threshold %.1f%%)", metric, value, threshold)
    if cfg.get("webhook_enabled"):
        url = os.getenv("ALERT_WEBHOOK_URL")
        if not url:
            logging.error("webhook_enabled is true but ALERT_WEBHOOK_URL is not set")
        else:
            try: requests.post(url, json={"text": f"System alert: {metric} {value:.1f}% exceeds {threshold:.1f}%"}, timeout=5).raise_for_status()
            except requests.RequestException as exc: logging.error("Alert delivery failed: %s", exc)
    STATE[metric] = now
    return True

def run_once(cfg: dict) -> dict:
    metrics = collect_metrics()
    DATA.mkdir(exist_ok=True)
    with (DATA / "metrics.jsonl").open("a", encoding="utf-8") as f: f.write(json.dumps(metrics) + "\n")
    for metric, threshold in cfg.get("thresholds", {}).items():
        value = metrics.get(metric)
        if isinstance(value, (int, float)) and value >= float(threshold): deliver_alert(metric, value, float(threshold), cfg)
    logging.info("Collected CPU %.1f%%, memory %.1f%%, disk %.1f%%", metrics["cpu_percent"], metrics["memory_percent"], metrics["disk_percent"])
    return metrics

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true", help="collect one snapshot")
    parser.add_argument("--interval", type=int, default=60, help="seconds between snapshots (minimum 5)")
    parser.add_argument("--config", type=Path, default=ROOT / "config.yaml")
    args = parser.parse_args()
    if args.interval < 5: parser.error("--interval must be at least 5 seconds")
    setup_logging(); cfg = load_config(args.config)
    if args.once: run_once(cfg); return
    while True:
        try: run_once(cfg)
        except Exception: logging.exception("Monitoring cycle failed")
        time.sleep(args.interval)

if __name__ == "__main__": main()
