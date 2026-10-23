# SyncBoard — Offline-Friendly Collaborative Kanban

A full-stack portfolio application with a React/TypeScript client, Fastify API, WebSocket updates, SQLite persistence and an IndexedDB offline outbox.

## Features
- Create and move tasks across To do, In progress and Done.
- Persist cards and mutation events in SQLite; use WAL mode.
- Broadcast accepted updates to connected browsers over WebSockets.
- Give each mutation an idempotency key so retrying an acknowledged operation does not apply it twice.
- Use card versions to detect stale updates and show a user-controlled conflict resolution path.
- Store the local board and pending outbox in IndexedDB.
- Reconnect automatically and replay queued mutations after the server snapshot.
- Cache the app shell and static assets with a service worker for offline reloads after a successful online visit.

## Stack
Client: React, TypeScript, Vite, IndexedDB, WebSocket, service worker.
Server: Node.js 20+, Fastify, SQLite (better-sqlite3), WebSocket, Zod.
Tests: Playwright, axe-core, Vitest for the separate your-ui component library.

## Run locally
Terminal 1:
```bash
cd server
npm install
npm run dev
```
Terminal 2:
```bash
cd client
npm install
npm run dev
```
- Client: http://localhost:5173
- Health: http://localhost:3001/health
- Cards: http://localhost:3001/api/cards
- Event replay: http://localhost:3001/api/events?since=0

The default SQLite database is created as `server/syncboard.sqlite` when the server starts. Set `SQLITE_PATH` to change the location. Do not commit local database files.

## End-to-end tests
From `../evidence`, run `npm install`, `npx playwright install --with-deps chromium`, then `npm run test:e2e`. Tests cover task creation/movement, API persistence, mutation idempotency, stale-version conflicts, offline queueing and automated axe scans. Review generated results rather than assuming tests passed.

## Deployment
See [DEPLOYMENT.md](./DEPLOYMENT.md) and the repository-level [Render blueprint](../render.yaml). Deployment requires connecting the repository in Render and approving service creation.

## Architecture and limitations
The API uses a persistent SQLite file, suitable for a portfolio-scale single instance. It is not configured for horizontal scaling: multiple API replicas would have independent local databases and WebSocket client sets. For multi-instance production, migrate to managed PostgreSQL and a shared pub/sub system. This project does not currently include user authentication or per-board access controls, so do not expose sensitive data.
