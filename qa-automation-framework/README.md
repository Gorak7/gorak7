# Web + Mobile + API Test Automation Framework

Python/pytest test framework for a smart-fan mock REST API, SauceDemo web UI and Android ApiDemos sample app.

## Layers
- API: FastAPI mock device service; auth, device CRUD, power and speed boundaries.
- Web: Playwright with Page Object Model against SauceDemo.
- Mobile: Appium 2 + UiAutomator2 sample tests (local emulator required).
- Selenium: separate browser smoke test.
- Reporting: Allure plugin; CI workflows upload test outputs where configured.

## Install and run
`pip install -r requirements.txt`
`uvicorn mock_backend.app:app --reload`
In another terminal: `pytest -m 'not web and not mobile' -q`
For browser tests: `playwright install chromium && pytest -m web -q`
For mobile: install Android Studio, create an emulator, install Appium 2 and UiAutomator2 driver, install ApiDemos APK, start Appium, set `RUN_APPIUM=1`, then `pytest -m mobile -q`.
For Allure: `pytest --alluredir=allure-results` then `allure serve allure-results`.

## Test inventory

The current suite defines approximately 89 test scenarios: 46 API cases, 32 Playwright web cases, 10 Appium Android smoke cases and 1 Selenium smoke case. The API and Playwright suites are configured in GitHub Actions. Appium and Selenium tests are opt-in because they require a local Android emulator/Appium server or ChromeDriver. These are authored test scenarios, not a claim that all 89 have passed in CI.

Run API tests with `pytest -m api -q`; run browser tests with `playwright install chromium && pytest -m web -q`; run Android tests after setup with `RUN_APPIUM=1 pytest -m mobile -q`; run Selenium with `RUN_SELENIUM=1 pytest -m web -q`.

## Evidence integrity
The API tests are self-contained. Web tests target the public SauceDemo demo site. Appium/Selenium are opt-in because they require local browser/emulator setup. Do not count skipped tests as passed. Record actual environment versions and attach real reports/screenshots.

## Next expansion
Add additional API schema and response-time cases, 30+ web tests, 10–15 Appium scenarios, Restful-Booker lifecycle checks and Newman execution to meet the full roadmap's 80+ test target.
