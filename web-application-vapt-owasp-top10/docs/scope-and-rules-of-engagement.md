# Scope and Rules of Engagement

> This template is not authorization by itself. Complete it before testing.

- Assessor: Gorak Addepalli
- Owner/approver and contact: `[fill in]`
- Written approval/ticket and date: `[fill in]`
- Test window/timezone: `[fill in]`
- Stop/emergency contact: `[fill in]`
- Lab application/version/base URL: `[local Juice Shop URL]`
- Roles and synthetic test accounts: `[fill in]`
- In-scope routes/APIs: `[fill in]`

## Out of scope
Public or third-party systems without explicit written authorization; denial-of-service/stress testing; destructive actions; persistence; social engineering; real users' data; and any host not listed above.

## Rules
1. Keep the intentionally vulnerable app isolated and non-public.
2. Use only synthetic data and designated lab accounts.
3. Prefer non-destructive checks; stop if availability or data integrity is at risk.
4. Do not access or retain unrelated information.
5. Redact cookies, tokens, credentials, API keys, and personal data.
6. Record enough details for a safe reproduction.
7. Stop immediately if a test reaches an out-of-scope asset or causes unexpected impact.

Approval: `[owner/date]`  
Assessor acknowledgement: `[name/date]`
