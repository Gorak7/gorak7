from fastapi import FastAPI
from pydantic import BaseModel, Field
from src.rag import answer

app = FastAPI(title="RAG Evaluation Demo", version="0.1.0")

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(payload: AskRequest):
    return answer(payload.question)
