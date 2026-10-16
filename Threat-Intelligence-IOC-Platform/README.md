# Threat Intelligence & IOC Analysis Platform

Full-stack portfolio application for storing and investigating synthetic indicators of compromise (IOCs).

## Technology
- Frontend: responsive HTML, CSS, vanilla JavaScript
- Backend: Node.js + Express REST API
- Database: PostgreSQL with indexed, parameterized queries
- Security: validation, rate limiting, Helmet, JWT demo flow
- Testing: Node test runner + Supertest
- Container: Docker Compose

## Features
- IOC dashboard and searchable/filterable table
- Add IP, domain, URL, and file-hash indicators
- Severity/confidence classification and analyst notes
- Duplicate indicator checks
- Update triage status and inspect IOC detail
- REST API, health endpoint, test cases, and API documentation
- Demo data for quick UI preview; PostgreSQL for persistence

## Start
1. Install Node.js 20+ and Docker Desktop.
2. Copy `.env.example` to `.env`; change `JWT_SECRET`.
3. Start the database: `docker compose up -d db`
4. Run `npm install` then `npm run dev`.
5. Visit http://localhost:3001.
6. Run tests using `npm test`.

The interface uses synthetic sample IOCs and does not automatically query external threat-intelligence providers. An IOC marked suspicious in this demo is not proof of malicious activity.

## Evidence checklist
Capture genuine screenshots after running the application:
- `docs/evidence/dashboard.png`
- `docs/evidence/create-ioc.png`
- `docs/evidence/search-filter.png`
- `docs/evidence/api-tests.png`
- `docs/evidence/postman-response.png`

Save test output to `docs/evidence/test-results.txt`. Do not label illustrative mockups as live test evidence.

## API
- `GET /api/health`
- `GET /api/iocs?q=&type=&severity=&status=`
- `POST /api/iocs`
- `PATCH /api/iocs/:id`

## Security note
Use only synthetic/public indicators in this portfolio demo. Configure unique secrets, database credentials, authentication, logging, and production deployment controls before public hosting.
