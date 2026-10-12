# Analyst Workbook — Network Traffic Analysis & IDS

## 1. Test record
- Analyst:
- Date/time and timezone:
- Host OS / VM:
- Tool versions (Wireshark, Suricata, Python):
- Capture interface:
- Scope/authorization:
- Capture duration:
- PCAP SHA-256:

## 2. Questions to answer
1. What hosts and protocols appear in the capture?
2. Are DNS query names and response addresses expected for this test?
3. Is there a repeated connection pattern or unusual port activity?
4. Did Suricata produce alerts? Which exact signature and rule SID?
5. Does the packet evidence support the alert, or could it be a false positive?
6. What additional context would be needed before classifying the activity?

## 3. Observation table
| Timestamp | Source | Destination | Protocol | Observed fact | Interpretation / confidence |
|---|---|---|---|---|---|
| Fill from your own capture | | | | | |

Keep observed facts separate from interpretations. Do not infer intent from an IP address alone.

## 4. Alert triage
For each alert, record signature, SID, severity, 5-tuple, timestamp, relevant packet numbers, rule match condition, and whether it was reproduced intentionally. Explain any false positives and missing telemetry.

## 5. Findings and recommendations
- Finding:
- Evidence references:
- Risk and confidence:
- Recommended next step:
- Limitations:

## 6. Screenshot checklist
- [ ] Wireshark overview showing packet timestamps and protocols
- [ ] DNS query/response detail, if DNS was captured
- [ ] Suricata alert output for a reproducible test
- [ ] Python JSON summary
- [ ] Hash manifest

Screenshots must be genuine captures from your own execution. Do not use the synthetic JSONL fixture as proof of live detection. Blur credentials, tokens, public IPs if sensitive, and personal identifiers before publishing.
