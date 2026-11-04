"""Structural and source-grounding checks for the curated golden dataset."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/golden_dataset.json"
def review():
    cases=json.loads(DATA.read_text(encoding="utf-8"))
    ids=[c["id"] for c in cases]
    questions=[c["question"].strip().casefold() for c in cases]
    errors=[]
    if len(cases)!=60: errors.append(f"Expected 60 cases, found {len(cases)}")
    if len(set(ids))!=len(ids): errors.append("Duplicate case IDs")
    if len(set(questions))!=len(questions): errors.append("Duplicate questions")
    for c in cases:
        if c.get("review_status")!="assistant-reviewed": errors.append(f"{c.get('id')}: not assistant-reviewed")
        if not c.get("expected_answer","").strip(): errors.append(f"{c.get('id')}: missing expected answer")
        if not c.get("expected_sources"): errors.append(f"{c.get('id')}: missing expected source")
        for source in c.get("expected_sources",[]):
            if not (ROOT/source).is_file(): errors.append(f"{c.get('id')}: source file missing: {source}")
        if c.get("category") not in {"factual","safety","troubleshooting","unanswerable"}: errors.append(f"{c.get('id')}: invalid category")
        if "Human sign-off is still required" not in c.get("review_note",""): errors.append(f"{c.get('id')}: missing human-review caveat")
    report={"cases":len(cases),"unique_questions":len(set(questions)),"categories":{k:sum(c["category"]==k for c in cases) for k in sorted({c["category"] for c in cases})},"assistant_review":"passed" if not errors else "failed","human_review":"pending","errors":errors}
    (ROOT/"reports").mkdir(exist_ok=True)
    (ROOT/"reports/dataset_review.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    if errors: raise SystemExit(1)
if __name__=="__main__": review()
