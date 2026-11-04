from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_answer_contains_sources():
    response = client.post("/ask", json={"question": "What before cleaning the fan?"})
    assert response.status_code == 200
    assert response.json()["sources"]

def test_reject_short_question():
    assert client.post("/ask", json={"question": "?"}).status_code == 422

def test_unanswerable_question_is_acknowledged():
    response = client.post("/ask", json={"question": "What is the warranty duration?"})
    assert response.status_code == 200
    assert response.json()["sources"]
    assert "do not specify" in response.json()["answer"].lower()
