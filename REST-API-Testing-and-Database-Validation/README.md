# REST API Testing and Database Validation

A portfolio project demonstrating entry-level QA skills with **Postman, REST APIs, JSON, SQL, and GitHub**.

> **Scope and honesty:** The API tests target the public [JSONPlaceholder](https://jsonplaceholder.typicode.com/) demo API. It is intended for testing and its POST/PUT/PATCH/DELETE operations are simulated; writes do not persist as a real production database would. The SQL scripts create a separate local SQLite dataset for practicing database validation. Run the collection yourself and save screenshots/results in `evidence/`; no test execution or screenshot is claimed until you produce it.

## Project objectives

- Verify GET, POST, PUT, and DELETE request behavior.
- Assert HTTP status codes, JSON response fields, data types, and required values.
- Exercise a negative route test and verify the not-found response.
- Practice SQL checks for row existence, duplicates, null values, and data consistency.
- Record reproducible test cases and evidence like a QA engineer.

## Repository structure

```text
REST-API-Testing-and-Database-Validation/
├── README.md
├── postman/
│   └── REST_API_Testing.postman_collection.json
├── sql/
│   ├── schema.sql
│   └── validation_queries.sql
├── test-cases/
│   └── TEST-CASES.md
├── docs/
│   └── TEST-PLAN.md
└── evidence/
    └── README.md
```

## Requirements

- Postman desktop or web app
- Internet access to reach JSONPlaceholder
- SQLite 3 or a database editor that supports SQLite

No API key or real user data is required.

## Run the API tests

1. Download or clone this repository.
2. Open Postman and select **Import**.
3. Import `postman/REST_API_Testing.postman_collection.json`.
4. Open the collection and confirm the `baseUrl` variable is `https://jsonplaceholder.typicode.com`.
5. Run the collection using Collection Runner. Run requests in order or individually.
6. Inspect each request's **Test Results** and response body.
7. Save screenshots of the collection, response, and passing assertions under `evidence/` if you want to publish execution proof.

### Requests included

| Request | Purpose | Expected status |
|---|---|---:|
| GET /posts/1 | Validate a single post and JSON fields | 200 |
| GET /posts?userId=1 | Validate a filtered collection | 200 |
| POST /posts | Validate create-request response | 201 |
| PUT /posts/1 | Validate update-request response | 200 |
| DELETE /posts/1 | Validate delete-request response | 200 |
| GET /invalid-resource-path/1 | Negative route / not-found check | 404 |

JSONPlaceholder is a fake online REST API, so the CRUD response demonstrates the API contract and does not prove persistent create/update/delete behavior.

## Run the SQL validation

Using SQLite:

1. Open a terminal in this project folder.
2. Create and seed the sample database:

   ```bash
   sqlite3 qa_api_demo.db < sql/schema.sql
   ```

3. Run the validation queries:

   ```bash
   sqlite3 -header -column qa_api_demo.db < sql/validation_queries.sql
   ```

The SQL data is a **local practice dataset** and is not automatically synchronized with JSONPlaceholder. The queries demonstrate the kind of database checks a tester would perform when connected to an application's test database.

## What to document as evidence

- Postman Collection Runner summary and per-request test results.
- A response body and status code for one successful GET and one POST.
- SQL output showing the seeded rows and validation queries.
- Any actual failures, with request, environment, timestamp, expected result, actual result, and reproduction steps.

Do not mark tests as passed unless you ran them. Do not include API keys, passwords, tokens, private URLs, or real personal data in screenshots.

## Skills demonstrated

Manual API testing, CRUD workflows, positive/negative testing, status-code validation, JSON assertions, SQL data checks, defect documentation, and test evidence management.

## Resume-ready description

**REST API Testing and Database Validation | Postman, SQL, JSON**
- Designed and organized Postman tests for GET, POST, PUT, and DELETE API workflows, validating response codes and JSON fields.
- Covered positive and negative scenarios and documented expected outcomes and reproducible defect details.
- Wrote SQLite queries to verify records, detect duplicate identifiers and null fields, and check data consistency in a local sample dataset.

Use these bullets once you have run the collection and SQL scripts and can explain the results in an interview.
