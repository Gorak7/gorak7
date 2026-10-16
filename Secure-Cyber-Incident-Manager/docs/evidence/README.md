# Evidence and Screenshot Guide

This folder is intended for genuine evidence captured from a local running instance. Screenshots and test results are not pre-populated because they must come from an actual run.

## Capture these screenshots
1. `01-dashboard.png` — full dashboard showing the sample incident list and metrics.
2. `02-create-incident.png` — form filled with synthetic values before submission.
3. `03-incident-created.png` — newly created incident visible in the table.
4. `04-filtered-results.png` — filtered list after choosing severity/status.
5. `05-validation-error.png` — invalid request rejected with HTTP 400.
6. `06-api-tests.png` — terminal showing the real output from `npm test`.
7. `07-postman-api.png` — Postman response for `GET /api/incidents` or `POST /api/incidents`.

## Run and capture
```bash
npm install
npm test
npm run dev
```
Open `http://localhost:3000`. Use synthetic test records only. Save screenshots in this folder and test output as `test-results.txt`.

For API evidence, run:
```bash
curl -i http://localhost:3000/api/health
curl -i http://localhost:3000/api/incidents
```

Do not represent mockups, sample output, or unexecuted test cases as runtime evidence.
