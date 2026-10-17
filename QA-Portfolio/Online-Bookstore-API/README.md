# Online Bookstore — Full-Stack API Testing Project

A full-stack bookstore demo with a browser UI, Spring Boot REST API, MySQL database, Postman collection, REST Assured automation, SQL validation, and GitHub Actions CI.

> **Evidence integrity:** test scripts and evidence instructions are provided. Run the application and tests yourself before claiming passing counts or uploading screenshots/reports as real results.

## Stack
- Frontend: HTML, CSS, vanilla JavaScript
- Backend: Java 17, Spring Boot 3, Spring Data JPA, Bean Validation
- Database: MySQL 8
- API documentation/testing: OpenAPI/Swagger UI, Postman, Newman
- Automated tests: REST Assured, JUnit 5
- CI: GitHub Actions

## Features
- Browse and search books
- View individual book records
- Create, update, and delete books (CRUD)
- Place a demo order and verify stock availability
- Validate request payloads and error responses
- Query the MySQL database to compare stored records with API responses

## Start locally
1. Install Docker Desktop, JDK 17+, and Maven 3.9+.
2. Run `docker compose up -d db` from this directory.
3. Run `mvn spring-boot:run` from `backend/`.
4. Open http://localhost:8081 for the UI.
5. API base: http://localhost:8081/api; OpenAPI UI: http://localhost:8081/swagger-ui/index.html.
6. Import `postman/Online-Bookstore.postman_collection.json` into Postman.
7. Run `mvn test` in `automation/` for REST Assured checks.
8. Optional Postman CLI: `npm install -g newman`, then `newman run postman/Online-Bookstore.postman_collection.json`.

## API endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/health | Health check |
| GET | /api/books | List/search books with optional `q` |
| GET | /api/books/{id} | Fetch one book |
| POST | /api/books | Create a book |
| PUT | /api/books/{id} | Update a book |
| DELETE | /api/books/{id} | Delete a book |
| POST | /api/orders | Create a demo order |

## Test scenarios
- Positive: list books, search, fetch a book, create/update/delete, valid order.
- Negative: unknown book ID, invalid price, blank title, malformed email, non-positive quantity, insufficient stock.
- Database: compare IDs, title, price, and stock returned by API against SQL queries.
- Contract: status codes, JSON fields, content type, and error response shape.

## Evidence
Capture real screenshots/results into `evidence/`: UI catalog, book search, Postman response, Swagger page, SQL output, REST Assured report, Newman summary, and GitHub Actions run. See `evidence/README.md`. Do not claim a test count or pass rate until actually measured.

## Resume-ready description (update after running)
**REST API Testing: Online Bookstore Service** — Built a full-stack bookstore demo using Spring Boot and MySQL; created Postman requests and REST Assured tests for CRUD, validation, and order endpoints; verified persistence with SQL and configured CI execution for repeatable API regression checks.
