const test = require('node:test');
const assert = require('node:assert/strict');
const request = require('supertest');
process.env.DEMO_MODE = 'true';
process.env.JWT_SECRET = 'test-only-secret-change-this';
const app = require('../server');

test('health endpoint reports status', async () => {
 const r = await request(app).get('/api/health');
 assert.equal(r.status,200); assert.equal(r.body.status,'ok');
});
test('IOC list returns seeded synthetic data', async () => {
 const r = await request(app).get('/api/iocs');
 assert.equal(r.status,200); assert.ok(Array.isArray(r.body.items));
});
test('invalid IOC type is rejected', async () => {
 const r = await request(app).post('/api/iocs').send({value:'test',type:'unknown',severity:'high'});
 assert.equal(r.status,400);
});
test('valid IOC can be added', async () => {
 const r = await request(app).post('/api/iocs').send({value:'203.0.113.77',type:'ip',severity:'medium',confidence:50});
 assert.equal(r.status,201); assert.equal(r.body.value,'203.0.113.77');
});
test('duplicate IOC is rejected', async () => {
 const data={value:'203.0.113.77',type:'ip',severity:'medium',confidence:50};
 const r=await request(app).post('/api/iocs').send(data);
 assert.equal(r.status,409);
});
