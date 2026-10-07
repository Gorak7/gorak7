"""Generate safe synthetic telemetry for the assumed-breach SOC lab.

No command in this file is executed on the host. The values represent
what endpoint/network telemetry could look like during an incident.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "simulated_events.jsonl"

EVENTS = [
    {
        "event_id": "EVT-001",
        "timestamp": "2026-10-07T10:00:00Z",
        "host": "LAB-WIN01",
        "user": "lab.user",
        "event_type": "file_execution",
        "process": "invoice_viewer.exe",
        "command_line": "invoice_viewer.exe attachment.pdf.exe [SIMULATED]",
        "source": "endpoint",
    },
    {
        "event_id": "EVT-002",
        "timestamp": "2026-10-07T10:01:20Z",
        "host": "LAB-WIN01",
        "user": "lab.user",
        "event_type": "process_start",
        "process": "powershell.exe",
        "command_line": "powershell.exe -NoProfile -ExecutionPolicy Bypass [SIMULATED]",
        "parent_process": "invoice_viewer.exe",
        "source": "endpoint",
    },
    {
        "event_id": "EVT-003",
        "timestamp": "2026-10-07T10:02:04Z",
        "host": "LAB-WIN01",
        "user": "lab.user",
        "event_type": "process_start",
        "process": "cmd.exe",
        "command_line": "cmd.exe /c whoami [SIMULATED]",
        "parent_process": "powershell.exe",
        "source": "endpoint",
    },
    {
        "event_id": "EVT-004",
        "timestamp": "2026-10-07T10:02:30Z",
        "host": "LAB-WIN01",
        "user": "lab.user",
        "event_type": "process_start",
        "process": "cmd.exe",
        "command_line": "cmd.exe /c ipconfig /all [SIMULATED]",
        "parent_process": "powershell.exe",
        "source": "endpoint",
    },
    {
        "event_id": "EVT-005",
        "timestamp": "2026-10-07T10:03:00Z",
        "host": "LAB-WIN01",
        "user": "lab.user",
        "event_type": "process_start",
        "process": "systeminfo.exe",
        "command_line": "systeminfo.exe [SIMULATED]",
        "parent_process": "powershell.exe",
        "source": "endpoint",
    },
    {
        "event_id": "EVT-006",
        "timestamp": "2026-10-07T10:04:10Z",
        "host": "LAB-WIN01",
        "user": "lab.user",
        "event_type": "credential_access_signal",
        "target": "credential_process",
        "details": "Synthetic credential-access telemetry",
        "source": "endpoint",
    },
    {
        "event_id": "EVT-007",
        "timestamp": "2026-10-07T10:05:22Z",
        "host": "LAB-WIN01",
        "user": "lab.user",
        "event_type": "network_connection",
        "destination": "10.20.30.15",
        "destination_port": 445,
        "protocol": "SMB",
        "details": "Synthetic remote-service activity",
        "source": "network",
    },
    {
        "event_id": "EVT-008",
        "timestamp": "2026-10-07T10:06:45Z",
        "host": "LAB-WIN01",
        "user": "lab.user",
        "event_type": "network_connection",
        "destination": "198.51.100.25",
        "destination_port": 443,
        "protocol": "HTTPS",
        "details": "Documentation-only TEST-NET destination",
        "source": "network",
    },
    {
        "event_id": "EVT-009",
        "timestamp": "2026-10-07T10:08:00Z",
        "host": "LAB-WIN01",
        "user": "lab.user",
        "event_type": "archive_staging",
        "path": "C:\\Lab\\staging\\documents.zip",
        "details": "Synthetic data-staging signal",
        "source": "endpoint",
    },
]


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as handle:
        for event in EVENTS:
            handle.write(json.dumps(event) + "\n")
    print(f"Wrote {len(EVENTS)} synthetic events to {OUTPUT}")


if __name__ == "__main__":
    main()
