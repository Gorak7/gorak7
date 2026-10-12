# Network Traffic Analysis & Intrusion Detection Lab

A reproducible blue-team lab for examining packet captures, detecting suspicious DNS/HTTP activity, and validating IDS alerts with **Wireshark, Suricata, Snort, Python, and Bash**.

> **Evidence integrity:** This repository contains configuration, scripts, and clearly labelled sample data. It does not claim that a live capture or IDS alert happened on another person's machine. Capture your own traffic in the isolated lab and add your own screenshots/results under `evidence/` before presenting them as execution evidence.

## Objectives
- Capture and inspect traffic from a lab interface with Wireshark/tcpdump.
- Identify DNS lookups, HTTP requests, repeated connection attempts, and unusual destinations.
- Run Suricata against a PCAP or live lab interface and review EVE JSON alerts.
- Use a small Python parser to extract alert metadata and candidate indicators.
- Document findings, limitations, and remediation as an analyst report.

## Architecture

```text
Lab client / generated test traffic
              |
       isolated lab network
              |
     tcpdump / Wireshark
              |
        PCAP evidence
              |
      Suricata IDS engine
              |
      eve.json (alerts + flows)
              |
    Python IOC / alert summarizer
              |
    report + screenshots + hashes
```

## Safety boundaries
Run tests only on systems and networks you own or are explicitly authorized to assess. Keep the lab isolated (host-only/internal virtual network recommended). The included test traffic is benign; do not scan public IPs. Do not capture other people's traffic or store credentials/personal data. HTTP is plaintext by design; prefer test values that are not real secrets.

## Prerequisites
- Linux VM (Ubuntu/Debian recommended) or a dedicated lab machine
- Wireshark and/or tcpdump
- Suricata 7.x (Snort 3 can be used instead, but the supplied rules use Suricata syntax)
- Python 3.10+
- Optional: jq, sha256sum, Git

## Quick start (Ubuntu)
```bash
sudo apt update
sudo apt install -y wireshark tcpdump python3 python3-venv curl jq
sudo apt install -y suricata
suricata --build-info | head
python3 --version
```

Check interface names with `ip -br link`. Set `IFACE` to the lab interface, not blindly to a public-facing interface.

### 1. Capture a short PCAP
```bash
mkdir -p evidence/pcap evidence/screenshots evidence/reports
sudo tcpdump -i "${IFACE:-lo}" -nn -s 0 -w evidence/pcap/lab-capture.pcap
```
Stop with Ctrl+C after generating only your own lab traffic. For a simple local HTTP test, in one terminal run `python3 -m http.server 8080 --bind 127.0.0.1`; in another run `curl -v http://127.0.0.1:8080/`. Loopback capture support varies by OS; if no packets appear, use a host-only VM interface and verify with `tcpdump -D`.

### 2. Inspect in Wireshark
Open `evidence/pcap/lab-capture.pcap`. Useful display filters:
- `dns` — DNS queries and responses
- `http` — HTTP protocol packets (only if unencrypted HTTP is present)
- `tcp.flags.syn == 1 && tcp.flags.ack == 0` — initial TCP SYN packets
- `ip.addr == 127.0.0.1` — lab loopback traffic (if supported)
- `tcp.analysis.retransmission` — possible retransmissions

Save screenshots of the packet list and a selected packet's details. Redact any personal data.

### 3. Validate Suricata rules against a PCAP
Review `rules/local.rules` and ensure your Suricata config loads that file under `rule-files`. Then:
```bash
mkdir -p evidence/suricata
sudo suricata -r evidence/pcap/lab-capture.pcap \
  -S rules/local.rules -l evidence/suricata

tail -n 20 evidence/suricata/fast.log 2>/dev/null || true

tail -n 20 evidence/suricata/eve.json 2>/dev/null || true
```
Suricata may use different default paths/options by package. Confirm with `suricata -h` and your installed configuration. Rules fire only when their conditions match the captured packets.

### 4. Parse EVE JSON alerts
```bash
python3 scripts/analyze_eve.py evidence/suricata/eve.json --out evidence/reports/alert-summary.json
``
The parser ignores non-alert events for IOC summaries and does not label an IP malicious solely because it appears in a log.

### 5. Generate your own harmless test traffic
Use a lab interface and an address you control. For example, start a local web server and issue several requests to it. To test DNS, query a domain you are authorized to resolve:
```bash
dig example.com
curl -I https://example.com
``
Note: encrypted HTTPS content is not readable as HTTP payload in a normal packet capture. Avoid aggressive scanning; if testing a scan signature, use only a deliberately vulnerable/local target inside an isolated lab and document the exact scope.

## Repository layout
- `rules/local.rules` — small Suricata rules for SYN bursts and HTTP requests to a reserved test path.
- `scripts/analyze_eve.py` — standard-library JSONL parser for Suricata EVE.
- `scripts/hash_evidence.sh` — creates SHA-256 hashes for evidence files.
- `data/sample-eve.jsonl` — synthetic fixture for checking parser behavior; **not a real alert export**.
- `docs/analysis-workbook.md` — analyst workflow and reporting template.
- `evidence/` — place your own PCAPs, output, screenshots and report here; do not commit sensitive traffic.

## Test the parser using the labelled fixture
```bash
python3 scripts/analyze_eve.py data/sample-eve.jsonl --out /tmp/sample-summary.json
cat /tmp/sample-summary.json
```
This validates parsing only; it is not proof that the IDS detected live traffic.

## Evidence checklist
- [ ] Wireshark packet-list screenshot with visible timestamp/protocol/source/destination
- [ ] Screenshot of DNS query/response details (if present in your capture)
- [ ] Suricata startup/PCAP analysis terminal output
- [ ] Screenshot or excerpt of a matching alert with signature, timestamp, and test source/destination
- [ ] JSON summary generated by the Python parser
- [ ] SHA-256 manifest for evidence files
- [ ] Short report explaining test setup, observed facts, interpretation, false positives, and remediation

Suggested screenshot names:
`01-wireshark-overview.png`, `02-dns-details.png`, `03-suricata-alert.png`, `04-python-summary.png`.

## Limitations and honest reporting
- Detection depends on interface visibility, capture quality, rule loading, and protocol encryption.
- A signature alert is an investigative lead, not a definitive verdict.
- Private/reserved addresses and synthetic fixture entries are not real-world threat intelligence.
- Include exact commands, tool versions, capture timestamps, and hashes to make results reproducible.

## Resume-ready wording (use only after completing the lab)
Built a network traffic analysis and IDS lab using Wireshark and Suricata to inspect DNS/HTTP traffic, validate local detection rules against PCAPs, and summarize EVE JSON alerts with Python; documented findings with reproducible commands and evidence hashes.

## License
MIT — see [LICENSE](LICENSE).
