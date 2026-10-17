# REST API Testing and Database Validation — Full-Stack QA Project

A runnable QA portfolio project with a browser UI, Spring Boot REST API, PostgreSQL, Postman assertions, SQL validation scripts, and evidence templates.

## Stack
- Front end: HTML, CSS, vanilla JavaScript
- Backend: Java 17, Spring Boot 3, Spring Data JPA, Bean Validation
- Database: PostgreSQL
- Testing: Postman collection, SQL queries, manual test register
- Runtime: Docker Compose

## Features
- CRUD endpoints: GET, POST, PUT, PATCH, DELETE.
- Browser UI to create, list, edit, and delete records.
- Required-field, email-format, duplicate-email and missing/invalid API-key scenarios.
- Postman tests for response codes, payloads, and response times.
- SQL checks for persistence, required fields, and duplicate emails.

## Run locally
Prerequisite: Docker Desktop with Docker Compose.
1. Open a terminal in this folder.
2. Run: docker compose up --build
3. Open http://localhost:8080 for the front end.
4. API base URL: http://localhost:8080/api/users
5. Demo API key: qa-demo-key, sent in the X-API-Key header.
6. Stop with: docker compose down. To erase local database data too, use docker compose down -v.

## Run Postman tests
Import postman/REST-API-Testing.postman_collection.json. Run requests in order against http://localhost:8080. The create request saves a user ID for later tests. Export the Postman run report and store it under evidence/reports/. Capture screenshots under evidence/screenshots/.

## Repository contents
- test-cases/test-cases.csv — manual test register.
- sql/validation-queries.sql — database validation.
- bug-reports/BUG-REPORT-TEMPLATE.md — defect documentation.
- evidence/README.md — screenshot and report checklist.
- LICENSE — MIT licence.

## API summary
Every /api/users endpoint requires X-API-Key: qa-demo-key.
- GET /api/users — list users
- GET /api/users/{id} — get one user
- POST /api/users — create user
- PUT /api/users/{id} — replace editable fields
- PATCH /api/users/{id} — partially update fields
- DELETE /api/users/{id} — delete user

## Security note
This is a local learning project. The hard-coded demo API key is not production authentication. Do not expose this service publicly or use real personal data. Production systems should use externalized secrets, proper identity management, HTTPS, rate limiting, and audit logging.
