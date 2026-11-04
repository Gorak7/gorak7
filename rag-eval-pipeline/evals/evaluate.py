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
        hit=int(any(s in sources for s in expected)) if expected else int(not result["contexts"])
        rows.append({"id":case["id"],"category":case["category"],"question":case["question"],"answer":result["answer"],"expected_sources":";".join(expected),"retrieved_sources":";".join(result["sources"]),"source_hit":hit})
    if not rows: raise SystemExit("Golden dataset is empty")
    Path("reports").mkdir(exist_ok=True)
    with open("reports/baseline.csv","w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    summary={"cases":len(rows),"source_hits":sum(r["source_hit"] for r in rows),"source_hit_rate":sum(r["source_hit"] for r in rows)/len(rows),"category_source_hit_rate":{}}
    for category in sorted({r["category"] for r in rows}):
        subset=[r for r in rows if r["category"]==category]
        summary["category_source_hit_rate"][category]=sum(r["source_hit"] for r in subset)/len(subset)
    Path("reports/baseline_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return summary
if __name__=="__main__": run()
