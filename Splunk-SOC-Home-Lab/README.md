# SOC Home Lab with Splunk SIEM

A reproducible, isolated home lab for learning log ingestion, security monitoring, alerting, and incident triage with Splunk, Windows Event Logs, Sysmon, Linux logs, and Kali Linux.

> **Status:** Project blueprint and detection content. Complete the hands-on setup, validate searches against your own telemetry, and add your own screenshots before describing it as fully implemented on a resume.

## Objectives
- Centralize Windows, Sysmon, and Linux security telemetry in Splunk.
- Investigate authentication failures, suspicious process activity, and network scanning.
- Create SPL searches, scheduled alerts, and dashboards.
- Document evidence, triage, containment, and remediation.

## Lab architecture
1. **Windows endpoint:** Windows VM; enable Security auditing and install Sysmon.
2. **Linux endpoint:** Ubuntu/Debian VM with SSH/authentication and system logs.
3. **SIEM:** Splunk Enterprise trial or another suitable Splunk lab deployment.
4. **Test host:** Kali Linux VM on an isolated host-only/internal virtual network. Scan only systems you own or are authorized to test.
5. **Analyst:** Use Splunk Search & Reporting to investigate events, create dashboards, and configure alerts.

Keep VMs isolated from production networks. Use snapshots and test accounts. Never use real credentials or scan unapproved targets.

## Suggested data sources
- Windows Security events (for example, failed logon Event ID 4625)
- Sysmon Operational events (for example, process creation Event ID 1)
- Linux authentication and system logs
- Network telemetry from a firewall, Zeek, Suricata, or another configured source, if available

Index and sourcetype names depend on your configuration. Inspect incoming events first, then adapt the sample searches to your real field names.

## Setup workflow
1. Install a hypervisor such as VirtualBox or VMware Workstation.
2. Create Windows, Linux, and Kali VMs on a private lab network.
3. Install Splunk and note the management URL, commonly http://<splunk-host>:8000.
4. Enable Windows Security auditing and install Sysmon using the official Sysinternals release and a reviewed configuration.
5. Install/configure Splunk Universal Forwarder or another supported ingestion method on endpoints.
6. Verify events arrive; note their index, sourcetype, host, and extracted fields.
7. Run the searches in searches/ and adjust them to match the data.
8. Generate benign test activity: failed logons against a test account and a low-rate Nmap scan of your own lab VM.
9. Validate the searches against timestamps and source hosts; tune thresholds to reduce noise.
10. Build dashboards and document evidence, outcomes, and remediation.

## Detection content
- searches/failed-logons.spl — investigate repeated Windows failed logons.
- searches/sysmon-process-creation.spl — investigate Sysmon process creation events.
- searches/port-scan-baseline.spl — detect high destination-port fan-out when compatible network telemetry exists.

These are starting-point examples, not universal plug-and-play detections. Verify field names and tune thresholds for your environment.

## Dashboard panels
1. Failed logons over time.
2. Top source hosts/users for failed logons.
3. Process creation by host and image.
4. Network destinations or destination ports per source host.
5. Recent alerts and high-priority events.

## Incident triage runbook
1. Record alert name, time range, host, user, source IP, and relevant event IDs.
2. Validate the event and review related events before and after it.
3. Determine whether the activity is expected lab testing or suspicious.
4. Scope related hosts/accounts and preserve relevant evidence.
5. Recommend proportionate remediation, such as resetting a test password or restricting a test port.
6. Record disposition, confidence, and follow-up tuning.

## Deliverables checklist
- [ ] VM and network architecture screenshot
- [ ] Ingestion proof for Windows, Sysmon, and Linux
- [ ] SPL results for each scenario
- [ ] Dashboard screenshot
- [ ] Alert configuration and trigger validation
- [ ] Incident report with evidence and remediation
- [ ] False-positive notes and limitations

## Troubleshooting
- **No events:** check forwarder service, receiving configuration, network reachability, and inputs.
- **Wrong index/sourcetype:** inspect event metadata and update the searches.
- **Fields missing:** inspect raw events and configure the appropriate add-on/parser.
- **Too many alerts:** tune thresholds against normal lab activity and group results by host/user.

## Resume entry (use only after validation)
**SOC Home Lab with Splunk SIEM** | Splunk, Sysmon, Windows, Linux, Kali Linux, Nmap
- Configured centralized Windows, Sysmon, and Linux log monitoring in Splunk and investigated authentication and endpoint events.
- Developed SPL searches and alert logic for repeated failed logons, suspicious process activity, and network-scan patterns.
- Built security dashboards and documented incident triage, evidence, and remediation recommendations.

## References
- Splunk Search Reference: https://docs.splunk.com/Documentation/Splunk/latest/SearchReference
- Microsoft Sysinternals Sysmon: https://learn.microsoft.com/sysinternals/downloads/sysmon
- Splunk Universal Forwarder: https://docs.splunk.com/Documentation/Forwarder
- Nmap Reference Guide: https://nmap.org/book/man.html
