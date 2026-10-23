# SyncBoard deployment and end-to-end verification

## Deployment target
The root `render.yaml` blueprint defines three public services:
- `syncboard-api`: Dockerized Fastify/WebSocket API backed by SQLite on a persistent disk.
- `syncboard-ui`: static React app, configured to connect to `wss://syncboard-api.onrender.com/ws`.
- `your-ui`: static React component playground.

## Publish
1. Open Render and choose **New → Blueprint**.
2. Connect the public `Gorak7/gorak7` GitHub repository.
3. Select the repository root and apply the `projects/frontend-portfolio-roadmap/render.yaml` blueprint.
4. Review service settings and approve creation. Provider account access and approval are required; committing this file does not itself deploy services.
5. Once services are created, confirm the actual generated hostnames. If they differ from the names in the blueprint, update `VITE_WS_URL` on the frontend and `CORS_ORIGIN` on the API, then redeploy.

## Persistence
The API uses SQLite WAL mode and `SQLITE_PATH`. On Render, the persistent disk mounts at `/var/data`. Do not use ephemeral filesystem storage for production data.

## Verification checklist
- [ ] API `/health` reports status `ok` and persistence `sqlite`.
- [ ] Create a task, restart/redeploy API, and confirm it remains.
- [ ] Open two browsers and verify accepted edits appear in both.
- [ ] Create and move a task while offline, reload while offline, reconnect, and verify queued changes.
- [ ] Trigger a version conflict from two clients and explicitly resolve it.
- [ ] Run Playwright and inspect screenshots, trace/video artifacts, axe results and Lighthouse reports.
- [ ] Confirm no secrets or local database files are committed.

## Important limitation
SQLite storage is appropriate for a portfolio-scale single API instance with a persistent disk. Do not horizontally scale this service to multiple instances: each process would have a different local database and WebSocket clients. For multi-instance production, move to managed PostgreSQL and a shared pub/sub mechanism.
