import streamlit as st
import requests
st.set_page_config(page_title="RAG Quality Lab",page_icon="🧪",layout="wide")
st.title("RAG Chatbot – Quality Lab")
api=st.sidebar.text_input("API base URL","http://localhost:8000")
st.sidebar.caption("Start the FastAPI server and build the vector index before asking questions.")
question=st.text_input("Ask a question about the sample fan documents")
if st.button("Ask",type="primary",disabled=not question.strip()):
    try:
        response=requests.post(api.rstrip("/")+"/ask",json={"question":question,"top_k":4},timeout=90)
        response.raise_for_status()
        data=response.json()
        st.subheader("Answer")
        st.write(data["answer"])
        st.subheader("Retrieved sources")
        for item in data.get("contexts",[]):
            with st.expander(item["source"]):
                st.write(item["text"])
                st.caption(f"Cosine distance: {item.get('distance')}")
    except requests.RequestException as exc: st.error(f"API request failed: {exc}")
