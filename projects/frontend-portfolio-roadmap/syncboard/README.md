# syncboard — Real-Time Collaborative Board

Full-stack Kanban starter based on the supplied roadmap. It includes a React board UI and Fastify/WebSocket server foundation. Production-grade offline replay, PostgreSQL persistence, authentication and conflict resolution are still roadmap tasks.

## Stack
Client: React, Vite, TypeScript. Server: Node.js 20+, Fastify, WebSockets, Zod.
Roadmap extensions: TanStack Query, Zustand, Dexie/IndexedDB, dnd-kit, PWA/Workbox, PostgreSQL/Drizzle, Vitest, MSW, Playwright and Lighthouse CI.

## Run locally
Terminal 1:
```bash
cd server && npm install && npm run dev
```
Terminal 2:
```bash
cd client && npm install && npm run dev
```
Server health check: http://localhost:3001/health
Client: http://localhost:5173

## Sync protocol to complete
Each mutation should include id, type, payload, baseVersion and clientTimestamp. Deduplicate mutation IDs, assign monotonically increasing sequence numbers, broadcast accepted events, and replay from lastSeq on reconnect. Persist an IndexedDB outbox before sending.

## Acceptance checklist
- [ ] Two browser clients sync board changes
- [ ] Duplicate mutation IDs are idempotent
- [ ] Offline edits persist and flush on reconnect
- [ ] Rejections roll back and show a message
- [ ] Keyboard-only and axe tests pass
- [ ] Playwright covers multi-client, offline/reconnect and rollback
- [ ] Lighthouse and bundle metrics are measured and published

Do not report performance figures or claim the full offline-first specification is done until verified.
