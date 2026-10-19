# Assessment Methodology

## Standards
Record the exact edition of OWASP Top 10, OWASP WSTG, and CVSS used. Align tests based on the version/current reference applicable when the lab is run.

## Phases
1. **Plan:** obtain approval; define hosts, routes, roles, window, exclusions, stop conditions, and evidence retention.
2. **Map:** browse each approved role and document routes, forms, inputs, APIs, and expected behavior.
3. **Test:** use Burp Suite or OWASP ZAP to inspect traffic and support manual review. Automated alerts are leads, not confirmed findings.
4. **Validate:** safely reproduce the condition in the lab using synthetic data. Record expected and observed outcomes, role, and minimal evidence.
5. **Rate:** document severity, CVSS version/vector when appropriate, impact, exploitability, and assumptions.
6. **Report:** use finding template; redact secrets and unrelated data.
7. **Remediate/retest:** rerun the same test after a fix and mark Pass, Fail, or Blocked with date/build and evidence.
8. **Close:** verify every claim is evidence-backed and clean up raw captures.

## Test areas
Access control; authentication/session management; input handling/injection; cryptography/data protection; security configuration; component/dependency exposure; server-side request and file processing; integrity/business logic; security logging; and API authorization. Not every area applies to every application.
