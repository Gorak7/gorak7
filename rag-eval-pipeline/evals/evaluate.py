import json,csv
from pathlib import Path
from src.rag import ask
DATA=Path("data/golden_dataset.json")
def run():
    cases=json.loads(DATA.read_text(encoding="utf-8"))
    rows=[]
    for case in cases:
        result=ask(case["question"])
        sources=" ".join(result["sources"]).lower()
        expected=[s.lower() for s in case["expected_sources"]]
        rows.append({"id":case["id"],"category":case["category"],"question":case["question"],"answer":result["answer"],"expected_sources":";".join(expected),"source_hit":int(any(s in sources for s in expected)) if expected else int(not result["contexts"])})
    Path("reports").mkdir(exist_ok=True)
    with open("reports/baseline.csv","w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    print(f"Evaluated {len(rows)} cases; source hit rate={sum(r['source_hit'] for r in rows)/len(rows):.3f}")
if __name__=="__main__": run()
