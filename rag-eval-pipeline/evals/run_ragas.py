import argparse,csv,json,os
from pathlib import Path
from google import genai
from ragas.llms import llm_factory
from ragas.embeddings.base import embedding_factory
from ragas.metrics.collections import Faithfulness,ContextPrecision,ContextRecall,AnswerRelevancy
from src.rag import ask

def main():
 p=argparse.ArgumentParser();p.add_argument("--limit",type=int,default=10);a=p.parse_args()
 key=os.getenv("GEMINI_API_KEY")
 if not key: raise SystemExit("Set GEMINI_API_KEY")
 client=genai.Client(api_key=key)
 llm=llm_factory(os.getenv("GEMINI_MODEL","gemini-2.0-flash"),provider="google",client=client)
 emb=embedding_factory("google",model="gemini-embedding-001",client=client)
 metrics={"faithfulness":Faithfulness(llm=llm),"context_precision":ContextPrecision(llm=llm),"context_recall":ContextRecall(llm=llm),"answer_relevancy":AnswerRelevancy(llm=llm,embeddings=emb)}
 data=json.loads(Path("data/golden_dataset.json").read_text(encoding="utf-8"))
 if a.limit>0:data=data[:a.limit]
 rows=[]
 for item in data:
  result=ask(item["question"]);contexts=[x["text"] for x in result["contexts"]]
  row={"id":item["id"],"category":item["category"]}
  for name,metric in metrics.items():
   if name=="faithfulness": score=metric.score(user_input=item["question"],response=result["answer"],retrieved_contexts=contexts)
   elif name in {"context_precision","context_recall"}: score=metric.score(user_input=item["question"],reference=item["expected_answer"],retrieved_contexts=contexts)
   else: score=metric.score(user_input=item["question"],response=result["answer"])
   row[name]=getattr(score,"value",score)
  rows.append(row);print(item["id"],{k:row[k] for k in metrics})
 Path("reports").mkdir(exist_ok=True)
 with open("reports/ragas_scores.csv","w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 print("Saved reports/ragas_scores.csv")
if __name__=="__main__":main()
