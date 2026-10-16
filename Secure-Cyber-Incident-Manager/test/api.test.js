const test = require('node:test');
const assert = require('node:assert/strict');
const request = require('supertest');
process.env.DEMO_MODE = 'true';
process.env.JWT_SECRET = 'test-only-secret-change-this';
const app = require('../server');

test('health endpoint reports status', async () => {
  const r = await request(app).get('/api/health');
  assert.equal(r.status, 200);
  assert.equal(r.body.status, 'ok');
});

test('incident list returns demo records', async () => {
  const r = await request(app).get('/api/incidents');
  assert.equal(r.status, 200);
  assert.ok(Array.isArray(r.body.items));
});

test('invalid incident title is rejected', async () => {
  const r = await request(app).post('/api/incidents').send({title:'no',severity:'high'});
  assert.equal(r.status, 400);
});

test('valid incident can be created', async () => {
  const r = await request(app).post('/api/incidents').send({title:'Test security incident',severity:'medium',description:'Synthetic test'});
  assert.equal(r.status, 201);
  assert.equal(r.body.title, 'Test security incident');
});
