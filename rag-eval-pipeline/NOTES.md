# Engineering notes

Record each experiment with date, commit, dataset version, model/provider, prompt version, chunk size, top-k, temperature, latency, cost and metric results.

## Experiment log
| Date | Change | Dataset | Result | Decision |
|---|---|---|---|---|
| TODO | Baseline | golden_dataset.json | Not measured yet | Establish baseline |

## Known gaps
- Current retriever is a tiny keyword baseline, not embeddings or a vector database.
- Current answerer is deterministic and does not call an LLM.
- Add ChromaDB ingestion, sentence-transformer embeddings, provider adapter, Ragas/DeepEval, promptfoo and LangSmith before claiming those capabilities.
