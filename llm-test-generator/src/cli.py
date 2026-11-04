import argparse, json
from pathlib import Path
from src.parser import load_spec, operations
from src.generator import generate_baseline
from src.evaluator import evaluate
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output", default="reports/generated.json")
    args = parser.parse_args()
    spec = load_spec(args.spec)
    ops = operations(spec)
    cases = generate_baseline(spec)
    report = {"cases": [c.model_dump() for c in cases], "evaluation": evaluate(cases, ops)}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["evaluation"], indent=2))
if __name__ == "__main__":
    main()
