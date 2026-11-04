"""Deterministic local baseline for RAG API tests."""
from dataclasses import dataclass

@dataclass
class Chunk:
    source: str
    text: str

DOCS = [
    Chunk("fan_manual.md", "Disconnect power before cleaning the fan. Do not spray liquid into the motor housing."),
    Chunk("faq.md", "If the fan does not start, check the power supply and remote batteries."),
]
STOPWORDS = {"what", "is", "the", "before", "should", "i", "do", "if", "does", "not", "a", "an", "to", "for", "of", "and", "my", "how"}

def retrieve(question: str, top_k: int = 3) -> list[Chunk]:
    terms = {w.lower().strip(".,?!") for w in question.split() if len(w) > 2 and w.lower().strip(".,?!") not in STOPWORDS}
    ranked = [(len(terms & set(c.text.lower().split())), c) for c in DOCS]
    return [c for score, c in sorted(ranked, key=lambda x: x[0], reverse=True) if score > 0][:top_k]

def answer(question: str) -> dict:
    chunks = retrieve(question)
    if not chunks:
        return {"answer": "I cannot find enough information in the supplied documents.", "sources": []}
    return {"answer": " ".join(c.text for c in chunks), "sources": [{"source": c.source, "text": c.text} for c in chunks]}
