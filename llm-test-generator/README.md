# AI-Assisted API Test Generator

OpenAPI-to-test-case generator with Pydantic validation, deterministic baseline generation, optional Gemini JSON generation, a localhost-only HTTP runner, coverage metrics, Streamlit UI and HTTP-level API mutation testing.

## Run
```bash
pip install -r requirements.txt
python -m src.cli --spec specs/device-openapi.json --output reports/generated.json
# Optional LLM generation
GEMINI_API_KEY=... python -m src.cli --spec specs/device-openapi.json --llm --prompt-version v2
streamlit run app/dashboard.py
pytest -q
```

## Local API execution
Start the Project 2 FastAPI mock API on localhost, then run:
```bash
python -m src.cli --spec specs/device-openapi.json --run-local --base-url http://127.0.0.1:8000
``
The runner allows only plain HTTP to localhost/127.0.0.1 and rejects remote hosts, URL-shaped paths and path traversal. Use disposable local test targets only; never execute generated requests against production.

## HTTP mutation testing
```bash
python -m mutants.mutation_lab
pytest -q
``
The mutation lab creates separate FastAPI apps and sends real HTTP requests through FastAPI TestClient. It tests the baseline contract and four injected defects: off-by-one upper boundary, missing lower bound, missing upper bound and always-valid behavior. The suite reports a mutation score from the actual killed mutants. The score is valid only when the tests complete successfully in the latest CI run.

## Implemented vs remaining
Implemented: OpenAPI operation parsing, Pydantic test-case contract, deterministic and Gemini adapters, versioned prompts, local-only HTTP runner, basic operation coverage/duplicate metrics, Streamlit generation/export and API-level mutation lab. Remaining: deeper request/response schema inference, more generated negative/boundary scenarios, persisted execution history and human review of LLM-generated expectations.
