import json,streamlit as st
from pathlib import Path
from src.parser import load_spec,operations
from src.generator import generate_baseline,generate_with_gemini
from src.evaluator import evaluate
st.set_page_config(page_title='AI Test Generator',layout='wide')
st.title('AI-Assisted API Test Generator')
upload=st.file_uploader('Upload OpenAPI JSON',type=['json'])
prompt=st.selectbox('Prompt version',['v1','v2'],index=1)
mode=st.radio('Generator',['Deterministic baseline','Gemini LLM'])
if st.button('Generate test cases',type='primary'):
 try:
  spec=json.load(upload) if upload else load_spec('specs/device-openapi.json')
  cases=generate_baseline(spec) if mode.startswith('Deterministic') else generate_with_gemini(spec,prompt)
  metrics=evaluate(cases,operations(spec)); st.session_state['cases']=[c.model_dump() for c in cases]; st.session_state['metrics']=metrics
 except Exception as exc: st.error(str(exc))
if 'metrics' in st.session_state:
 st.json(st.session_state['metrics']); st.dataframe(st.session_state['cases'])
 st.download_button('Download generated cases',json.dumps(st.session_state['cases'],indent=2),'generated-tests.json','application/json')
