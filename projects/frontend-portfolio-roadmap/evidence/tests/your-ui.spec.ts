import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("your-ui renders the playground and interactive controls", async ({ page }) => {
  await page.goto("http://127.0.0.1:4173");
  await expect(page.getByRole("heading", { name: "your-ui" })).toBeVisible();
  await page.getByLabel("Display name").fill("Gorak");
  await expect(page.getByText("Preview: Gorak")).toBeVisible();
  await page.getByRole("button", { name: "Open dialog" }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await page.screenshot({ path: "test-results/screenshots/your-ui-playground.png", fullPage: true });
});

test("your-ui accessibility scan has no serious or critical axe violations", async ({ page }) => {
  await page.goto("http://127.0.0.1:4173");
  const results = await new AxeBuilder({ page }).analyze();
  const serious = results.violations.filter(v => ["serious", "critical"].includes(v.impact ?? ""));
  expect(serious, JSON.stringify(serious.map(v => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.length })), null, 2)).toEqual([]);
});