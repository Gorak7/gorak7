"""Streaming defensive log analyzer with JSON and HTML reporting."""
from __future__ import annotations
import argparse, html, json, re
from collections import Counter, defaultdict
from pathlib import Path

ACCESS = re.compile(r'^(?P<ip>\S+) \S+ \S+ \[(?P<time>[^]]+)\] "(?P<request>[^"]*)" (?P<status>\d{3}) (?P<size>\S+)')
FAILED_SSH = re.compile(r"Failed password for (?:invalid user )?\S+ from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})")

def analyze(path: Path, burst_threshold: int = 20, ssh_threshold: int = 5) -> dict:
    total = malformed = 0; statuses = Counter(); ips = Counter(); failures = Counter(); five_x = 0; evidence = []
    for line_no, line in enumerate(path.open(encoding="utf-8", errors="replace"), 1):
        total += 1; line = line.rstrip("\n")
        match = ACCESS.match(line)
        if match:
            d = match.groupdict(); status = int(d["status"]); statuses[str(status)] += 1; ips[d["ip"]] += 1
            if status >= 500:
                five_x += 1
                if len(evidence) < 100: evidence.append({"line": line_no, "type": "http_server_error", "ip": d["ip"], "status": status, "request": d["request"]})
            continue
        ssh = FAILED_SSH.search(line)
        if ssh:
            failures[ssh.group("ip")] += 1
            if len(evidence) < 100: evidence.append({"line": line_no, "type": "ssh_auth_failure", "ip": ssh.group("ip")})
        elif not line.strip(): malformed += 1
    findings = []
    if five_x >= 3: findings.append({"severity": "high", "title": "HTTP 5xx error spike", "count": five_x, "recommendation": "Correlate with deploys and application logs; verify dependency health."})
    for ip, count in failures.items():
        if count >= ssh_threshold: findings.append({"severity": "high", "title": "Repeated SSH authentication failures", "ip": ip, "count": count, "recommendation": "Review access logs, enforce MFA/key auth, and apply rate limiting."})
    for ip, count in ips.items():
        if count >= burst_threshold: findings.append({"severity": "medium", "title": "Request burst from one IP", "ip": ip, "count": count, "recommendation": "Validate against expected traffic before applying controls."})
    return {"source": path.name, "total_lines": total, "malformed_or_blank_lines": malformed, "status_counts": dict(statuses), "top_ips": ips.most_common(10), "ssh_failures_by_ip": dict(failures), "http_5xx_count": five_x, "findings": findings, "evidence": evidence, "impact": "Potential service degradation or repeated authentication attempts; validate with surrounding telemetry.", "generated_recommendations": [f["recommendation"] for f in findings]}

def render_html(report: dict) -> str:
    findings = "".join(f"<li><b>{html.escape(f['severity'].upper())}</b> — {html.escape(f['title'])}: {f.get('count', 0)}. {html.escape(f['recommendation'])}</li>" for f in report["findings"]) or "<li>No findings crossed configured thresholds.</li>"
    return "<!doctype html><html><head><meta charset='utf-8'><title>Incident Summary</title><style>body{font:16px system-ui;max-width:900px;margin:3rem auto;padding:0 1rem}li{margin:.7rem 0}code{background:#eee;padding:.2rem}</style></head><body><h1>Log Analysis Incident Summary</h1><h2>Summary</h2><p>Source: <code>"+html.escape(report["source"])+"</code> · Lines: "+str(report["total_lines"])+" · HTTP 5xx: "+str(report["http_5xx_count"])+"</p><h2>Findings and recommendations</h2><ul>"+findings+"</ul><h2>Evidence (sample)</h2><pre>"+html.escape(json.dumps(report["evidence"], indent=2))+"</pre><h2>Impact</h2><p>"+html.escape(report["impact"])+"</p></body></html>"

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("--file", required=True, type=Path); p.add_argument("--format", choices=["json", "html"], default="json"); p.add_argument("--output", required=True, type=Path); p.add_argument("--burst-threshold", type=int, default=20); p.add_argument("--ssh-threshold", type=int, default=5); a = p.parse_args()
    report = analyze(a.file, a.burst_threshold, a.ssh_threshold); a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2) if a.format == "json" else render_html(report), encoding="utf-8")
    print(f"Analyzed {report['total_lines']} lines; {len(report['findings'])} finding(s); wrote {a.output}")
if __name__ == "__main__": main()
