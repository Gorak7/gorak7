import { test, expect } from "@playwright/test";

test("SyncBoard API persists cards and makes mutation IDs idempotent", async ({ request }) => {
  const mutationId = `e2e-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  const cardId = `card-${mutationId}`;
  const payload = { id: cardId, title: "Persisted from E2E", column: "todo", baseVersion: 0 };
  const created = await request.post("http://127.0.0.1:3001/api/mutations", {
    data: { id: mutationId, type: "card.upsert", payload, baseVersion: 0, clientTimestamp: Date.now() }
  });
  expect(created.ok()).toBeTruthy();
  const firstAck = await created.json();
  const duplicate = await request.post("http://127.0.0.1:3001/api/mutations", {
    data: { id: mutationId, type: "card.upsert", payload, baseVersion: 0, clientTimestamp: Date.now() }
  });
  expect(duplicate.ok()).toBeTruthy();
  expect((await duplicate.json()).duplicate).toBe(true);
  const listed = await request.get("http://127.0.0.1:3001/api/cards");
  expect(listed.ok()).toBeTruthy();
  const body = await listed.json();
  expect(body.cards.some((card: {id:string;title:string}) => card.id === cardId && card.title === payload.title)).toBe(true);
  expect(body.seq).toBeGreaterThanOrEqual(firstAck.seq);
});

test("SyncBoard API rejects stale version updates without overwriting current card", async ({ request }) => {
  const suffix = `conflict-${Date.now()}`;
  const card = { id: suffix, title: "Initial", column: "todo", baseVersion: 0 };
  const create = await request.post("http://127.0.0.1:3001/api/mutations", { data: { id: `${suffix}-create`, type: "card.upsert", payload: card, baseVersion: 0 } });
  expect(create.ok()).toBeTruthy();
  const latest = await request.get("http://127.0.0.1:3001/api/cards");
  const current = (await latest.json()).cards.find((item: {id:string}) => item.id === suffix);
  const update = await request.post("http://127.0.0.1:3001/api/mutations", { data: { id: `${suffix}-update`, type: "card.upsert", payload: { ...card, title: "Fresh update" }, baseVersion: current.version } });
  expect(update.ok()).toBeTruthy();
  const stale = await request.post("http://127.0.0.1:3001/api/mutations", { data: { id: `${suffix}-stale`, type: "card.upsert", payload: { ...card, title: "Stale update" }, baseVersion: current.version } });
  expect(stale.status()).toBe(409);
  expect((await stale.json()).code).toBe("VERSION_CONFLICT");
});