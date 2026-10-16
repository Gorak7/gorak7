# IOC API Reference

Base URL: `http://localhost:3001`

## GET /api/health
Returns application status and mode.

## GET /api/iocs
Optional query parameters: `q`, `type`, `severity`, `status`. Returns `{items,total}`.

## POST /api/iocs
Example JSON:
```json
{"value":"203.0.113.10","type":"ip","severity":"medium","confidence":50,"source":"Lab test","notes":"Synthetic sample"}
```
Supported types: `ip`, `domain`, `url`, `hash`. Severity: `low`, `medium`, `high`, `critical`. Confidence: integer 0–100. Duplicate value/type returns HTTP 409.

## PATCH /api/iocs/:id
Supports `status`, `severity`, `confidence`, and `notes`. Status: `new`, `investigating`, `confirmed`, `false_positive`.
