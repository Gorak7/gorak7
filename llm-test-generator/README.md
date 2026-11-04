# AI-Assisted API Test Generator

OpenAPI-to-test-case generator with typed validation, deterministic baseline, optional Gemini JSON generation, safe local test execution, metrics and Streamlit UI.

## Architecture
OpenAPI JSON → parser → versioned prompt (v1/v2) → deterministic or Gemini generator → Pydantic validation → allowlisted HTTP runner → coverage/validity/duplicate metrics → dashboard/export.

## Setup
`pip install -r requirements.txt`
`python -m src.cli --spec specs/device-openapi.json --output reports/generated.json`
`streamlit run app/dashboard.py`

Set `GEMINI_API_KEY` and optionally `GEMINI_MODEL` to enable Gemini. Without a key use the deterministic baseline. Do not place credentials in source files.

## Safety
The HTTP runner permits only plain HTTP to localhost/127.0.0.1/testserver. It rejects remote hosts and URL-shaped paths. Use a disposable local test API; never execute generated requests against production. Add request body/schema generation and stricter path-template validation before using generated cases beyond this demo.

## Metrics and limitations
Validity rate currently reflects Pydantic-validated in-memory cases; operation coverage measures unique operations touched; duplicate rate detects duplicate operation/name pairs. Executability and mutation kill rate require executing against each baseline/mutant target and are not claimed by this starter implementation. LLM-generated expected outcomes need human review.

## Roadmap status
Implemented: parser, typed schema, baseline generator, Gemini adapter, prompt versions, local allowlist runner, basic metrics, dashboard and tests. Remaining: richer parameter/body/schema extraction, 30–50 cases, execution report persistence, controlled mutants and DeepEval GEval scoring.
