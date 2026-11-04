# AI Quality Engineer Portfolio

Three project tracks aligned to the AI Quality Engineer roadmap in this portfolio.

## 1. RAG Chatbot + LLM Evaluation Pipeline
[Open project](./rag-eval-pipeline/README.md) · [Source](./rag-eval-pipeline/src/)
- FastAPI local RAG baseline, source attribution, golden dataset and adversarial examples.
- Next: real document ingestion, embeddings/ChromaDB, Ragas/DeepEval, promptfoo, LangSmith and CI metric thresholds.

## 2. Web + Mobile + API Test Automation Framework
[Open project](./qa-automation-framework/README.md) · [Mock API](./qa-automation-framework/mock_backend/app.py)
- FastAPI smart-device API and pytest API tests are the initial executable baseline.
- Next: Playwright Page Object Model, Selenium smoke suite, Appium Android Screen Objects, Allure evidence and Dockerized runs.

## 3. AI-Assisted API Test Generator
[Open project](./llm-test-generator/README.md) · [CLI](./llm-test-generator/src/cli.py)
- OpenAPI parser, Pydantic test-case contract, deterministic baseline generator and coverage/duplicate metrics.
- Next: LLM provider adapter, prompt v1/v2 evaluation, allowlisted test execution, mutation testing and Streamlit dashboard.

## Reproducibility and honest reporting
These repositories are staged implementations, not claims that every roadmap milestone is complete. Report only tests and metrics reproduced from actual runs. Keep secrets in environment variables, use authorized test targets, and include sanitized screenshots and CI run links as evidence.
