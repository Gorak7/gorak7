def evaluate(cases, spec_operations: list[dict]) -> dict:
    ids = [c.operation_id for c in cases]
    expected = {o["operation_id"] for o in spec_operations}
    duplicates = len(ids) - len(set(ids))
    return {"generated_cases": len(cases), "validity_rate": 1.0 if cases else 0.0, "operation_coverage": len(set(ids) & expected) / len(expected) if expected else 0.0, "duplicate_rate": duplicates / len(cases) if cases else 0.0, "uncovered_operations": sorted(expected - set(ids))}
