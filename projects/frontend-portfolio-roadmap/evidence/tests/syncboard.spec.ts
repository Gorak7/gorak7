import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("SyncBoard supports adding and moving a task", async ({ page }) => {
  await page.goto("http://127.0.0.1:5173");
  await expect(page.getByRole("heading", { name: "SyncBoard" })).toBeVisible();
  await page.getByLabel("Add a task").fill("Accessibility review");
  await page.getByRole("button", { name: "+ Add task" }).click();
  const task = page.locator(".task").filter({ hasText: "Accessibility review" });
  await expect(task).toBeVisible();
  await task.getByLabel("Move task").selectOption("doing");
  await expect(page.locator(".column").filter({ has: page.getByRole("heading", { name: "In progress" }) }).getByText("Accessibility review")).toBeVisible();
  await page.screenshot({ path: "test-results/screenshots/syncboard-board.png", fullPage: true });
});

test("SyncBoard accessibility scan has no serious or critical axe violations", async ({ page }) => {
  await page.goto("http://127.0.0.1:5173");
  const results = await new AxeBuilder({ page }).analyze();
  const serious = results.violations.filter(v => ["serious", "critical"].includes(v.impact ?? ""));
  expect(serious, JSON.stringify(serious.map(v => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.length })), null, 2)).toEqual([]);
});