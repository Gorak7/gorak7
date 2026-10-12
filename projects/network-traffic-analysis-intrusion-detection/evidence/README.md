# Evidence directory

Place **your own** outputs here after running the lab:
- `pcap/`: packet captures (review for sensitive data before committing)
- `screenshots/`: genuine screenshots captured from Wireshark, Suricata, and the Python summary
- `suricata/`: relevant alert excerpts or sanitized EVE JSON
- `reports/`: completed analyst workbook/report and generated summary

Do not add fabricated screenshots or present the synthetic fixture under `../data/` as a real capture. For a public portfolio, use a small sanitized PCAP and redact personal or sensitive details. Evidence hashes can be generated with `bash ../scripts/hash_evidence.sh .` from this directory's parent project directory, or pass the evidence path from the project root.
