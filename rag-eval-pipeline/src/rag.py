"""Small deterministic RAG baseline; replace LocalAnswerer with a provider adapter."""
from dataclasses import dataclass

@dataclass
class RetrievedChunk:
    source: str
    text: str

DOCUMENTS = [
    RetrievedChunk("docs/fan_manual.md", "Disconnect power before cleaning the fan. Do not spray liquid into the motor housing."),
    RetrievedChunk("docs/faq.md", "If the fan does not start, check the power supply and remote batteries before requesting service."),
]

def retrieve(question: str, top_k: int = 3) -> list[RetrievedChunk]:
    terms = {t.lower().strip(".,?!") for t in question.split() if len(t) > 2}
    scored = []
    for chunk in DOCUMENTS:
        words = set(chunk.text.lower().split())
        score = len(terms & words)
        if score:
            scored.append((score, chunk))
    return [c for _, c in sorted(scored, key=lambda x: x[0], reverse=True)[:top_k]]

def answer(question: str) -> dict:
    chunks = retrieve(question)
    if not chunks:
        return {"answer": "I cannot find enough information in the supplied documents.", "sources": []}
    context = " ".join(c.text for c in chunks)
    return {"answer": context, "sources": [{"source": c.source, "text": c.text} for c in chunks]}
