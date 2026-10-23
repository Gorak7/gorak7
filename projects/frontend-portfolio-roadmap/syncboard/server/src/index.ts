import Fastify from "fastify";
import cors from "@fastify/cors";
import { WebSocketServer, WebSocket } from "ws";
import { randomUUID } from "node:crypto";
import { z } from "zod";
const app=Fastify({logger:true});await app.register(cors,{origin:true});
const CardSchema=z.object({id:z.string(),title:z.string().min(1).max(160),column:z.enum(["todo","doing","done"]),updatedAt:z.number().optional()});
type Card=z.infer<typeof CardSchema>;const cards=new Map<string,Card>();const clients=new Set<WebSocket>();const seen=new Set<string>();let seq=0;
app.get("/health",async()=>({status:"ok",service:"syncboard-server"}));
app.get("/api/cards",async()=>({seq,cards:[...cards.values()]}));
app.post("/api/cards",async(req,reply)=>{const parsed=CardSchema.safeParse(req.body);if(!parsed.success)return reply.code(400).send({error:"Invalid card",details:parsed.error.flatten()});const card={...parsed.data,updatedAt:Date.now()};cards.set(card.id,card);const event={type:"card.upsert",mutationId:randomUUID(),seq:++seq,payload:card};broadcast(event);return reply.code(201).send({card,seq});});
await app.listen({port:Number(process.env.PORT??3001),host:"0.0.0.0"});
const wss=new WebSocketServer({server:app.server,path:"/ws"});
wss.on("connection",socket=>{clients.add(socket);socket.send(JSON.stringify({type:"snapshot",seq,cards:[...cards.values()]}));socket.on("message",raw=>{let input:unknown;try{input=JSON.parse(raw.toString())}catch{socket.send(JSON.stringify({type:"error",message:"Invalid JSON"}));return;}const parsed=z.object({id:z.string().min(1),type:z.literal("card.upsert"),payload:CardSchema}).safeParse(input);if(!parsed.success){socket.send(JSON.stringify({type:"error",message:"Invalid mutation envelope"}));return;}if(seen.has(parsed.data.id)){socket.send(JSON.stringify({type:"ack",id:parsed.data.id,duplicate:true,seq}));return;}seen.add(parsed.data.id);const card={...parsed.data.payload,updatedAt:Date.now()};cards.set(card.id,card);const event={type:"card.upsert",mutationId:parsed.data.id,seq:++seq,payload:card};broadcast(event);socket.send(JSON.stringify({type:"ack",id:parsed.data.id,seq}));});socket.on("close",()=>clients.delete(socket));});
function broadcast(event:object){const data=JSON.stringify(event);for(const client of clients)if(client.readyState===WebSocket.OPEN)client.send(data);}
app.log.info("SyncBoard HTTP + WebSocket server ready");