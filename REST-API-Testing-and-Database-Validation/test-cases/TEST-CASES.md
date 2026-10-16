# Test Cases and Expected Results

**Environment:** JSONPlaceholder public demo API; base URL `https://jsonplaceholder.typicode.com`.

| ID | Scenario | Steps / Input | Expected result | Evidence |
|---|---|---|---|---|
| API-001 | Fetch one post | GET `/posts/1` | HTTP 200; JSON includes userId, id=1, title, body | Capture response + assertions |
| API-002 | Filter posts | GET `/posts?userId=1` | HTTP 200; JSON array; every post has userId=1 | Capture response + assertions |
| API-003 | Create post | POST `/posts` with title/body/userId | HTTP 201; response reflects submitted fields and includes id | Capture response + assertions |
| API-004 | Update post | PUT `/posts/1` with id/title/body/userId | HTTP 200; response reflects submitted fields | Capture response + assertions |
| API-005 | Delete post | DELETE `/posts/1` | HTTP 200; response is empty or JSON object | Capture response + assertions |
| API-006 | Invalid route | GET `/invalid-resource-path/1` | HTTP 404 | Capture response + assertions |
| DB-001 | Seed sample records | Execute `sql/schema.sql` | Four sample rows are inserted | Capture SQLite output |
| DB-002 | Required fields | Run null-check query | No rows returned for missing required fields | Capture query output |
| DB-003 | Duplicate IDs | Run duplicate-ID query | No duplicate IDs returned | Capture query output |
| DB-004 | Count by user | Run aggregate query | Counts match the seeded sample rows | Capture query output |

## Execution log

Fill this in only after running the tests.

| Test ID | Actual result | Pass/Fail | Date | Evidence file |
|---|---|---|---|---|
| API-001 | _Record actual result_ | _TBD_ | _TBD_ | _TBD_ |
| API-002 | _Record actual result_ | _TBD_ | _TBD_ | _TBD_ |
| API-003 | _Record actual result_ | _TBD_ | _TBD_ | _TBD_ |
| API-004 | _Record actual result_ | _TBD_ | _TBD_ | _TBD_ |
| API-005 | _Record actual result_ | _TBD_ | _TBD_ | _TBD_ |
| API-006 | _Record actual result_ | _TBD_ | _TBD_ | _TBD_ |

## Defect report template

- **Defect ID:**
- **Summary:**
- **Environment / endpoint:**
- **Preconditions:**
- **Steps to reproduce:**
- **Expected result:**
- **Actual result:**
- **Severity / priority:**
- **Evidence:**
- **Status:**
