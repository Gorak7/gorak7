# Live Lab Evidence — Capture Your Own Screenshots

This folder is reserved for screenshots and test records captured from your own running environment. No genuine live Splunk screenshots have been captured by this repository setup process.

## Required evidence
1. `01-architecture.png` — VM network and component layout.
2. `02-windows-events.png` — Splunk results showing Windows Security events and host metadata.
3. `03-sysmon-process.png` — Sysmon process event with event ID, image, parent image, and timestamp.
4. `04-linux-auth.png` — Linux authentication records from your test.
5. `05-failed-logon-detection.png` — SPL results for the controlled failed-logon test.
6. `06-network-scan-detection.png` — network detection results from a scan against your own lab target, if network telemetry is configured.
7. `07-dashboard.png` — your running Splunk dashboard.
8. `08-alert-trigger.png` — saved alert settings and a triggered result.
9. `09-incident-report.png` or a redacted Markdown/PDF report — one completed investigation.

## Capture procedure
- Capture the whole relevant Splunk panel, including search and time picker when possible.
- Keep the host, event ID, timestamp, and relevant fields visible.
- Remove credentials, tokens, personal account names, public IPs, and unrelated browser tabs.
- Do not alter a screenshot in a way that changes the meaning of the evidence. Cropping/redaction is acceptable.
- Add a short note for each file with the test ID, time, expected result, actual result, and conclusion.
- Use a consistent timezone in your incident timeline.

## Status template
Copy this for each test:
- Test ID:
- Date/time + timezone:
- Search:
- Expected:
- Observed:
- Status: PASS / FAIL / NOT RUN
- Evidence filename:
- Notes:

Do not change NOT RUN to PASS until you have run and observed the test.
