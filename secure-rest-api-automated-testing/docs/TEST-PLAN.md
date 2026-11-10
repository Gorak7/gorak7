# Test Plan
Validate authentication, CRUD for startups/mentors/programmes, validation, pagination, errors, rate limiting and audit events.

| ID | Scenario | Expected result |
|---|---|---|
| AUTH-01 | Valid credentials request token | 201 bearer token |
| AUTH-02 | Invalid password | 401 INVALID_CREDENTIALS |
| AUTH-03 | Protected endpoint without token | 401 UNAUTHORIZED |
| AUTH-04 | Malformed or expired token | 401 |
| CRUD-01 | Create valid startup | 201 and Location |
| CRUD-02 | List startups | 200 with pagination metadata |
| CRUD-03 | Read existing startup | 200 |
| CRUD-04 | PATCH resource | 200 and persisted update |
| CRUD-05 | Delete resource | 200 |
| CRUD-06 | Read deleted resource | 404 RESOURCE_NOT_FOUND |
| MENT-01 | Create mentor with valid email | 201 |
| MENT-02 | Invalid mentor email | 422 |
| PROG-01 | Create programme with supported status | 201 |
| PROG-02 | Unsupported programme status | 422 |
| VAL-01 | Malformed JSON | 400 INVALID_JSON |
| VAL-02 | Empty required field | 422 VALIDATION_ERROR |
| VAL-03 | Unsafe URL scheme | 422 |
| PAGE-01 | Page 1 and limit 10 | 200 with requested metadata |
| PAGE-02 | Limit 101 or page 0 | 422 |
| RATE-01 | Exceed configured request limit | 429 and Retry-After |
| AUD-01 | Create/update/delete resource | Audit row written |

## Exit criteria
All PHPUnit and Postman assertions pass; no unexpected 5xx; audit events verified; Newman JUnit report and redacted screenshots saved under evidence.