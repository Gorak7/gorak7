# Network & Uptime Checker

A small service-monitoring backend with a minimal Flask dashboard (the only dashboard in this portfolio).

## Features
- HTTP response/status checks and TCP connection checks
- SQLite history, per-target status and latency
- APScheduler interval checks; configurable targets
- Down state after three consecutive failures and recovery event tracking
- Rolling 24-hour availability calculation and a latency chart
- Webhook alerts via environment variable, Docker Compose, and tests

## Run locally
```bash
python -m venv .venv
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`. Docker: `docker compose up --build`. Add only endpoints and hosts you own or have permission to monitor. ICMP is not enabled by default because it can require OS privileges; HTTP/TCP are supported out of the box.
