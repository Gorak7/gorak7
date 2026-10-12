# SOC Lab Test Plan

## Test discipline
Run tests only on lab VMs and accounts you control. Record actual timestamps, hosts, SPL, results, and screenshots. The synthetic CSV tests below validate search logic only; they do not validate event forwarding, Windows auditing, or live alert delivery.

## Test cases
| ID | Scenario | Safe method | Expected signal | Evidence |
|---|---|---|---|---|
| T01 | Baseline collection | Wait for normal Windows/Linux activity | Events searchable with correct host/index/sourcetype | Search results and event details |
| T02 | Failed logon burst | Enter an intentionally incorrect password several times for a disposable local test account | Windows Event ID 4625 or Linux auth failure records | Event IDs, source, account, timestamps |
| T03 | Process creation | Open a benign application such as Notepad | Sysmon Event ID 1 | Image, parent, user, command line |
| T04 | Port scan | Run a low-rate scan against your own isolated lab target only | Network telemetry shows one source contacting multiple ports, if collection is configured | Scan command, target, time range, network events |
| T05 | Alert trigger | Configure a test alert with a threshold suited to T02 | Alert fires once the threshold is reached | Saved-search configuration and triggered alert |
| T06 | False-positive review | Repeat expected administrative activity or a known benign scan | Analyst identifies legitimate context and tunes carefully | Before/after search and tuning note |
| T07 | Incident report | Investigate one alert end-to-end | Timeline, scope, disposition, remediation | Completed report with redacted evidence |

## Acceptance criteria
- Event exists in the source operating system.
- Matching event is ingested into Splunk within the expected delay.
- SPL returns the relevant event(s) in the correct time range.
- Alert logic fires only under the configured conditions.
- Analyst can explain limitations and plausible benign causes.
- Evidence is captured and redacted.

## Test record template
- Test ID:
- Date/time and timezone:
- Lab hosts:
- Action performed:
- Index/sourcetype:
- SPL and time range:
- Expected result:
- Actual result:
- Status: PASS / FAIL / NOT RUN
- Screenshot/evidence filename:
- Notes and tuning:
