import json
from pathlib import Path
HTTP_METHODS = {"get", "post", "put", "patch", "delete"}
def load_spec(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if "openapi" not in data or "paths" not in data:
        raise ValueError("Unsupported OpenAPI document")
    return data
def operations(spec: dict) -> list[dict]:
    found = []
    for path, item in spec["paths"].items():
        for method, op in item.items():
            if method.lower() in HTTP_METHODS and isinstance(op, dict):
                found.append({"path": path, "method": method.upper(), "operation_id": op.get("operationId", method + "_" + path), "responses": op.get("responses", {})})
    return found
