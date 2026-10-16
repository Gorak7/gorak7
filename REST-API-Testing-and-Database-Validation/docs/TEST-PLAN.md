# Test Plan

## 1. Purpose
Validate representative REST API behaviors and practice relational-data checks as an entry-level QA exercise.

## 2. Scope
- HTTP GET, POST, PUT, DELETE request workflows.
- Status-code and JSON body assertions in Postman.
- One invalid-route negative test.
- Local SQLite schema, seed data, and SQL validation queries.

## 3. Out of scope
- Production systems, real user information, load/performance testing, security penetration testing, and persistent CRUD behavior on JSONPlaceholder.
- Live synchronization between the demo API and SQLite.

## 4. Test approach
1. Import and run the Postman collection.
2. Review each response, assertion result, and actual status code.
3. Create a local SQLite database from `sql/schema.sql`.
4. Execute `sql/validation_queries.sql` and compare results to expected conditions.
5. Record execution date, result, and evidence; log defects with repeatable steps.

## 5. Entry and exit criteria
**Entry:** Postman available, internet connectivity available for API tests, SQLite available for SQL tests.

**Exit:** All planned cases have an actual result recorded; failures have evidence and reproducible steps; no test is marked passed without execution.

## 6. Risks and limitations
JSONPlaceholder is a demo API. POST/PUT/DELETE responses are simulated and are not persisted as production records. Public service behavior and availability can change. SQL validation uses a local sample database and cannot verify the API's backend database.

## 7. Deliverables
- Postman collection with test assertions.
- SQL schema, sample data, and validation queries.
- Test cases and execution log.
- Screenshots or exported reports added by the tester after running the tests.
