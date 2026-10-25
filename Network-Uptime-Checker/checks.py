"""Network checks. Only use against systems you own or are authorized to monitor."""
from __future__ import annotations
import socket, time
from urllib.parse import urlparse
import requests

def check_target(target: dict) -> dict:
    started = time.perf_counter(); kind = target.get("type", "http"); timeout = float(target.get("timeout_seconds", 5)); error = None; status_code = None
    try:
        if kind == "http":
            response = requests.get(target["address"], timeout=timeout, allow_redirects=True, headers={"User-Agent":"PortfolioUptimeChecker/1.0"})
            status_code = response.status_code; ok = 200 <= status_code < 400
            if not ok: error = f"HTTP {status_code}"
        elif kind == "tcp":
            with socket.create_connection((target["host"], int(target["port"])), timeout=timeout): pass
            ok = True
        else: raise ValueError(f"Unsupported check type: {kind}")
    except (requests.RequestException, socket.timeout, OSError, KeyError, ValueError) as exc:
        ok = False; error = str(exc)[:300]
    return {"target_name": target.get("name", target.get("address", target.get("host", "unnamed"))), "check_type": kind, "ok": ok, "status_code": status_code, "latency_ms": round((time.perf_counter()-started)*1000, 2), "error": error}
