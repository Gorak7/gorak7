require('dotenv').config();
const express = require('express');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const { Pool } = require('pg');
const path = require('path');

const app = express();
app.use(helmet({ contentSecurityPolicy: false }));
app.use(express.json({ limit: '32kb' }));
app.use(rateLimit({ windowMs: 60_000, limit: 120 }));
app.use(express.static(path.join(__dirname, 'public')));

const pool = process.env.DATABASE_URL ? new Pool({ connectionString: process.env.DATABASE_URL }) : null;
const demo = process.env.DEMO_MODE === 'true' || !pool;
let incidents = [
  { id: 1, title: 'Suspicious sign-in attempts', description: 'Multiple failed logins from an unfamiliar source.', severity: 'high', status: 'investigating', assignee: 'SOC Analyst', created_by: 'demo@local', created_at: new Date().toISOString() },
  { id: 2, title: 'Endpoint malware alert', description: 'Simulated endpoint alert for workflow demonstration.', severity: 'critical', status: 'open', assignee: 'Unassigned', created_by: 'demo@local', created_at: new Date().toISOString() },
  { id: 3, title: 'Unusual DNS requests', description: 'Synthetic DNS anomaly requiring triage.', severity: 'medium', status: 'resolved', assignee: 'SOC Analyst', created_by: 'demo@local', created_at: new Date().toISOString() }
];
const jwtSecret = process.env.JWT_SECRET || 'local-demo-only-change-me';
function auth(req, res, next) {
  const token = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  if (!token && demo) { req.user = { email: 'demo@local', role: 'admin' }; return next(); }
  try { req.user = jwt.verify(token, jwtSecret); next(); }
  catch { return res.status(401).json({ error: 'Valid bearer token required' }); }
}
function validateIncident(body) {
  const allowed = ['low','medium','high','critical'];
  if (!body || typeof body.title !== 'string' || body.title.trim().length < 4 || body.title.length > 160) return 'Title must be 4–160 characters';
  if (!allowed.includes(body.severity)) return 'Severity must be low, medium, high, or critical';
  if (body.description && typeof body.description !== 'string') return 'Description must be text';
  return null;
}
app.get('/api/health', (_req, res) => res.json({ status: 'ok', mode: demo ? 'demo' : 'database' }));
app.post('/api/auth/login', async (req, res, next) => {
  try {
    const email = String(req.body?.email || '').trim().toLowerCase();
    const password = String(req.body?.password || '');
    if (!email || !password) return res.status(400).json({ error: 'Email and password are required' });
    if (demo) return res.json({ token: jwt.sign({ email, role: 'admin' }, jwtSecret, { expiresIn: '1h' }), user: { email, role: 'admin' }, note: 'Demo mode: configure PostgreSQL and seeded users for persistent auth' });
    const result = await pool.query('SELECT id,email,password_hash,role FROM app_users WHERE email=$1', [email]);
    if (!result.rowCount || !(await bcrypt.compare(password, result.rows[0].password_hash))) return res.status(401).json({ error: 'Invalid credentials' });
    const user = result.rows[0];
    res.json({ token: jwt.sign({ id: user.id, email: user.email, role: user.role }, jwtSecret, { expiresIn: '1h' }), user: { email: user.email, role: user.role } });
  } catch (e) { next(e); }
});
app.get('/api/incidents', auth, async (req, res, next) => {
  try {
    const { status, severity, q } = req.query;
    if (demo) {
      let rows = [...incidents];
      if (status) rows = rows.filter(x => x.status === status);
      if (severity) rows = rows.filter(x => x.severity === severity);
      if (q) rows = rows.filter(x => (x.title + ' ' + x.description).toLowerCase().includes(String(q).toLowerCase()));
      return res.json({ items: rows, total: rows.length });
    }
    const result = await pool.query(
      'SELECT * FROM incidents WHERE ($1::text IS NULL OR status=$1) AND ($2::text IS NULL OR severity=$2) AND ($3::text IS NULL OR title ILIKE $3 OR description ILIKE $3) ORDER BY created_at DESC',
      [status || null, severity || null, q ? '%' + String(q).slice(0,100) + '%' : null]);
    res.json({ items: result.rows, total: result.rowCount });
  } catch (e) { next(e); }
});
app.post('/api/incidents', auth, async (req, res, next) => {
  try {
    const error = validateIncident(req.body);
    if (error) return res.status(400).json({ error });
    const data = { title: req.body.title.trim(), description: String(req.body.description || '').slice(0,4000), severity: req.body.severity, assignee: String(req.body.assignee || 'Unassigned').slice(0,100), created_by: req.user.email };
    if (demo) {
      const item = { id: Math.max(0, ...incidents.map(x => x.id)) + 1, ...data, status: 'open', created_at: new Date().toISOString() };
      incidents.unshift(item); return res.status(201).json(item);
    }
    const result = await pool.query('INSERT INTO incidents(title,description,severity,assignee,created_by) VALUES($1,$2,$3,$4,$5) RETURNING *',
      [data.title,data.description,data.severity,data.assignee,data.created_by]);
    res.status(201).json(result.rows[0]);
  } catch (e) { next(e); }
});
app.patch('/api/incidents/:id', auth, async (req, res, next) => {
  try {
    const status = req.body?.status;
    const severity = req.body?.severity;
    if (status && !['open','investigating','resolved'].includes(status)) return res.status(400).json({ error: 'Invalid status' });
    if (severity && !['low','medium','high','critical'].includes(severity)) return res.status(400).json({ error: 'Invalid severity' });
    if (demo) {
      const item = incidents.find(x => x.id === Number(req.params.id));
      if (!item) return res.status(404).json({ error: 'Incident not found' });
      if (status) item.status = status; if (severity) item.severity = severity;
      if (req.body.assignee) item.assignee = String(req.body.assignee).slice(0,100);
      return res.json(item);
    }
    const result = await pool.query('UPDATE incidents SET status=COALESCE($1,status), severity=COALESCE($2,severity), assignee=COALESCE($3,assignee), updated_at=NOW() WHERE id=$4 RETURNING *',
      [status || null, severity || null, req.body.assignee ? String(req.body.assignee).slice(0,100) : null, Number(req.params.id)]);
    if (!result.rowCount) return res.status(404).json({ error: 'Incident not found' });
    res.json(result.rows[0]);
  } catch (e) { next(e); }
});
app.use((err, _req, res, _next) => { console.error(err.message); res.status(500).json({ error: 'Internal server error' }); });
if (require.main === module) app.listen(process.env.PORT || 3000, () => console.log('Incident Manager listening on :' + (process.env.PORT || 3000)));
module.exports = app;
