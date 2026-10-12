# Synthetic Detection Validation

**Evidence type:** Offline, synthetic sample-data validation.  
**Not represented as:** A live Splunk screenshot, a real attack, or proof of end-to-end log forwarding.

The committed file `data/synthetic-events.csv` contains fabricated records with clearly labelled lab hostnames and RFC 5737 documentation IP addresses. It can be used to sanity-check detection logic and practice triage. These records are not genuine Windows/Sysmon/Linux logs.

## Expected observations
- **SYN-01 — repeated failed logons:** the sample source 192.0.2.25 has five failed-logon records for the lab test account. A threshold of five within the same test window should identify it.
- **SYN-02 — process investigation:** the dataset includes a synthetic Sysmon process-creation event for a benign test application. The process query should surface its image, parent, and account fields when the sample is mapped into the expected schema.
- **SYN-03 — network port fan-out:** the dataset includes a synthetic source contacting multiple destination ports. A distinct-port threshold should identify it if the records are ingested with compatible field mappings.

## Reproduce
1. Review the CSV and note that its records are fabricated.
2. Import it into a temporary test index or use it to create a small test dataset in your preferred local workflow.
3. Map columns to the fields used by the SPL.
4. Run the searches over the sample's time range.
5. Record the exact query and actual output; do not mark a live-lab test passed based only on this file.

## Result status
| Test | Expected | Current status |
|---|---|---|
| SYN-01 | Five failures grouped to one source/account | Sample data prepared; live Splunk execution not verified here |
| SYN-02 | Process event appears in investigation table | Sample data prepared; live Splunk execution not verified here |
| SYN-03 | Multi-port source appears above threshold | Sample data prepared; live Splunk execution not verified here |

## Evidence integrity
No fabricated event or illustrative SVG in this repository should be described as captured from a real running Splunk UI. Add your own verified outputs to `evidence/live-lab/` after running the project.
