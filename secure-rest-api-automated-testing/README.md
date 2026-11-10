# Secure REST API with Automated Testing

A PHP 8.2+ REST API backed by MySQL, with bearer-token authentication, validation, rate limiting, audit logging, PHPUnit and Postman/Newman automation.

## Features
- CRUD for startups, mentors and programmes.
- Opaque 256-bit bearer tokens; only SHA-256 token hashes are stored. Tokens expire after eight hours.
- Password hashing with PHP password_hash/password_verify.
- Consistent JSON errors: 400, 401, 404, 405, 422, 429 and 500.
- IP and authenticated-user fixed-window rate limiting.
- Audit events for create/update/delete; pagination (limit max 100).
- Postman collection, PHPUnit tests and GitHub Actions CI.

## Quick start (Docker)
1. Install Docker Desktop.
2. Copy .env.example to .env and change all demo passwords.
3. Run `docker compose up --build -d`.
4. Seed a local demo user: `docker compose exec api php database/seed.php`.
5. Health check: `curl -i http://localhost:8000/api/v1/health`.
6. Import the collection and environment from `postman/` into Postman and run sequentially.

The default seed account is a throwaway local demo only. Never use the documented demo password outside a disposable environment. Set SEED_USERNAME and SEED_PASSWORD for custom credentials.

## Local setup
Requirements: PHP 8.2+, PDO MySQL, MySQL 8+, Composer 2.
```bash
cp .env.example .env
set -a; . ./.env; set +a
mysql -u root -p < database/schema.sql
composer install
php database/seed.php
php -S 127.0.0.1:8000 -t public
```

## API reference
Base URL: `http://localhost:8000/api/v1`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Health check; no auth |
| POST | /auth/token | Issue bearer token |
| GET, POST | /startups | List/create |
| GET, PUT, PATCH, DELETE | /startups/{id} | Read/update/delete |
| GET, POST | /mentors | List/create |
| GET, PUT, PATCH, DELETE | /mentors/{id} | Read/update/delete |
| GET, POST | /programmes | List/create |
| GET, PUT, PATCH, DELETE | /programmes/{id} | Read/update/delete |

All resource endpoints require `Authorization: Bearer <token>`. Lists accept `?page=1&limit=20`.

## Tests
```bash
composer install
composer lint
composer test
npm install --global newman
newman run postman/Secure-REST-API.postman_collection.json -e postman/Secure-REST-API.local.postman_environment.json --reporters cli,junit --reporter-junit-export evidence/newman-junit.xml
```

See docs/TEST-PLAN.md and docs/TEST-REPORT.md. Evidence examples are illustrative, not claims of completed live tests. Capture real Postman, PHPUnit, SQL and CI screenshots as listed in evidence/README.md.

## Security limitations
Educational portfolio project, not production-certified. Add HTTPS, secrets management, account lockout, token revocation, role-based access, stricter per-field schemas, structured logging, backup policies and security review before production. MySQL fixed-window rate limiting is single-instance demo-grade; use Redis/API gateway when distributed.

MIT License. See LICENSE.
