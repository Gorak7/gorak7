# MITRE ATT&CK Detection Mapping

## Scope

This lab uses ATT&CK technique IDs as defensive classification labels. The simulator does not execute the behaviors.

| ID | Technique | Lab evidence | Detection ID |
|---|---|---|---|
| T1204.002 | User Execution: Malicious File | Synthetic attachment execution | DET-001 |
| T1059.001 | PowerShell | Synthetic suspicious PowerShell process | DET-002 |
| T1087 | Account Discovery | Synthetic whoami event | DET-003 |
| T1082 | System Information Discovery | Synthetic systeminfo event | DET-004 |
| T1016 | System Network Configuration Discovery | Synthetic ipconfig event | DET-005 |
| T1003 | OS Credential Dumping | Synthetic credential-access signal | DET-006 |
| T1021.002 | SMB/Windows Admin Shares | Synthetic SMB connection | DET-007 |
| T1071.001 | Web Protocols | Synthetic HTTPS egress signal | DET-008 |
| T1560.001 | Archive Collected Data | Synthetic archive staging | DET-009 |

## Coverage Method

Coverage is calculated as:

`detected ATT&CK techniques / techniques represented by detection rules × 100`

This is **lab coverage**, not a claim of enterprise ATT&CK coverage.
