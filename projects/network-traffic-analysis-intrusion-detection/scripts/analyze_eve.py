#!/usr/bin/env python3
"""Summarize Suricata EVE JSONL alerts; standard library only.

This tool reports observed alert fields and candidate IPs. It does not determine
whether an address is malicious and is not a replacement for analyst triage.
"""
import argparse
import json
from collections import Counter
from pathlib import Path


def read_events(path):
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield line_no, json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"[WARN] Skipping invalid JSON at line {line_no}: {exc}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("eve_jsonl", type=Path, help="Suricata eve.json file or JSONL fixture")
    parser.add_argument("--out", type=Path, help="Optional path for JSON summary")
    args = parser.parse_args()

    alerts, signatures, src_ips, dest_ips = [], Counter(), Counter(), Counter()
    event_counts = Counter()
    for line_no, event in read_events(args.eve_jsonl):
        event_type = event.get("event_type", "unknown")
        event_counts[event_type] += 1
        if event_type != "alert":
            continue
        alert = event.get("alert") or {}
        record = {
            "timestamp": event.get("timestamp"),
            "src_ip": event.get("src_ip"),
            "src_port": event.get("src_port"),
            "dest_ip": event.get("dest_ip"),
            "dest_port": event.get("dest_port"),
            "proto": event.get("proto"),
            "signature": alert.get("signature", "Unknown signature"),
            "signature_id": alert.get("signature_id"),
            "category": alert.get("category"),
            "severity": alert.get("severity"),
            "source_line": line_no,
        }
        alerts.append(record)
        signatures[record["signature"]] += 1
        if record["src_ip"]:
            src_ips[record["src_ip"]] += 1
        if record["dest_ip"]:
            dest_ips[record["dest_ip"]] += 1

    summary = {
        "input_file": str(args.eve_jsonl),
        "event_type_counts": dict(event_counts),
        "alert_count": len(alerts),
        "top_signatures": [{"signature": k, "count": v} for k, v in signatures.most_common()],
        "top_alert_source_ips": [{"ip": k, "count": v} for k, v in src_ips.most_common()],
        "top_alert_destination_ips": [{"ip": k, "count": v} for k, v in dest_ips.most_common()],
        "alerts": alerts,
        "analyst_note": "IPs are observed indicators only; validate context and reputation independently.",
    }
    rendered = json.dumps(summary, indent=2)
    print(rendered)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered + "\n", encoding="utf-8")
        print(f"\n[+] Wrote summary to {args.out}")


if __name__ == "__main__":
    main()
