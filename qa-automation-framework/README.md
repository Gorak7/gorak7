# Web + Mobile + API Test Automation Framework

Python/pytest automation project for a smart-fan mock REST API, SauceDemo browser UI and Android ApiDemos sample application.

## Test layers
- API: FastAPI mock device service with bearer-token checks, device CRUD, power control and speed boundaries.
- Web: Playwright Page Object Model regression against SauceDemo: login, lockout, inventory, sorting, cart, product details and checkout.
- Mobile: Appium 2 + UiAutomator2 tests against the Appium team's ApiDemos sample app.
- Reporting: Allure result files uploaded by the root repository GitHub Actions workflow.

## Local setup
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

API tests:
```bash
pytest -m api --alluredir=allure-results/api -q
```

Browser tests:
```bash
playwright install chromium
pytest -m web --ignore=tests/web/test_selenium_smoke.py --alluredir=allure-results/web -q
```

Android tests require Android Studio/emulator, Appium 2, UiAutomator2 driver and the ApiDemos APK installed on the emulator:
```bash
npm install --global appium@2
appium driver install uiautomator2
appium
# In another terminal, with the ApiDemos app installed:
RUN_APPIUM=1 APPIUM_URL=http://127.0.0.1:4723 pytest -m mobile --alluredir=allure-results/mobile -q
```

Docker API: `docker compose up --build mock-api`.
Allure report: `allure serve allure-results`.

## GitHub Actions
The root workflow `.github/workflows/ai-quality-engineer.yml` runs API and Playwright suites on Ubuntu and runs the Appium suite inside an Android emulator. It uploads separate Allure artifacts. The Selenium smoke test remains opt-in for a local Chrome/ChromeDriver setup.

The suite currently defines 46 API, 32 Playwright, 10 Android and 1 Selenium scenarios. These are authored test cases; use the latest Actions run and its artifacts for the actual pass/fail totals. Never count skipped tests as passed.

## Scope and limitations
The mock API stores data in memory and uses demo credentials; it is a local test target, not a production IoT control plane. SauceDemo is an external demo site and browser tests require network access. Android CI downloads the public ApiDemos sample APK from the Appium project.
