# Evidence and Screenshot Guide

This folder is reserved for genuine screenshots and test output captured after running the application. No fake runtime evidence is included.

## Capture these screenshots
1. `01-dashboard.png` — IOC overview with sample indicators and metrics.
2. `02-add-ioc.png` — new synthetic IOC entered in the form.
3. `03-ioc-added.png` — newly created indicator visible in the table.
4. `04-search-filter.png` — filtered results by type or severity.
5. `05-duplicate-rejected.png` — duplicate IOC request returning HTTP 409.
6. `06-api-tests.png` — terminal output from the actual test run.
7. `07-postman-response.png` — successful API response with JSON body.

## Run and capture
```bash
npm install
npm test
npm run dev
```
Open `http://localhost:3001`. The included examples are synthetic/reserved indicators, not confirmed malicious IOCs. Save screenshots here and actual test output as `test-results.txt`.

For API evidence:
```bash
curl -i http://localhost:3001/api/health
curl -i http://localhost:3001/api/iocs
```

Never label mockups or expected results as evidence from an actual test run.
