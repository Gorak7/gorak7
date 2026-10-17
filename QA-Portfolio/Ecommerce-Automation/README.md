# E-Commerce Web Application — Selenium Automation Framework

A full-stack QA portfolio project: a browser-based shopping UI, Java Spring Boot REST API, MySQL persistence, and a Selenium/TestNG automation framework.

> **Evidence integrity:** this repository contains runnable test assets and an evidence checklist. Add screenshots and report files from your own local executions; no execution counts, defects, or screenshots are represented as real until you generate them.

## Architecture
- **Frontend:** HTML, CSS, vanilla JavaScript (served by Spring Boot static resources)
- **Backend:** Java 17+, Spring Boot 3, Spring Web, Spring Data JPA
- **Database:** MySQL 8
- **UI automation:** Selenium 4, Java, TestNG, Maven
- **Reporting/CI:** Surefire HTML/XML output; Jenkins pipeline example
- **Coverage:** health, product listing/search, cart, order creation, API error handling, browser workflows

## Repository layout
```
Ecommerce-Automation/
├── frontend/                 # UI source (copy into backend src/main/resources/static)
├── backend/                  # Spring Boot application
├── automation/               # Selenium + TestNG suite
├── database/schema.sql
├── evidence/                 # Store real screenshots/reports here
├── Jenkinsfile
└── docker-compose.yml
```

## Run the app
Prerequisites: JDK 17+, Maven 3.9+, Docker Desktop. From this folder:
1. Start MySQL: `docker compose up -d db`
2. In `backend`, configure `SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME`, and `SPRING_DATASOURCE_PASSWORD` or use the local defaults in `application.properties`.
3. Run `mvn spring-boot:run`.
4. Open http://localhost:8080. API health: http://localhost:8080/api/health; products: http://localhost:8080/api/products.
5. Start the Selenium suite from `automation`: `mvn test`. Set `BASE_URL` to change the application URL.

## Test strategy
- UI: home page, product rendering/search, add-to-cart, quantity and total, checkout validation, order confirmation.
- API: product listing, search, invalid requests, order payload validation.
- Cross-browser: configure Selenium browser locally for Chrome, Firefox, and Edge; install matching browsers/drivers.
- Regression: Maven Surefire output can be archived by Jenkins.
- Defect reporting: record reproducible steps, expected/actual result, environment, severity, priority, and evidence link.

## Evidence checklist
Capture your own images and save them in `evidence/`:
- `01-homepage.png` — app running in browser
- `02-product-search.png` — search results
- `03-cart.png` — cart with item and total
- `04-checkout-validation.png` — validation message
- `05-test-report.png` — actual TestNG/Surefire report
- `06-failed-test-screenshot.png` — only if a test genuinely fails
- `07-jenkins-build.png` — actual Jenkins run, if configured

Do not claim a specific test count, defect count, pass rate, or time saving until measured. See `evidence/README.md`.

## Resume-ready description (update after running)
**E-Commerce Web Application: Selenium Automation Framework** — Built a browser-based shopping application backed by Spring Boot and MySQL; developed reusable Selenium Page Object Model tests with TestNG and Maven for product search, cart, checkout, and validation flows; configured CI execution and retained actual test reports/screenshots as evidence.
