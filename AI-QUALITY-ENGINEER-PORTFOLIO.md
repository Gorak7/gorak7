# AI Quality Engineer Portfolio

Portfolio projects based on the AI Quality Engineer roadmap.

## 1. RAG Chatbot + LLM Evaluation Pipeline
[Project folder](./rag-eval-pipeline/)
- PDF/Markdown/text ingestion, ChromaDB + sentence-transformer retrieval, FastAPI, optional Gemini, Streamlit, 60 draft golden cases, source-hit report and optional promptfoo/Ragas/DeepEval/LangSmith dependencies.
- Remaining: human review of benchmark, actual Ragas/DeepEval scored runs and measured CI quality thresholds.

## 2. Web + Mobile + API Test Automation Framework
[Project folder](./qa-automation-framework/)
- FastAPI smart-fan mock service, pytest API tests, Playwright Page Object Model tests, Selenium smoke test, Appium Android sample tests, Postman collection, Allure dependency and GitHub Actions.
- Browser/mobile tests require local setup; complete the 80+ roadmap target and collect real screenshots/reports before claiming completion.

## 3. AI-Assisted API Test Generator
[Project folder](./llm-test-generator/)
- OpenAPI parser, Pydantic test-case schema, deterministic + optional Gemini generator, prompt versions, localhost-only runner, metrics, Streamlit dashboard and mutation lab.
- Remaining: full schema/body generation, API-runner orchestration, full mutant execution and DeepEval GEval.

## Reproducibility
Only claim tests, metrics and tool integrations that have actually been run and whose artifacts are committed. Keep API keys in environment variables and use authorized test targets.
