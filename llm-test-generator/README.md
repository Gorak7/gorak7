# AI-Assisted API Test Generator

OpenAPI-to-test-case generator with typed validation, deterministic baseline, optional Gemini JSON generation, a local-only HTTP runner, quality metrics, a mutation lab and Streamlit UI.

## Run
```bash
pip install -r requirements.txt
python -m src.cli --spec specs/device-openapi.json --output reports/generated.json
# Optional LLM generation
GEMINI_API_KEY=... python -m src.cli --spec specs/device-openapi.json --llm --prompt-version v2
streamlit run app/dashboard.py
pytest -q
```

## Architecture
OpenAPI JSON → parser → prompt v1/v2 → deterministic or Gemini generator → Pydantic validation → local-only HTTP runner → coverage/validity/duplicate metrics → dashboard/export.

## Safety
The runner permits only plain HTTP to localhost/127.0.0.1. It rejects remote hosts and URL-shaped paths. Use disposable local test targets only. Never execute generated requests against production.

## Implemented vs remaining
Implemented: OpenAPI operation parser, Pydantic contract, baseline and Gemini adapters, versioned prompt templates, safe runner, basic metrics, Streamlit generation/export, pure-function mutation lab and tests. Remaining: full parameter/request-body/schema extraction, execution result persistence and controlled mutant API orchestration, 30–50 meaningful generated cases, live baseline-vs-mutant API execution and DeepEval GEval evaluation. The current mutation lab validates sample speed-boundary mutants, not the full mock API. LLM expected outcomes require human review.
