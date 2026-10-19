# Evidence Handling

- Capture the minimum evidence necessary to demonstrate a validated finding.
- Use synthetic lab data and test accounts only.
- Redact cookies, bearer tokens, API keys, passwords, personal information, and unrelated data.
- Keep raw Burp/ZAP sessions and HAR files local and excluded from Git.
- Commit only sanitized screenshots or concise request/response excerpts when useful.
- Use IDs such as `VAPT-001-E1`; note the date/time, route, role, tool/version, and finding.
- Delete temporary raw captures according to the lab/owner's retention rules.
- Never put secrets or real user data in a public repository.
