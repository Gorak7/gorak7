import Fastify from "fastify";
import cors from "@fastify/cors";
import Database from "better-sqlite3";
import { WebSocketServer, WebSocket } from "ws";
import { randomUUID } from "node:crypto";
import { z } from "zod";

const app = Fastify({ logger: true });
await app.register(cors, { origin: process.env.CORS_ORIGIN?.split(",") ?? true });
const db = new Database(process.env.SQLITE_PATH ?? "./syncboard.sqlite");
db.pragma("journal_mode = WAL");
db.pragma("foreign_keys = ON");
db.exec(`
  CREATE TABLE IF NOT EXISTS cards (
    id TEXT PRIMARY KEY, title TEXT NOT NULL, column_name TEXT NOT NULL,
    updated_at INTEGER NOT NULL, version INTEGER NOT NULL
  );
  CREATE TABLE IF NOT EXISTS mutations (
    id TEXT PRIMARY KEY, seq INTEGER NOT NULL, card_id TEXT NOT NULL,
    created_at INTEGER NOT NULL
  );
  CREATE TABLE IF NOT EXISTS events (
    seq INTEGER PRIMARY KEY AUTOINCREMENT, mutation_id TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL, payload TEXT NOT NULL, created_at INTEGER NOT NULL
  );
`);
type Card = { id: string; title: string; column: "todo" | "doing" | "done"; updatedAt: number; version: number };
const CardInput = z.object({
  id: z.string().min(1).max(100),
  title: z.string().trim().min(1).max(160),
  column: z.enum(["todo", "doing", "done"]),
  baseVersion: z.number().int().nonnegative().optional(),
  updatedAt: z.number().optional(),
});
const MutationInput = z.object({
  id: z.string().min(1).max(120),
  type: z.literal("card.upsert"),
  payload: CardInput,
  baseVersion: z.number().int().nonnegative().optional(),
  clientTimestamp: z.number().optional(),
});
const selectCard = db.prepare("SELECT id, title, column_name AS column, updated_at AS updatedAt, version FROM cards WHERE id = ?");
const allCards = db.prepare("SELECT id, title, column_name AS column, updated_at AS updatedAt, version FROM cards ORDER BY updated_at");
const selectEventByMutation = db.prepare("SELECT seq, mutation_id AS mutationId, type, payload FROM events WHERE mutation_id = ?");
const latestSeq = db.prepare("SELECT COALESCE(MAX(seq), 0) AS seq FROM events");
const selectEventsSince = db.prepare("SELECT seq, mutation_id AS mutationId, type, payload FROM events WHERE seq > ? ORDER BY seq LIMIT 1000");
const upsertCard = db.prepare(`INSERT INTO cards(id,title,column_name,updated_at,version) VALUES(@id,@title,@column,@updatedAt,@version)
  ON CONFLICT(id) DO UPDATE SET title=excluded.title,column_name=excluded.column_name,updated_at=excluded.updated_at,version=excluded.version`);
const insertEvent = db.prepare("INSERT INTO events(mutation_id,type,payload,created_at) VALUES(?,?,?,?)");
const insertMutation = db.prepare("INSERT INTO mutations(id,seq,card_id,created_at) VALUES(?,?,?,?)");
const commitMutation = db.transaction((mutationId: string, input: z.infer<typeof CardInput>) => {
  const existing = selectCard.get(input.id) as Card | undefined;
  if (existing && input.baseVersion !== undefined && input.baseVersion !== existing.version) {
    return { conflict: true as const, current: existing };
  }
  const card: Card = {
    id: input.id, title: input.title, column: input.column,
    updatedAt: Date.now(), version: (existing?.version ?? 0) + 1
  };
  upsertCard.run(card);
  const eventInfo = insertEvent.run(mutationId, "card.upsert", JSON.stringify(card), card.updatedAt);
  const seq = Number(eventInfo.lastInsertRowid);
  insertMutation.run(mutationId, seq, card.id, card.updatedAt);
  return { conflict: false as const, event: { type: "card.upsert", mutationId, seq, payload: card } };
});
const clients = new Set<WebSocket>();
function broadcast(event: object) {
  const data = JSON.stringify(event);
  for (const client of clients) if (client.readyState === WebSocket.OPEN) client.send(data);
}
function sendSnapshot(socket: WebSocket) {
  socket.send(JSON.stringify({ type: "snapshot", seq: (latestSeq.get() as {seq:number}).seq, cards: allCards.all() }));
}
function processMutation(raw: unknown, socket?: WebSocket) {
  const parsed = MutationInput.safeParse(raw);
  if (!parsed.success) {
    socket?.send(JSON.stringify({ type: "reject", code: "INVALID_MUTATION", message: "Invalid mutation envelope or card fields", details: parsed.error.flatten() }));
    return { status: 400, body: { error: "Invalid mutation", details: parsed.error.flatten() } };
  }
  const mutation = parsed.data;
  const prior = selectEventByMutation.get(mutation.id) as {seq:number;mutationId:string;type:string;payload:string} | undefined;
  if (prior) {
    const ack = { type: "ack", id: mutation.id, duplicate: true, seq: prior.seq };
    socket?.send(JSON.stringify(ack));
    return { status: 200, body: ack };
  }
  const result = commitMutation(mutation.id, { ...mutation.payload, baseVersion: mutation.baseVersion ?? mutation.payload.baseVersion });
  if (result.conflict) {
    const rejection = { type: "reject", code: "VERSION_CONFLICT", id: mutation.id, message: "Card changed on the server; refresh and resolve before retrying.", current: result.current };
    socket?.send(JSON.stringify(rejection));
    return { status: 409, body: rejection };
  }
  broadcast(result.event);
  const ack = { type: "ack", id: mutation.id, seq: result.event.seq };
  socket?.send(JSON.stringify(ack));
  return { status: 200, body: ack };
}
app.get("/health", async () => ({ status: "ok", service: "syncboard-server", persistence: "sqlite", seq: (latestSeq.get() as {seq:number}).seq }));
app.get("/api/cards", async () => ({ seq: (latestSeq.get() as {seq:number}).seq, cards: allCards.all() }));
app.get("/api/events", async (request, reply) => {
  const query = z.object({ since: z.coerce.number().int().nonnegative().default(0) }).safeParse(request.query);
  if (!query.success) return reply.code(400).send({ error: "since must be a non-negative integer" });
  const rows = selectEventsSince.all(query.data.since) as Array<{seq:number;mutationId:string;type:string;payload:string}>;
  return { events: rows.map(row => ({ ...row, payload: JSON.parse(row.payload) })), nextSeq: rows.at(-1)?.seq ?? query.data.since };
});
app.post("/api/mutations", async (request, reply) => {
  const result = processMutation(request.body);
  return reply.code(result.status).send(result.body);
});
app.post("/api/cards", async (request, reply) => {
  const parsed = CardInput.safeParse(request.body);
  if (!parsed.success) return reply.code(400).send({ error: "Invalid card", details: parsed.error.flatten() });
  const result = processMutation({ id: randomUUID(), type: "card.upsert", payload: parsed.data });
  if (result.status !== 200) return reply.code(result.status).send(result.body);
  return reply.code(201).send({ card: selectCard.get(parsed.data.id), ...result.body });
});
await app.listen({ port: Number(process.env.PORT ?? 3001), host: "0.0.0.0" });
const wss = new WebSocketServer({ server: app.server, path: "/ws" });
wss.on("connection", socket => {
  clients.add(socket);
  sendSnapshot(socket);
  socket.on("message", raw => {
    let input: unknown;
    try { input = JSON.parse(raw.toString()); }
    catch { socket.send(JSON.stringify({ type: "reject", code: "INVALID_JSON", message: "Message must be valid JSON" })); return; }
    processMutation(input, socket);
  });
  socket.on("close", () => clients.delete(socket));
  socket.on("error", error => app.log.warn({ error }, "WebSocket client error"));
});
app.addHook("onClose", async () => { for (const client of clients) client.close(); db.close(); });
app.log.info("SyncBoard durable SQLite + WebSocket server ready");