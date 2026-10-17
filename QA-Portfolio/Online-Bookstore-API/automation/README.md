# Bookstore test execution and evidence

Run the Spring Boot backend first, then:
```bash
mvn -B test
```
The REST Assured suite validates health, list/search, missing records, invalid payloads, and CRUD. The Selenium UI test captures homepage and search screenshots into `automation/evidence/screenshots/` when Chrome is installed and the UI is reachable.

Postman:
```bash
npm install -g newman
newman run ../postman/Online-Bookstore.postman_collection.json --reporters cli,junit --reporter-junit-export target/newman-results.xml
```
Save actual Postman UI screenshots in `../evidence/`. Never substitute fabricated output for real run evidence.
