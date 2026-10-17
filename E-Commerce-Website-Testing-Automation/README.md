# E-Commerce Website Testing & Automation

Full-stack QA portfolio project using Spring Boot, Java, H2, HTML/CSS/JavaScript, Selenium WebDriver, TestNG, and Maven.

## Features
- Storefront UI with product search, cart, and checkout.
- REST API for health, products, and order creation/retrieval.
- H2 persistence for orders.
- Selenium + TestNG regression tests with assertions and failure screenshots.
- Test plan and evidence-capture instructions.

## Run
Requirements: JDK 17+, Maven 3.9+, Chrome.

From this directory, run `mvn spring-boot:run` and open http://localhost:8080.
In a second terminal, run `mvn test`. Selenium expects the app to be running at http://localhost:8080. Override with `-DbaseUrl=http://localhost:8080`. Use `-Dheadless=true` for headless Chrome.

API endpoints: GET /api/health, GET /api/products, POST /api/orders, GET /api/orders/{id}. H2 console: http://localhost:8080/h2-console; JDBC URL `jdbc:h2:file:./data/shopdb`, user `sa`, blank password.

## End-to-end scenarios
1. Storefront loads four sample products.
2. Search filters by product name/category.
3. Add-to-cart updates count and total; items can be removed.
4. Empty cart checkout shows validation.
5. Valid checkout creates a persisted order and confirmation.
6. API rejects invalid checkout data.

## Evidence and screenshots
Capture actual screenshots after starting the app: `evidence/screenshots/storefront.png`, `cart.png`, and `order-confirmation.png`. On Windows use Win+Shift+S. Failed Selenium tests automatically attempt to save a failure PNG. Maven/Surefire results are in `target/surefire-reports/`.

Important: no screenshots or test outcomes are represented as real until captured from an actual run. Keep actual screenshots/reports; do not substitute mockups.

## Structure
- `src/main/java/com/gorak/ecommerce/`: Spring Boot app, models, controller, repository
- `src/main/resources/static/index.html`: storefront UI
- `src/test/java/com/gorak/ecommerce/StoreE2ETest.java`: Selenium/TestNG tests
- `docs/TEST-PLAN.md`: manual/API/database test plan
- `evidence/screenshots/`: real screenshots from local runs

This is a demo store with sample products and no real payment processing. Do not enter real payment details.
