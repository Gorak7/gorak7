from pathlib import Path
from src.config import CHROMA_PATH,COLLECTION_NAME
MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"
def chunk_text(text:str,chunk_words:int=180,overlap:int=30)->list[str]:
 words=text.split()
 if chunk_words<1 or overlap<0 or overlap>=chunk_words: raise ValueError("Require chunk_words > overlap >= 0")
 result=[];step=chunk_words-overlap
 for start in range(0,len(words),step):
  part=" ".join(words[start:start+chunk_words])
  if part: result.append(part)
  if start+chunk_words>=len(words): break
 return result
def load_documents(directory:str="data/docs")->list[dict]:
 docs=[]
 for path in sorted(Path(directory).glob("**/*")):
  if path.is_file() and path.suffix.lower() in {".md",".txt"}:
   for i,part in enumerate(chunk_text(path.read_text(encoding="utf-8"))):
    docs.append({"id":f"{path.name}-{i}","text":part,"source":str(path),"chunk":i})
 return docs
def build_index(directory:str="data/docs",reset:bool=False)->int:
 import chromadb
 from sentence_transformers import SentenceTransformer
 docs=load_documents(directory)
 if not docs: raise ValueError(f"No .md or .txt documents found in {directory}")
 client=chromadb.PersistentClient(path=CHROMA_PATH)
 if reset:
  try: client.delete_collection(COLLECTION_NAME)
  except Exception: pass
 collection=client.get_or_create_collection(COLLECTION_NAME,metadata={"hnsw:space":"cosine"})
 model=SentenceTransformer(MODEL_NAME)
 vectors=model.encode([d["text"] for d in docs],normalize_embeddings=True).tolist()
 collection.upsert(ids=[d["id"] for d in docs],documents=[d["text"] for d in docs],metadatas=[{"source":d["source"],"chunk":d["chunk"]} for d in docs],embeddings=vectors)
 return len(docs)
if __name__=="__main__": print(f"Indexed {build_index(reset=True)} chunks")
