# ELK SOC Lab Simulation

A portfolio-grade Security Operations Center lab using Elasticsearch, Logstash, Kibana, Filebeat, FastAPI and a custom analyst dashboard.

## Architecture
Synthetic telemetry → Filebeat → Logstash → Elasticsearch → Kibana / FastAPI → SOC Analyst UI.

## Features
- Centralized ELK SIEM pipeline
- Synthetic endpoint/network telemetry
- Detection rules mapped to MITRE ATT&CK
- FastAPI REST backend
- Browser-based SOC analyst console
- Alert acknowledgement workflow
- Kibana investigation workflow
- Docker Compose deployment
- Safe lab-only attack simulation

## Structure
```
ELK-SOC-Lab-Simulation/
├── backend/              # FastAPI SIEM API
├── frontend/             # Analyst dashboard
├── simulator/            # Synthetic telemetry
├── detection/            # Detection rule catalog
├── logstash/pipeline/    # Parsing + enrichment
├── filebeat/             # Log collection
├── kibana/               # Investigation guide
├── scripts/              # Start/stop/seed helpers
├── tests/                # Automated tests
├── docker-compose.yml
└── README.md
```

## Requirements
Docker Desktop/Engine with Compose v2, Git, modern browser, and 8 GB RAM recommended.

## A-Z setup
```bash
git clone https://github.com/Gorak7/gorak7.git
cd gorak7/ELK-SOC-Lab-Simulation
cp .env.example .env
docker compose up -d --build
```

Open:
- SOC dashboard: http://localhost:8000
- API/Swagger: http://localhost:8000/docs
- Kibana: http://localhost:5601
- Elasticsearch: http://localhost:9200

Generate telemetry:
```bash
docker compose --profile tools run --rm simulator python /app/generate_logs.py --scenario all --count 50
```

Then investigate the generated alerts in the SOC console and Kibana.

## Detection coverage
| Rule | Detection | ATT&CK | Severity |
|---|---|---|---|
| SOC-001 | Repeated authentication failures | T1110 | High |
| SOC-002 | Suspicious PowerShell | T1059.001 | High |
| SOC-003 | Encoded command | T1027 | High |
| SOC-004 | Phishing attachment | T1566.001 | High |
| SOC-005 | Unusual outbound transfer | T1041 | Critical |

## SOC workflow
Collect → Normalize → Enrich → Detect → Alert → Triage → Investigate → Document.

## Interview explanation
I built an isolated ELK-based SOC simulation where synthetic endpoint and network events are collected with Filebeat, parsed/enriched by Logstash, indexed in Elasticsearch, investigated in Kibana, and surfaced through a FastAPI analyst console. I also implemented deterministic detections, severity, MITRE ATT&CK mapping and alert acknowledgement.

## Resume bullet
**ELK-Based SOC SIEM & Detection Lab** — Built an end-to-end SOC simulation using Elasticsearch, Logstash, Kibana and Filebeat with a FastAPI analyst console; engineered detections for brute-force, phishing, PowerShell and data-exfiltration scenarios with MITRE ATT&CK mapping.

For authorized lab and educational use only. All attack scenarios are synthetic telemetry.
