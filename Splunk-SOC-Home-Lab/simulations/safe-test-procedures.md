# Safe Test Procedures

All procedures are for an isolated lab with systems you own or are explicitly authorized to test. Use test accounts only.

## Scenario A — failed logons
1. On the Windows VM, create a disposable standard local test account.
2. From the VM console, attempt several incorrect passwords for that account; do not use an account that can affect production.
3. Open Event Viewer > Windows Logs > Security and verify Event ID 4625 appears.
4. Confirm the event is ingested into Splunk.
5. Run `detections/failed-logons.spl` after adjusting the index/fields/time range.
6. Record whether the threshold matches the test and check for false positives.

## Scenario B — process creation
1. Confirm Sysmon Event ID 1 is enabled and collected.
2. Open a benign application (for example, Notepad) on the Windows VM.
3. Verify the process creation event in Event Viewer and Splunk.
4. Run `detections/sysmon-process-investigation.spl`.
5. Document the image, parent image, user, and timestamp.

## Scenario C — network port fan-out
1. Verify your Kali VM and target VM are on an isolated network and record both lab IPs.
2. Confirm the target is yours and the scan is permitted.
3. Run a low-rate scan only against the target lab VM, for example:
   `nmap -sT -T2 --top-ports 20 <YOUR-LAB-TARGET-IP>`
4. Do not substitute a public IP or scan a network you do not own.
5. Verify the firewall/network telemetry source records the scan. Nmap activity will not automatically appear in Splunk unless network logging is configured and forwarded.
6. Run `detections/network-port-fanout.spl`, adapt field names, and document whether the configured threshold was met.

## Scenario D — incident response drill
For one generated alert, fill in `reports/incident-report-template.md`. Include timeline, scope, evidence, disposition, remediation, and detection tuning. Distinguish expected test traffic from real malicious activity.
