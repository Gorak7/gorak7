from src.models import GeneratedTestCase
from src.parser import operations
def generate_baseline(spec: dict) -> list[GeneratedTestCase]:
    """Deterministic operation-derived baseline; not an LLM implementation."""
    cases = []
    for op in operations(spec):
        codes = [int(c) for c in op["responses"] if str(c).isdigit() and 200 <= int(c) < 300]
        cases.append(GeneratedTestCase(name="Baseline valid request: " + op["operation_id"], operation_id=op["operation_id"], method=op["method"], path=op["path"], expected_status=codes[0] if codes else 200, category="positive", rationale="Derived from the documented OpenAPI operation and success response."))
    return cases
