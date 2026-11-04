import csv,os,sys
from pathlib import Path
path=Path("reports/ragas_scores.csv")
if not path.exists(): raise SystemExit("Missing reports/ragas_scores.csv; run evals.run_ragas first")
with path.open(encoding="utf-8") as f: rows=list(csv.DictReader(f))
if not rows: raise SystemExit("Ragas report is empty")
def mean(key):
 values=[float(r[key]) for r in rows if r.get(key) not in (None,"")]
 if not values: raise SystemExit(f"No numeric values for {key}")
 return sum(values)/len(values)
limits={"faithfulness":float(os.getenv("MIN_FAITHFULNESS","0.70")),"answer_relevancy":float(os.getenv("MIN_ANSWER_RELEVANCY","0.60"))}
scores={k:mean(k) for k in limits}
print("Mean Ragas scores:",scores,"Thresholds:",limits)
failed=[k for k in limits if scores[k]<limits[k]]
if failed: raise SystemExit("Quality gate failed: "+", ".join(failed))
print("Quality gate passed")
