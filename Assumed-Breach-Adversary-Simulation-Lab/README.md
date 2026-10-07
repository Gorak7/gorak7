# Assumed-Breach Adversary Simulation Lab with Detection Mapping

A controlled blue-team lab that models an assumed-breach scenario using **synthetic endpoint/network telemetry**, maps observed behaviors to **MITRE ATT&CK**, and evaluates defensive detections.

> **Safety:** This project does not execute malware, exploit real systems, steal credentials, or perform persistence/evasion. The adversary activity is represented as structured lab events so the focus stays on detection engineering, SOC investigation, and ATT&CK coverage.

## 🎯 Objectives

- Simulate a realistic assumed-breach attack storyline with safe synthetic events.
- Normalize endpoint and network events into a small SOC telemetry schema.
- Map behaviors to MITRE ATT&CK techniques and tactics.
- Run deterministic detections against the simulated telemetry.
- Produce analyst-friendly findings with severity, evidence, technique, and recommended response.
- Demonstrate how a SOC can measure detection coverage and identify gaps.

## 🏗️ Architecture

```text
Scenario
   |
   v
Synthetic Telemetry Generator
   |
   +---- endpoint events
   +---- authentication events
   +---- network events
   |
   v
Normalized JSONL Events
   |
   +-------------------+
   |                   |
   v                   v
Detection Rules     ATT&CK Mapping
   |                   |
   +---------+---------+
             v
       Analyst Findings
             |
             v
     Investigation / Response
```

## 🔴 Scenario

The lab assumes that an attacker has obtained an initial foothold on a test workstation.

The simulated storyline is:

1. **Initial Access** — suspicious attachment execution is represented as a telemetry event.
2. **Execution** — a PowerShell process launches with suspicious characteristics.
3. **Discovery** — commands such as `whoami`, `ipconfig`, and `systeminfo` are represented as events.
4. **Credential Access Attempt** — a synthetic event represents access to a credential-related process.
5. **Lateral Movement Attempt** — a synthetic SMB/remote-service connection is represented.
6. **Command & Control** — a synthetic outbound connection to an unusual external destination is represented.
7. **Impact Signal** — a synthetic archive/staging event represents suspicious collection preparation.

No real payloads or offensive commands are executed.

## 🧩 MITRE ATT&CK Detection Mapping

| Event / Behavior | ATT&CK Technique | Tactic | Detection |
|---|---|---|---|
| Suspicious attachment execution | T1204.002 User Execution: Malicious File | Initial Access / Execution | DET-001 |
| Suspicious PowerShell | T1059.001 PowerShell | Execution | DET-002 |
| Account discovery | T1087 | Discovery | DET-003 |
| System information discovery | T1082 | Discovery | DET-004 |
| Network configuration discovery | T1016 | Discovery | DET-005 |
| Credential access signal | T1003 | Credential Access | DET-006 |
| SMB/remote service signal | T1021.002 SMB/Windows Admin Shares | Lateral Movement | DET-007 |
| Unusual outbound connection | T1071.001 Web Protocols | Command and Control | DET-008 |
| Data staging/archive signal | T1560.001 Archive Collected Data | Collection | DET-009 |

## 🚀 Quick Start

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
python src/generate_lab_telemetry.py
python src/run_detections.py
```

The generated findings are written to:

```text
output/detection_findings.json
output/coverage_report.json
```

## 📁 Project Structure

```text
Assumed-Breach-Adversary-Simulation-Lab/
├── data/
│   └── simulated_events.jsonl
├── detections/
│   ├── sigma/
│   │   ├── suspicious_powershell.yml
│   │   └── discovery_commands.yml
│   ├── splunk/
│   │   └── detection_rules.spl
│   └── sentinel/
│       └── detection_rules.kql
├── docs/
│   ├── attack-mapping.md
│   └── investigation-playbook.md
├── src/
│   ├── generate_lab_telemetry.py
│   └── run_detections.py
├── tests/
│   └── test_detections.py
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

## 🔎 Detection Engineering

The Python detection engine demonstrates four SOC concepts:

- **Event normalization** — consistent fields such as timestamp, host, user, process, event_type and destination.
- **Rule logic** — deterministic matching of suspicious behaviors.
- **ATT&CK enrichment** — every finding is mapped to a technique and tactic.
- **Risk prioritization** — severity is based on behavior and correlation.

Example normalized event:

```json
{
  "event_id": "EVT-004",
  "timestamp": "2026-10-07T10:03:12Z",
  "host": "LAB-WIN01",
  "user": "lab.user",
  "event_type": "process_start",
  "process": "powershell.exe",
  "command_line": "powershell.exe -NoProfile -ExecutionPolicy Bypass [SIMULATED]",
  "source": "endpoint"
}
```

## 🛡️ SOC Investigation Workflow

1. Validate the alert and identify the affected host/user.
2. Pivot across the event timeline.
3. Identify the first suspicious event.
4. Determine which ATT&CK techniques are represented.
5. Scope related hosts, users, destinations, and processes.
6. Contain the simulated endpoint.
7. Reset potentially exposed credentials in a real incident.
8. Block malicious infrastructure if confirmed.
9. Document root cause and evidence.
10. Tune the detection to reduce false positives.

See [docs/investigation-playbook.md](docs/investigation-playbook.md).

## 📊 Detection Coverage

The lab tracks:

- Number of ATT&CK techniques represented.
- Techniques detected.
- Techniques without a detection.
- Severity distribution.
- Detection-to-technique relationships.

This makes the project useful for demonstrating **SOC monitoring, SIEM correlation, MITRE ATT&CK, incident triage, and detection engineering**.

## 🧪 Testing

```bash
python -m unittest discover -s tests -v
```

## 🔐 Ethics and Scope

Use this lab only for defensive education and authorized testing. The simulator intentionally uses synthetic telemetry rather than executing adversary tooling against live systems.

## 👤 Portfolio Value

This project demonstrates practical exposure to:

**SOC Operations • SIEM • Detection Engineering • MITRE ATT&CK • Log Analysis • Incident Response • Threat Detection • Security Monitoring • Python • Sigma • Splunk SPL • Microsoft Sentinel KQL**
