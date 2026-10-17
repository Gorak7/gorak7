# Online Bookstore — Full-Stack API Testing Project

A full-stack bookstore demo with browser UI, Spring Boot REST API, MySQL, Postman/Newman, REST Assured/JUnit 5, SQL validation, and GitHub Actions.

> **Evidence integrity:** test scripts and evidence automation are provided. Do not report tests as passed or screenshots as generated until a real run produces them.

## Quick start — easiest option (Docker Desktop)
1. Install and start Docker Desktop.
2. Open a terminal in `QA-Portfolio/Online-Bookstore-API`.
3. Run:
   ```bash
   docker compose up --build -d
   docker compose ps
   docker compose logs -f app
   ```
4. Wait for Spring Boot to finish starting. Open **http://localhost:8081**.
5. Health check: **http://localhost:8081/api/health**. Expected JSON contains `"status":"UP"`.
6. Swagger UI: **http://localhost:8081/swagger-ui/index.html**.
7. Stop with `docker compose down`. To delete the local demo database and start fresh, use `docker compose down -v`.

Compose waits for MySQL health before starting Spring Boot. Inside Docker, the app connects to `db:3306`; the host mapping `localhost:3308` is for database tools on your computer only.

## Run backend directly on your computer
Requirements: Docker Desktop, JDK 17+, Maven 3.9+.
1. Run `docker compose up -d db` from this project folder.
2. Wait until `docker compose ps` shows the database is healthy.
3. In another terminal, run `cd backend`, then `mvn -B clean spring-boot:run`.
4. Open http://localhost:8081.
5. API base: http://localhost:8081/api; Swagger: http://localhost:8081/swagger-ui/index.html.

## Tests
- REST Assured + JUnit 5: from `automation/`, run `mvn -B test` while the backend and database are running.
- Postman: import `postman/Online-Bookstore.postman_collection.json`; set the base URL to `http://localhost:8081`.
- Newman: from the project root, run `npx --yes newman run postman/Online-Bookstore.postman_collection.json`.
- CI: the GitHub Actions workflow runs backend build, REST Assured/UI checks, Newman, and uploads any generated reports/screenshots as artifacts.

## API endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/books?q=Clean` | List/search books |
| GET | `/api/books/{id}` | Fetch one book |
| POST | `/api/books` | Create a book |
| PUT | `/api/books/{id}` | Update a book |
| DELETE | `/api/books/{id}` | Delete a book |
| POST | `/api/orders` | Create a simulated demo order |

## Troubleshooting
- **Connection refused:** inspect `docker compose ps` and `docker compose logs --tail=200 app`; do not open the UI until the app has started.
- **Database error:** inspect `docker compose logs --tail=200 db`. Default host DB port is 3308; if that port is occupied, change the host-side mapping. Keep the app's internal JDBC hostname `db` and port 3306 unchanged.
- **404/blank UI:** confirm `backend/src/main/resources/static/index.html` exists and rebuild with `docker compose up --build -d`; hard-refresh the browser.
- **Maven/Java error:** run `java -version` and `mvn -version`; use Java 17+. Run app commands in `backend/` and tests in `automation/`.
- **Old database data:** named volumes preserve records across restarts. To recreate the database from the checked-in schema, run `docker compose down -v` and then `docker compose up --build -d`. This deletes local demo data.

## Evidence
Real screenshots, SQL output, REST Assured reports, Newman results, and CI logs should be downloaded from an actual successful workflow run or generated locally. Do not claim test counts or pass rates until measured.
