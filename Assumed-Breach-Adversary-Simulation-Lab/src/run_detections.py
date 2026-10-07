"""Run deterministic defensive detections against synthetic lab telemetry."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "simulated_events.jsonl"
OUTPUT = ROOT / "output"
FINDINGS = OUTPUT / "detection_findings.json"
COVERAGE = OUTPUT / "coverage_report.json"

RULES = [
    {
        "id": "DET-001",
        "name": "Suspicious File Execution",
        "technique": "T1204.002",
        "tactic": "Execution",
        "severity": "High",
        "match": lambda e: e.get("event_type") == "file_execution",
    },
    {
        "id": "DET-002",
        "name": "Suspicious PowerShell Execution",
        "technique": "T1059.001",
        "tactic": "Execution",
        "severity": "High",
        "match": lambda e: e.get("process", "").lower() == "powershell.exe"
        and ("bypass" in e.get("command_line", "").lower()
             or "[simulated]" in e.get("command_line", "").lower()),
    },
    {
        "id": "DET-003",
        "name": "Account Discovery",
        "technique": "T1087",
        "tactic": "Discovery",
        "severity": "Medium",
        "match": lambda e: "whoami" in e.get("command_line", "").lower(),
    },
    {
        "id": "DET-004",
        "name": "System Information Discovery",
        "technique": "T1082",
        "tactic": "Discovery",
        "severity": "Medium",
        "match": lambda e: e.get("process", "").lower() == "systeminfo.exe",
    },
    {
        "id": "DET-005",
        "name": "Network Configuration Discovery",
        "technique": "T1016",
        "tactic": "Discovery",
        "severity": "Medium",
        "match": lambda e: "ipconfig" in e.get("command_line", "").lower(),
    },
    {
        "id": "DET-006",
        "name": "Credential Access Signal",
        "technique": "T1003",
        "tactic": "Credential Access",
        "severity": "Critical",
        "match": lambda e: e.get("event_type") == "credential_access_signal",
    },
    {
        "id": "DET-007",
        "name": "SMB Remote Service Signal",
        "technique": "T1021.002",
        "tactic": "Lateral Movement",
        "severity": "High",
        "match": lambda e: e.get("event_type") == "network_connection"
        and e.get("protocol") == "SMB"
        and e.get("destination_port") == 445,
    },
    {
        "id": "DET-008",
        "name": "Unusual HTTPS Egress Signal",
        "technique": "T1071.001",
        "tactic": "Command and Control",
        "severity": "High",
        "match": lambda e: e.get("event_type") == "network_connection"
        and e.get("protocol") == "HTTPS"
        and e.get("destination") == "198.51.100.25",
    },
    {
        "id": "DET-009",
        "name": "Archive Staging Signal",
        "technique": "T1560.001",
        "tactic": "Collection",
        "severity": "High",
        "match": lambda e: e.get("event_type") == "archive_staging",
    },
]


def load_events():
    with DATA.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> None:
    events = load_events()
    findings = []

    for event in events:
        for rule in RULES:
            if rule["match"](event):
                findings.append(
                    {
                        "detection_id": rule["id"],
                        "detection": rule["name"],
                        "severity": rule["severity"],
                        "technique": rule["technique"],
                        "tactic": rule["tactic"],
                        "event_id": event["event_id"],
                        "host": event["host"],
                        "user": event["user"],
                        "evidence": event,
                    }
                )

    OUTPUT.mkdir(exist_ok=True)
    FINDINGS.write_text(json.dumps(findings, indent=2), encoding="utf-8")

    techniques = sorted({r["technique"] for r in RULES})
    detected = sorted({f["technique"] for f in findings})
    report = {
        "total_events": len(events),
        "total_findings": len(findings),
        "severity_counts": dict(Counter(f["severity"] for f in findings)),
        "techniques_in_scope": techniques,
        "techniques_detected": detected,
        "coverage_percent": round((len(detected) / len(techniques)) * 100, 2),
    }
    COVERAGE.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
