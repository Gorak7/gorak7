require('dotenv').config();
const express = require('express');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const jwt = require('jsonwebtoken');
const { Pool } = require('pg');
const path = require('path');
const app = express();
app.use(helmet({ contentSecurityPolicy: false }));
app.use(express.json({limit:'32kb'}));
app.use(rateLimit({windowMs:60000,limit:120}));
app.use(express.static(path.join(__dirname,'public')));
const pool = process.env.DATABASE_URL ? new Pool({connectionString:process.env.DATABASE_URL}) : null;
const demo = process.env.DEMO_MODE === 'true' || !pool;
let iocs = [
 {id:1,value:'198.51.100.24',type:'ip',severity:'high',confidence:78,status:'investigating',source:'Synthetic feed',notes:'Reserved documentation IP used as a safe example.',created_at:new Date().toISOString()},
 {id:2,value:'example-suspicious.invalid',type:'domain',severity:'medium',confidence:45,status:'new',source:'Analyst report',notes:'Reserved .invalid domain; not a real threat indicator.',created_at:new Date().toISOString()},
 {id:3,value:'sha256:demo-hash-placeholder',type:'hash',severity:'low',confidence:20,status:'false_positive',source:'Lab exercise',notes:'Placeholder hash for UI demonstration.',created_at:new Date().toISOString()}
];
const secret = process.env.JWT_SECRET || 'local-demo-only-change-me';
function auth(req,res,next){const token=(req.headers.authorization||'').replace(/^Bearer\s+/i,'');if(!token&&demo){req.user={email:'demo@local',role:'admin'};return next()}try{req.user=jwt.verify(token,secret);next()}catch{return res.status(401).json({error:'Valid bearer token required'})}}
function validate(b){if(!b||typeof b.value!=='string'||b.value.trim().length<3||b.value.length>500)return 'IOC value must be 3–500 characters';if(!['ip','domain','url','hash'].includes(b.type))return 'Type must be ip, domain, url, or hash';if(!['low','medium','high','critical'].includes(b.severity))return 'Invalid severity';const c=Number(b.confidence??50);if(!Number.isInteger(c)||c<0||c>100)return 'Confidence must be an integer from 0 to 100';return null}
app.get('/api/health',(_req,res)=>res.json({status:'ok',mode:demo?'demo':'database'}));
app.get('/api/iocs',auth,async(req,res,next)=>{try{const {q,type,severity,status}=req.query;if(demo){let rows=[...iocs];if(q)rows=rows.filter(x=>(x.value+' '+x.notes).toLowerCase().includes(String(q).toLowerCase()));if(type)rows=rows.filter(x=>x.type===type);if(severity)rows=rows.filter(x=>x.severity===severity);if(status)rows=rows.filter(x=>x.status===status);return res.json({items:rows,total:rows.length})}const r=await pool.query('SELECT * FROM iocs WHERE ($1::text IS NULL OR value ILIKE $1 OR notes ILIKE $1) AND ($2::text IS NULL OR type=$2) AND ($3::text IS NULL OR severity=$3) AND ($4::text IS NULL OR status=$4) ORDER BY created_at DESC',[q?'%'+String(q).slice(0,200)+'%':null,type||null,severity||null,status||null]);res.json({items:r.rows,total:r.rowCount})}catch(e){next(e)}});
app.post('/api/iocs',auth,async(req,res,next)=>{try{const err=validate(req.body);if(err)return res.status(400).json({error:err});const d={value:req.body.value.trim(),type:req.body.type,severity:req.body.severity,confidence:Number(req.body.confidence??50),status:'new',source:String(req.body.source||'analyst').slice(0,100),notes:String(req.body.notes||'').slice(0,4000)};if(demo){if(iocs.some(x=>x.value.toLowerCase()===d.value.toLowerCase()&&x.type===d.type))return res.status(409).json({error:'Duplicate IOC already exists'});const item={id:Math.max(0,...iocs.map(x=>x.id))+1,...d,created_at:new Date().toISOString()};iocs.unshift(item);return res.status(201).json(item)}const r=await pool.query('INSERT INTO iocs(value,type,severity,confidence,status,source,notes) VALUES($1,$2,$3,$4,$5,$6,$7) ON CONFLICT(value,type) DO NOTHING RETURNING *',[d.value,d.type,d.severity,d.confidence,d.status,d.source,d.notes]);if(!r.rowCount)return res.status(409).json({error:'Duplicate IOC already exists'});res.status(201).json(r.rows[0])}catch(e){next(e)}});
app.patch('/api/iocs/:id',auth,async(req,res,next)=>{try{const {status,severity,confidence,notes}=req.body;if(status&&!['new','investigating','confirmed','false_positive'].includes(status))return res.status(400).json({error:'Invalid status'});if(severity&&!['low','medium','high','critical'].includes(severity))return res.status(400).json({error:'Invalid severity'});if(confidence!==undefined&&(!Number.isInteger(Number(confidence))||Number(confidence)<0||Number(confidence)>100))return res.status(400).json({error:'Confidence must be 0–100'});if(demo){const x=iocs.find(x=>x.id===Number(req.params.id));if(!x)return res.status(404).json({error:'IOC not found'});if(status)x.status=status;if(severity)x.severity=severity;if(confidence!==undefined)x.confidence=Number(confidence);if(notes!==undefined)x.notes=String(notes).slice(0,4000);return res.json(x)}const r=await pool.query('UPDATE iocs SET status=COALESCE($1,status),severity=COALESCE($2,severity),confidence=COALESCE($3,confidence),notes=COALESCE($4,notes) WHERE id=$5 RETURNING *',[status||null,severity||null,confidence===undefined?null:Number(confidence),notes===undefined?null:String(notes).slice(0,4000),Number(req.params.id)]);if(!r.rowCount)return res.status(404).json({error:'IOC not found'});res.json(r.rows[0])}catch(e){next(e)}});
app.use((e,_req,res,_next)=>{console.error(e.message);res.status(500).json({error:'Internal server error'})});
if(require.main===module)app.listen(process.env.PORT||3001,()=>console.log('IOC Platform listening on :' +(process.env.PORT||3001)));
module.exports=app;
