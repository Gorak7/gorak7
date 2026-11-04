"""HTTP-level mutation testing against real FastAPI TestClient instances.

Each mutant changes the speed-validation behavior of an API endpoint. The
same contract test vectors are replayed against the baseline and every mutant.
"""
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

class SpeedPayload(BaseModel):
    speed: int

def create_mutant_app(mutant: str | None = None) -> FastAPI:
    app = FastAPI(title=f"Smart Fan API mutation target: {mutant or 'baseline'}")

    @app.patch("/devices/fan-001/speed")
    def update_speed(payload: SpeedPayload):
        speed = payload.speed
        if mutant == "off_by_one":
            valid = 1 <= speed < 5
        elif mutant == "no_lower_bound":
            valid = speed <= 5
        elif mutant == "no_upper_bound":
            valid = speed >= 1
        elif mutant == "always_valid":
            valid = True
        else:
            valid = 1 <= speed <= 5
        if not valid:
            from fastapi import HTTPException
            raise HTTPException(status_code=422, detail="Speed must be between 1 and 5")
        return {"device_id": "fan-001", "speed": speed}

    return app

CONTRACT_CASES = [
    (1, 200), (2, 200), (3, 200), (4, 200), (5, 200),
    (0, 422), (6, 422), (-1, 422), (99, 422),
]
MUTANTS = ("off_by_one", "no_lower_bound", "no_upper_bound", "always_valid")

def run_contract(app: FastAPI) -> list[dict]:
    client = TestClient(app)
    results = []
    for speed, expected_status in CONTRACT_CASES:
        response = client.patch("/devices/fan-001/speed", json={"speed": speed})
        results.append({
            "speed": speed,
            "expected_status": expected_status,
            "actual_status": response.status_code,
            "passed": response.status_code == expected_status,
        })
    return results

def run_mutations() -> dict:
    baseline = run_contract(create_mutant_app())
    if not all(case["passed"] for case in baseline):
        raise AssertionError("The baseline API does not satisfy the speed contract")
    details = {}
    for mutant in MUTANTS:
        cases = run_contract(create_mutant_app(mutant))
        killed_by = [case["speed"] for case in cases if not case["passed"]]
        details[mutant] = {
            "killed": bool(killed_by),
            "killed_by_inputs": killed_by,
            "total_contract_cases": len(cases),
        }
    killed = sum(item["killed"] for item in details.values())
    return {
        "baseline": {"passed": len(baseline), "total": len(baseline)},
        "mutants": details,
        "mutants_killed": killed,
        "mutants_total": len(MUTANTS),
        "mutation_score": killed / len(MUTANTS) if MUTANTS else 0.0,
    }

if __name__ == "__main__":
    import json
    print(json.dumps(run_mutations(), indent=2))
