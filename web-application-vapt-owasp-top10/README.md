# Web Application VAPT — OWASP Top 10

Portfolio project framework for an authorized OWASP Juice Shop lab. This initial commit contains the methodology and evidence templates; assessment findings, screenshots, and retest results must be added only after you run and verify the lab.

## Lab
- OWASP Juice Shop: https://owasp.org/www-project-juice-shop/
- Burp Suite Community: https://portswigger.net/burp/communitydownload
- OWASP ZAP: https://www.zaproxy.org/
- OWASP WSTG: https://owasp.org/www-project-web-security-testing-guide/
- CVSS: https://www.first.org/cvss/

## Safe workflow
1. Get written permission and define scope before testing.
2. Run Juice Shop only in a local/disposable lab.
3. Map routes and roles; record baseline behavior.
4. Use Burp/ZAP as supporting tools. Validate scanner alerts manually.
5. Save sanitized screenshots and request/response snippets only; never commit cookies, tokens, credentials, or personal data.
6. Map confirmed issues to an OWASP/WSTG reference, document impact and remediation, then retest.
7. Update the report with actual results only. Never present placeholders as findings.

## Repository layout
- `docs/methodology.md` — phases and testing approach
- `docs/scope-and-rules-of-engagement.md` — scope/authorization template
- `docs/evidence-handling.md` — evidence handling guidance
- `templates/report-template.md` — final report outline
- `templates/finding-template.md` — validated finding template
- `templates/test-plan.csv` — initial checklist
- `LICENSE` — MIT License

## Status
**Framework prepared; live lab assessment not yet executed.** Real screenshots and findings are not included in this initial commit.

## Resume bullet (only after completing the lab)
Assessed a deliberately vulnerable web application in an authorized lab using Burp Suite/OWASP ZAP; mapped and validated findings against OWASP WSTG, documented severity and remediation, and retested applicable fixes.
