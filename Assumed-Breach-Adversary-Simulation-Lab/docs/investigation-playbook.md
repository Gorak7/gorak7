# SOC Investigation Playbook

## 1. Triage

Capture:

- Alert ID
- Host
- User
- Timestamp
- Detection ID
- ATT&CK technique
- Initial evidence

Classify the alert as true positive, benign positive, or false positive.

## 2. Timeline Reconstruction

Build a timeline from the first suspicious event through the latest related activity.

Prioritize:

1. File execution
2. Process creation
3. Discovery activity
4. Credential-access signal
5. Lateral-movement signal
6. Network egress
7. Collection/staging

## 3. Scoping Questions

- Is the same user active on other hosts?
- Did the same parent process appear elsewhere?
- Are other endpoints communicating with the destination?
- Are there authentication anomalies?
- Does the activity correspond to an approved administrative task?
- Are there related alerts in the same time window?

## 4. Containment

For a real confirmed incident:

- Isolate the affected endpoint.
- Disable or reset compromised credentials where appropriate.
- Block confirmed malicious infrastructure.
- Preserve relevant logs and forensic evidence.
- Escalate according to the organization's incident-response plan.

## 5. Eradication and Recovery

- Remove the confirmed root cause.
- Patch the exploited weakness if applicable.
- Restore systems from trusted sources.
- Monitor for recurrence.
- Validate that detections continue to trigger.

## 6. Detection Tuning

For each false positive, document:

- Why it triggered.
- What legitimate behavior caused it.
- A safe exclusion or additional condition.
- The expected impact on detection coverage.

Never suppress an alert solely because it is noisy without documenting the risk.
