# API Examples

Examples use illustrative IDs; actual IDs are database-generated.

## Health
GET /api/v1/health — expected 200:
```json
{"status":"ok","service":"secure-rest-api","version":"1.0.0"}
```

## Token
POST /api/v1/auth/token:
```json
{"username":"demo-admin","password":"YOUR_LOCAL_SEED_PASSWORD"}
```
Expected 201 with data.access_token, token_type Bearer and expires_in 28800. Only a SHA-256 token hash is stored.

## Create startup
POST /api/v1/startups:
```json
{"name":"Northstar Labs","website":"https://example.com","industry":"Technology","contact_email":"hello@example.com"}
```
Expected 201 with generated ID and Location header.

## Validation error
Expected 422:
```json
{"error":{"code":"VALIDATION_ERROR","message":"The supplied data is invalid.","fields":{"name":"This field cannot be empty."}}}
```

## Missing record
GET /api/v1/startups/999999 — expected 404:
```json
{"error":{"code":"RESOURCE_NOT_FOUND","message":"Record not found."}}
```