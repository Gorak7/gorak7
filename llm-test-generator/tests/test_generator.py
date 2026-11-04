from src.parser import load_spec, operations
from src.generator import generate_baseline
from src.evaluator import evaluate
SPEC = "specs/device-openapi.json"
def test_parser_finds_operations():
    assert len(operations(load_spec(SPEC))) == 4
def test_baseline_is_valid_and_covers_spec():
    spec = load_spec(SPEC)
    ops = operations(spec)
    cases = generate_baseline(spec)
    metrics = evaluate(cases, ops)
    assert len(cases) == 4
    assert metrics["operation_coverage"] == 1.0
    assert metrics["duplicate_rate"] == 0.0
