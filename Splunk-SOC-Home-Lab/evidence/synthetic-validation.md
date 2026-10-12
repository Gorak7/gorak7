# Synthetic Detection Validation

**Evidence type:** Offline, synthetic sample-data validation.  
**Not represented as:** A live Splunk screenshot, a real attack, or proof of end-to-end log forwarding.

The committed `data/synthetic-events.csv` contains fabricated records with clearly labelled lab hostnames and RFC 5737 documentation IP addresses. These records are not genuine Windows/Sysmon/Linux logs.

## Run the reproducible check
From the repository root, run:

```bash
python Splunk-SOC-Home-Lab/tests/validate_synthetic_data.py
```

The script checks the CSV structure and verifies three expected patterns:
- **SYN-01 — repeated failed logons:** five fabricated Event ID 4625 records for `labuser` from `192.0.2.25`.
- **SYN-02 — process investigation:** one fabricated Sysmon Event ID 1 record for a benign Notepad example.
- **SYN-03 — network port fan-out:** fifteen fabricated destination ports associated with `198.51.100.10`.

## Expected result
The script should report:
- 21 synthetic rows loaded.
- One failed-logon group meeting the threshold of five.
- One process-creation sample event.
- One source with fifteen distinct destination ports.
- A final synthetic validation PASS.

This validates the sample file and the test script only. It does **not** validate SPL syntax inside Splunk, log forwarding, field extraction, saved-search alert delivery, or dashboard behavior.

## Result status
| Test | Expected | Evidence status |
|---|---|---|
| SYN-01 | Five failures grouped to one source/account | Validated by local Python dataset check when run |
| SYN-02 | Process event appears in sample data | Validated by local Python dataset check when run |
| SYN-03 | Multi-port source appears above threshold | Validated by local Python dataset check when run |
| LIVE-01 | Actual Windows logs arrive in Splunk | Not verified here |
| LIVE-02 | Actual Sysmon logs arrive in Splunk | Not verified here |
| LIVE-03 | Actual Linux logs arrive in Splunk | Not verified here |
| LIVE-04 | Live alert fires in Splunk | Not verified here |

## Evidence integrity
No fabricated event or illustrative SVG in this repository should be described as captured from a real running Splunk UI. Add your own verified outputs to `evidence/live-lab/` after running the project.
