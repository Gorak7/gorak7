# Installation and Configuration Guide

This guide describes a small, isolated learning environment. Splunk menu labels and product capabilities can vary by version and license.

## 1. Plan the lab
Suggested minimum host resources: 16 GB RAM, 4 CPU cores, and enough free disk space for three VMs. With less RAM, run only two VMs at a time. Suggested VMs:
- Splunk server: Linux or Windows, sized for a small lab
- Windows endpoint: Windows 10/11 evaluation or licensed installation
- Linux endpoint: Ubuntu Server
- Kali: optional test VM

Use a host-only or internal virtual network. Assign static lab IPs or DHCP reservations and record them in your own notes. Avoid exposing Splunk's web or receiving ports to the public internet.

## 2. Install Splunk
1. Download Splunk from the official Splunk website and choose the appropriate supported package.
2. Install it on the SIEM VM and accept the license.
3. Start Splunk and create a unique lab-only administrator password.
4. From the host or a permitted lab VM, open the Splunk Web interface (often port 8000).
5. In Settings, locate Forwarding and Receiving and configure a receiving port only if using a Universal Forwarder. The default commonly used receiving port is 9997.
6. Restrict inbound access to the private lab subnet. Do not port-forward Splunk from your router.

## 3. Configure Windows event collection
1. Enable relevant audit policy for logon events (success/failure as needed) using Local Security Policy or an equivalent managed policy.
2. Confirm failed logon events appear in Windows Event Viewer under Windows Logs > Security. Event ID 4625 is commonly used for failed logons.
3. Download Sysmon from Microsoft's official Sysinternals site.
4. Review the Sysmon configuration before installing it. Start with process creation (Event ID 1); add network connection telemetry (Event ID 3) only if required and be mindful of event volume.
5. Confirm Sysmon events appear in Event Viewer under Applications and Services Logs > Microsoft > Windows > Sysmon > Operational.

Do not copy an unknown Sysmon configuration blindly. Review exclusions, event volume, and the data you actually need.

## 4. Install a Universal Forwarder on Windows
1. Download the matching Splunk Universal Forwarder from the official Splunk site.
2. During setup, configure the receiving Splunk host and port if the installer offers those fields, or configure forwarding after installation.
3. Configure inputs for the Security and Sysmon Operational channels. Example inputs are provided in `setup/windows-inputs.example.conf`.
4. Restart the forwarder after configuration changes.
5. In Splunk Search, inspect recent events and verify host, source, sourcetype, and event fields.

The example configuration is a starting point. Verify supported stanza names and channel paths for your forwarder version.

## 5. Configure Linux collection
1. Install a Universal Forwarder on Ubuntu if suitable for your environment, or use a supported syslog ingestion approach.
2. Configure inputs for the distro's authentication and system logs. File locations differ: Ubuntu often uses `/var/log/auth.log`; some systems use `/var/log/secure` or journald.
3. Configure forwarding to the private Splunk receiver.
4. Restart the service and confirm that test SSH/authentication events appear in Splunk.

Example input stanzas are in `setup/linux-inputs.example.conf`. Use the correct path and permissions for your distro.

## 6. Verify before detection
Run a broad search in Splunk over the relevant time range:
```spl
index=* earliest=-15m
| stats count by index sourcetype host source
| sort - count
```
This inventory helps reveal the actual data model. Update the project searches to match your installed add-ons and field extractions.

## 7. Configure saved searches and alerts
1. Open Search & Reporting and run a tuned detection search.
2. Confirm the search returns the expected event set.
3. Save As > Alert (wording varies by version).
4. Start with a sensible test-only schedule and threshold.
5. Choose an action supported by your installation, such as a Splunk alert listing or email if configured.
6. Trigger the test in your isolated lab and capture the search result, alert configuration, and triggered alert.

Avoid high-frequency schedules or broad `index=*` searches in large environments. Narrow the index and sourcetype once known.

## 8. Build dashboard
Use the panel specification in `dashboards/soc-overview-dashboard.json` as a design checklist. Create panels for:
- Failed logons over time
- Top failed-logon source/account pairs
- Sysmon process creation
- Network source-to-port fan-out
- Recent alerts / investigations

Validate each panel separately before adding it to the dashboard.

## 9. Test and collect evidence
Follow `tests/test-plan.md`. For every scenario, capture:
- Test timestamp and target VM
- Exact action performed
- Search query and time range
- Event sample or event ID
- Detection result and whether it met expectation
- Screenshot of the live Splunk interface
- Any tuning required

Store genuine captures in `evidence/live-lab/`. Redact usernames, IPs, hostnames, and other private details before publishing.
