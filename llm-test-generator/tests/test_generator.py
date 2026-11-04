from src.parser import load_spec,operations
from src.generator import generate_baseline
from src.evaluator import evaluate
from src.runner import execute_case
import pytest
SPEC='specs/device-openapi.json'
def test_parser_finds_operations(): assert len(operations(load_spec(SPEC)))==4
def test_baseline_covers_spec():
 spec=load_spec(SPEC); ops=operations(spec); cases=generate_baseline(spec); metrics=evaluate(cases,ops)
 assert len(cases)==4 and metrics['operation_coverage']==1.0 and metrics['duplicate_rate']==0.0
def test_runner_blocks_remote_hosts():
 case=generate_baseline(load_spec(SPEC))[0]
 with pytest.raises(ValueError): execute_case(case,'https://example.com')
def test_runner_blocks_non_local_http():
 case=generate_baseline(load_spec(SPEC))[0]
 with pytest.raises(ValueError): execute_case(case,'http://example.com')

def test_baseline_includes_local_execution_data():
    cases=generate_baseline(load_spec(SPEC))
    speed=next(c for c in cases if c.operation_id=="updateSpeed")
    assert speed.path=="/devices/fan-001/speed"
    assert speed.body=={"speed":3}
    assert speed.headers["Authorization"]=="Bearer demo-token"
