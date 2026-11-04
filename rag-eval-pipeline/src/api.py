from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from src.rag import ask
app=FastAPI(title="RAG Chatbot Evaluation API",version="1.0.0")
class AskRequest(BaseModel):
 question:str=Field(min_length=3,max_length=1500)
 top_k:int=Field(default=4,ge=1,le=10)
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/ask")
def ask_route(payload:AskRequest):
 try: return ask(payload.question,payload.top_k)
 except Exception as exc: raise HTTPException(status_code=503,detail=f"RAG service unavailable: {type(exc).__name__}")
