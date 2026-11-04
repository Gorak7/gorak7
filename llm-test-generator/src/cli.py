import argparse,json
from pathlib import Path
from src.parser import load_spec,operations
from src.generator import generate_baseline,generate_with_gemini
from src.evaluator import evaluate
from src.runner import execute_case
def main():
 p=argparse.ArgumentParser();p.add_argument("--spec",required=True);p.add_argument("--output",default="reports/generated.json");p.add_argument("--llm",action="store_true");p.add_argument("--prompt-version",choices=["v1","v2"],default="v2");p.add_argument("--run-local",action="store_true");p.add_argument("--base-url",default="http://127.0.0.1:8000");a=p.parse_args()
 spec=load_spec(a.spec);ops=operations(spec);cases=generate_with_gemini(spec,a.prompt_version) if a.llm else generate_baseline(spec)
 report={"cases":[c.model_dump() for c in cases],"evaluation":evaluate(cases,ops)}
 if a.run_local:
  results=[]
  for case in cases:
   try: results.append(execute_case(case,a.base_url))
   except Exception as exc: results.append({"name":case.name,"passed":False,"error":str(exc)})
  report["execution"]={"results":results,"passed":sum(bool(x.get("passed")) for x in results),"total":len(results)}
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2),encoding="utf-8");print(json.dumps(report,indent=2))
if __name__=="__main__":main()
