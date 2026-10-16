# API Reference

Base URL: `http://localhost:3000`

## GET /api/health
Returns application status and whether demo/database mode is active.

## POST /api/auth/login
JSON body: `{"email":"analyst@example.com","password":"..." }`
Returns a signed JWT in configured authentication mode.

## GET /api/incidents
Optional query parameters: `status`, `severity`, `q`. Returns `{items,total}`.

## POST /api/incidents
JSON body:
```json
{"title":"Suspicious login","description":"Synthetic test case","severity":"high","assignee":"SOC Analyst"}
```
Returns HTTP 201 and the created incident. Invalid title/severity returns HTTP 400.

## PATCH /api/incidents/:id
JSON body can include `status` (`open|investigating|resolved`), `severity`, or `assignee`.

Use a bearer token outside demo mode. Never place real credentials or sensitive incident data in public examples.
