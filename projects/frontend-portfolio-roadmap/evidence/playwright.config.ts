import { defineConfig, devices } from "@playwright/test";
export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  reporter: [["list"], ["html", { outputFolder: "playwright-report", open: "never" }], ["json", { outputFile: "test-results/results.json" }]],
  outputDir: "test-results",
  use: { baseURL: "http://127.0.0.1:4173", trace: "retain-on-failure", screenshot: "only-on-failure", video: "retain-on-failure" },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: [
    { command: "cd ../your-ui && npm run dev -- --host 127.0.0.1 --port 4173", url: "http://127.0.0.1:4173", reuseExistingServer: !process.env.CI, timeout: 120000 },
    { command: "cd ../syncboard/client && npm run dev -- --host 127.0.0.1 --port 5173", url: "http://127.0.0.1:5173", reuseExistingServer: !process.env.CI, timeout: 120000 },
    { command: "cd ../syncboard/server && npm run dev", url: "http://127.0.0.1:3001/health", reuseExistingServer: !process.env.CI, timeout: 120000 }
  ]
});