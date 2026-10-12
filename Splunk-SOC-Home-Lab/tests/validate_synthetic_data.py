#!/usr/bin/env python3
"""Validate the committed SYNTHETIC sample dataset. This does not test live Splunk."""
import csv
from collections import Counter, defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "synthetic-events.csv"

def main():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert rows, "No sample rows loaded"
    assert all("SYNTHETIC" in (row.get("notes") or "") for row in rows), (
        "Every sample record must remain clearly labelled SYNTHETIC"
    )

    failures = Counter()
    for row in rows:
        if row["record_type"] == "windows_security" and row["EventCode"] == "4625":
            failures[(row["source_ip"], row["target_user"])] += 1

    process_events = [
        r for r in rows
        if r["record_type"] == "sysmon" and r["EventCode"] == "1"
    ]
    ports = defaultdict(set)
    for row in rows:
        if row["record_type"] == "network" and row["source_ip"] and row["destination_port"]:
            ports[row["source_ip"]].add(row["destination_port"])

    print("Synthetic dataset validation (NOT live Splunk evidence)")
    print(f"Rows loaded: {len(rows)}")
    failed_logon_matches = {k: v for k, v in failures.items() if v >= 5}
    print(f"Failed-logon groups at threshold >= 5: {failed_logon_matches}")
    print(f"Sysmon process-creation sample events: {len(process_events)}")
    port_matches = {ip: sorted(values) for ip, values in ports.items() if len(values) >= 15}
    print(f"Sources with >= 15 distinct destination ports: {port_matches}")

    assert len(rows) == 21, f"Expected 21 synthetic rows, got {len(rows)}"
    assert failed_logon_matches.get(("192.0.2.25", "labuser")) == 5
    assert len(process_events) == 1
    assert len(port_matches.get("198.51.100.10", [])) == 15
    print("RESULT: PASS — synthetic dataset structure and expected patterns validated.")
    print("LIMITATION: This does not verify log forwarding, SPL field extraction, Splunk alerts, or live dashboard behavior.")

if __name__ == "__main__":
    main()
