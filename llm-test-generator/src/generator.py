import json,os
from src.models import GeneratedTestCase
from src.parser import operations
from src.prompts import PROMPTS

def generate_baseline(spec:dict)->list[GeneratedTestCase]:
 cases=[]
 for op in operations(spec):
  codes=[int(c) for c in op['responses'] if str(c).isdigit() and 200<=int(c)<300]
  cases.append(GeneratedTestCase(name='Baseline valid request: '+op['operation_id'],operation_id=op['operation_id'],method=op['method'],path=op['path'],expected_status=codes[0] if codes else 200,category='positive',rationale='Derived from the documented OpenAPI operation and success response.'))
 return cases

def generate_with_gemini(spec:dict,prompt_version:str='v2')->list[GeneratedTestCase]:
 key=os.getenv('GEMINI_API_KEY')
 if not key: raise RuntimeError('Set GEMINI_API_KEY to enable LLM generation')
 from google import genai
 client=genai.Client(api_key=key)
 prompt=PROMPTS[prompt_version].format(spec=json.dumps(spec))
 response=client.models.generate_content(model=os.getenv('GEMINI_MODEL','gemini-2.0-flash'),contents=prompt,config={'response_mime_type':'application/json'})
 raw=json.loads(response.text)
 return [GeneratedTestCase.model_validate(item) for item in raw]
