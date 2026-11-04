# Web + Mobile + API Test Automation Framework

Python/pytest framework for a smart-fan mock REST API, SauceDemo web UI and Android ApiDemos sample app.

## Layers
- API: FastAPI mock device service with demo token auth, device CRUD, power toggle and speed boundary validation.
- Web: Playwright Page Object Model tests against SauceDemo: login, lockout, inventory, sorting, cart and checkout.
- Mobile: Appium 2 + UiAutomator2 sample-app smoke/navigation checks (local Android emulator required).
- Selenium: separate browser smoke test.
- Reporting: Allure results; GitHub Actions runs API and browser suites and uploads their result artifacts.

## Setup and run
```bash
pip install -r requirements.txt
uvicorn mock_backend.app:app --reload
```
API tests: `pytest -m api --alluredir=allure-results -q`
Browser tests: `playwright install chromium && pytest -m web --alluredir=allure-results -q`
Android: install Android Studio, create an emulator, install Appium 2 and UiAutomator2 driver, install the ApiDemos APK, start Appium, set `RUN_APPIUM=1`, then run `pytest -m mobile -q`.
Selenium: install Chrome/ChromeDriver, set `RUN_SELENIUM=1`, then run `pytest -m web -q`.
Allure report: `allure serve allure-results`.
Docker: `docker compose up --build mock-api`.

## Test inventory
The suite defines approximately 89 scenarios: 46 API cases, 32 Playwright cases, 10 Appium Android cases and 1 Selenium smoke case. API and Playwright are configured in GitHub Actions. Appium and Selenium are opt-in because they require local emulator/browser setup. These are authored scenarios, not a claim that all 89 have passed in CI.

## Evidence integrity
Do not count skipped tests as passed. Capture actual Allure reports, screenshots, browser traces, emulator evidence and CI links after running. The mock service stores data in memory and uses demo credentials; it is a local test target, not a production IoT control plane.
