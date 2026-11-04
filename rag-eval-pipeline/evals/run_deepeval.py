"""Run DeepEval RAG metrics and a custom tone/correctness GEval with Gemini judge."""
import argparse,json,os
from pathlib import Path
from pydantic import BaseModel
from google import genai
from deepeval.models import DeepEvalBaseLLM
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric,FaithfulnessMetric,GEval
from deepeval.test_case import LLMTestCase,LLMTestCaseParams
from src.rag import ask

class GeminiJudge(DeepEvalBaseLLM):
    def __init__(self):
        key=os.getenv("GEMINI_API_KEY")
        if not key: raise RuntimeError("Set GEMINI_API_KEY")
        self.client=genai.Client(api_key=key)
        self.model=os.getenv("GEMINI_MODEL","gemini-2.0-flash")
    def load_model(self): return self.client
    def generate(self,prompt:str,schema:BaseModel|None=None):
        config={"response_mime_type":"application/json","response_schema":schema} if schema else None
        response=self.client.models.generate_content(model=self.model,contents=prompt,config=config)
        if schema: return schema.model_validate_json(response.text)
        return response.text or ""
    async def a_generate(self,prompt:str,schema:BaseModel|None=None):
        return self.generate(prompt,schema)
    def get_model_name(self): return self.model

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--limit",type=int,default=10);args=parser.parse_args()
    cases=json.loads(Path("data/golden_dataset.json").read_text(encoding="utf-8"))
    if args.limit>0: cases=cases[:args.limit]
    judge=GeminiJudge();test_cases=[]
    for golden in cases:
        result=ask(golden["question"])
        test_cases.append(LLMTestCase(input=golden["question"],actual_output=result["answer"],expected_output=golden["expected_answer"],retrieval_context=[c["text"] for c in result["contexts"]]))
    metrics=[AnswerRelevancyMetric(model=judge),FaithfulnessMetric(model=judge),GEval(name="Support tone and answer quality",criteria="Evaluate whether the answer is concise, helpful, safe, and does not claim facts beyond the supplied reference.",evaluation_params=[LLMTestCaseParams.INPUT,LLMTestCaseParams.ACTUAL_OUTPUT,LLMTestCaseParams.EXPECTED_OUTPUT],model=judge,threshold=0.7)]
    Path("reports").mkdir(exist_ok=True)
    evaluate(test_cases=test_cases,metrics=metrics)
    print(f"DeepEval completed for {len(test_cases)} cases. Review the DeepEval output and local run artifacts.")
if __name__=="__main__": main()
