# AI Quality Engineer Portfolio

Three end-to-end project tracks based on the AI Quality Engineer roadmap.

## 1. RAG Chatbot + LLM Evaluation Pipeline
[Project folder](./rag-eval-pipeline/)
- PDF/Markdown/text ingestion, chunking, sentence-transformer embeddings, ChromaDB, FastAPI, optional Gemini and Streamlit.
- 60 draft golden questions, source-hit CSV, Gemini-backed Ragas runner, DeepEval metrics/GEval runner, promptfoo config, optional LangSmith tracing and opt-in Ragas CI threshold gate.
- Human review of the draft benchmark and real evaluation runs are required before publishing quality claims.

## 2. Web + Mobile + API Test Automation Framework
[Project folder](./qa-automation-framework/)
- FastAPI smart-fan mock API, 46 API cases, 32 Playwright web cases, 10 Appium smoke cases, Selenium smoke, Postman collection, Docker Compose and Allure-enabled GitHub Actions.
- API and browser suites run in CI; Android/Selenium require local device/browser setup. Verify CI runs and attach real reports.

## 3. AI-Assisted API Test Generator
[Project folder](./llm-test-generator/)
- OpenAPI parser, Pydantic test schema, deterministic + optional Gemini generator, prompt v1/v2, localhost-only HTTP runner, coverage metrics, Streamlit dashboard and controlled mutation lab.
- Remaining: deeper request/response schema inference, richer generated negative/boundary cases, persisted run history and full mutation testing against API mutant builds.

## Reproducibility
Only claim tests, metrics and integrations that have actually run and whose reports are committed. Keep credentials in environment variables and use authorized test targets.
