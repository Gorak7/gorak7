# Screenshots, tests, accessibility and performance evidence

This folder contains reproducible evidence tooling. Results must come from a real run; this file does not claim tests or audits have passed.

## Generate evidence locally
1. Install Node.js 20+.
2. From `evidence/`, run `npm install`.
3. Install the browser: `npx playwright install --with-deps chromium`.
4. Start the your-ui and SyncBoard client/server processes as documented in their READMEs.
5. Run `npm run test:e2e` from this folder.

Playwright tests create screenshots, HTML reports, JSON results, traces and videos under `evidence/test-results/` and `evidence/playwright-report/`. Keep generated artifacts out of Git unless intentionally publishing a reviewed report.

## Accessibility audit
The Playwright suite runs axe-core on both pages and fails on serious/critical violations. This automated scan is not a full WCAG conformance audit. Also perform keyboard-only checks, focus order/return checks, zoom/reflow checks, reduced-motion checks, and screen-reader review. Record browser, OS, date, tested routes, violations, fixes and retest results in the release report.

## Performance metrics
Run Lighthouse CI against a production build for more representative results. Keep the generated JSON/HTML reports and record Performance, Accessibility, Best Practices, SEO, LCP, CLS, INP/TBT, transfer size and environment. Compare repeated runs and do not copy sample values into the README. The initial configuration uses warning thresholds while the projects are still being developed.

## CI artifacts
The GitHub Actions workflow installs dependencies, builds the projects, runs browser tests and uploads test reports/screenshots. Lighthouse is a separate step and must target both already-running applications in the workflow. A green workflow means only the checks that actually ran passed; it is not proof of complete WCAG compliance or production readiness.
