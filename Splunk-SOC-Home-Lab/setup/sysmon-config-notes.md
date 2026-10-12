# Sysmon Setup Notes

## Purpose
Sysmon is a Windows system service and driver that records detailed activity to the Sysmon Operational event log. It complements, rather than replaces, Windows Security auditing.

## Suggested initial scope
- Process creation (Event ID 1): useful for parent/child process and command-line investigation.
- Network connection (Event ID 3): optional; can be high-volume and is often disabled by default in some configurations.
- DNS query (Event ID 22): optional, depending on investigation needs and configuration.

Use Microsoft's official Sysmon download and review the configuration file before deployment. Keep the initial scope small so you can understand what is collected.

## Verify installation
1. Open Event Viewer.
2. Navigate to Applications and Services Logs > Microsoft > Windows > Sysmon > Operational.
3. Confirm recent events exist.
4. Create a benign process such as opening Notepad and verify a process creation event appears.
5. Confirm Splunk receives the same event and inspect the raw fields before relying on a search.

## Important field caveat
Common Sysmon XML event fields include Image, CommandLine, ParentImage, User, ProcessId, and ParentProcessId. Splunk field extractions depend on input format, add-ons, and configuration. Inspect actual raw events and extracted fields before using the project searches.
