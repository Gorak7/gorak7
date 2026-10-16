# Secure Cyber Incident Manager

A full-stack incident-management application for a security operations workflow.

## Stack
- Frontend: responsive HTML, CSS, vanilla JavaScript
- Backend: Node.js, Express, REST API
- Database: PostgreSQL
- Security: bcrypt password hashing, JWT authentication, role-based access control, Helmet, rate limiting, input validation
- Testing: Node test runner + Supertest

## Features
- Dashboard metrics and incident table
- Create, view, filter, assign, and update incidents
- JWT-based login and analyst/admin roles
- Parameterized SQL queries and database constraints
- API health endpoint, centralized errors, request validation
- Docker Compose for PostgreSQL and app
- Automated API tests

## Run locally
1. Install Node.js 20+ and Docker Desktop.
2. Copy `.env.example` to `.env` and set a unique `JWT_SECRET`.
3. Start PostgreSQL: `docker compose up -d db`
4. Install and run: `npm install && npm run dev`
5. Open http://localhost:3000
6. Run tests: `npm test`

The app can start in demo mode without a database for UI exploration, but persistent storage requires PostgreSQL. Never use demo credentials or sample secrets in production.

## Evidence
- API test output: run `npm test`; save terminal output to `docs/evidence/api-tests.txt`.
- UI screenshots: capture the dashboard, create-incident form, filtered incident list, and validation error in `docs/evidence/`.
- API examples: `docs/API.md`.

## API
- `GET /api/health`
- `POST /api/auth/login`
- `GET /api/incidents`
- `POST /api/incidents`
- `PATCH /api/incidents/:id`

## Safety
This is a portfolio/demo application. Use synthetic incident data only. Review authentication, secrets management, logging, and deployment settings before exposing it publicly.
