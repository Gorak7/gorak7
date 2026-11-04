from src.ingest import chunk_text
from src.api import app
from fastapi.testclient import TestClient
def test_chunking_overlap_and_validation():
 assert chunk_text("one two three four five six",4,1)==["one two three four","four five six"]
 try: chunk_text("abc",2,2)
 except ValueError: pass
 else: assert False
def test_health(): assert TestClient(app).get("/health").json()["status"]=="ok"
def test_request_validation(): assert TestClient(app).post("/ask",json={"question":"?"}).status_code==422
