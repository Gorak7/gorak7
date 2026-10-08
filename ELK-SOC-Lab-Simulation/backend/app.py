import os
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch

ES_URL=os.getenv("ELASTICSEARCH_URL","http://localhost:9200")
INDEX=os.getenv("EVENTS_INDEX","soc-events")
app=FastAPI(title="ELK SOC Lab API",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
es=Elasticsearch(ES_URL)
def search(body):
    try: return es.search(index=INDEX,**body)
    except Exception as e: raise HTTPException(503,str(e))
@app.get("/api/health")
def health():
    try:
        x=es.info(); return {"status":"ok","cluster":x.get("cluster_name"),"version":x["version"]["number"]}
    except Exception as e: raise HTTPException(503,str(e))
@app.get("/api/stats")
def stats():
    x=search({"size":0,"aggs":{"severity":{"terms":{"field":"alert.severity.keyword","size":10}},"status":{"terms":{"field":"alert.status.keyword","size":10}},"events":{"value_count":{"field":"@timestamp"}}}})
    a=x.get("aggregations",{})
    return {"events":a.get("events",{}).get("value",0),"severity":{b["key"]:b["doc_count"] for b in a.get("severity",{}).get("buckets",[]) },"status":{b["key"]:b["doc_count"] for b in a.get("status",{}).get("buckets",[])}}
@app.get("/api/alerts")
def alerts(size:int=50):
    x=search({"size":min(max(size,1),200),"query":{"exists":{"field":"alert.rule_id"}},"sort":[{"@timestamp":"desc"}]})
    return [h["_source"]|{"_id":h["_id"]} for h in x["hits"]["hits"]]
@app.get("/api/events")
def events(size:int=50):
    x=search({"size":min(max(size,1),200),"sort":[{"@timestamp":"desc"}]})
    return [h["_source"]|{"_id":h["_id"]} for h in x["hits"]["hits"]]
@app.post("/api/alerts/{alert_id}/ack")
def ack(alert_id:str):
    try: doc=es.get(index=INDEX,id=alert_id)["_source"]
    except Exception: raise HTTPException(404,"Alert not found")
    doc.setdefault("alert",{})["status"]="acknowledged"
    doc["alert"]["acknowledged_at"]=datetime.now(timezone.utc).isoformat()
    es.index(index=INDEX,id=alert_id,document=doc,refresh=True)
    return {"status":"acknowledged","id":alert_id}
@app.get("/")
def dashboard(): return FileResponse("/frontend/index.html")
@app.get("/app.js")
def js(): return FileResponse("/frontend/app.js",media_type="text/javascript")
@app.get("/styles.css")
def css(): return FileResponse("/frontend/styles.css",media_type="text/css")
