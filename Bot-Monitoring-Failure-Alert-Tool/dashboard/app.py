from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="FlowOps | Bot Monitoring", page_icon="⚙️", layout="wide")
st.title("FlowOps — RPA Operations Console")
st.caption("DEMO DATA · Synthetic sample execution records. Not connected to a live A360 Control Room.")
base=Path(__file__).resolve().parents[1]/"data"/"execution_logs_demo.csv"
uploaded=st.file_uploader("Upload an A360-exported execution log CSV",type=["csv"])
try:
    df=pd.read_csv(uploaded if uploaded else base).fillna("")
except Exception as e:
    st.error(f"Unable to read CSV: {e}"); st.stop()
required={"run_id","bot_name","invoice_id","status","started_at","completed_at","duration_seconds","error_message"}
if not required.issubset(df.columns):
    st.error("CSV missing required columns: "+", ".join(sorted(required-set(df.columns)))); st.stop()
def category(r):
    s=str(r.error_message).lower()
    for c,terms in {"TIMEOUT":["timeout","timed out"],"DATABASE_ERROR":["database","sql","connection refused"],
    "FILE_SYSTEM_ERROR":["file not found","no such file"],"AUTHENTICATION_ERROR":["login failed","unauthorized"],
    "APPLICATION_ERROR":["application not responding","element not found"],
    "DATA_ERROR":["invalid invoice","duplicate","missing invoice","invalid gst"]}.items():
        if any(t in s for t in terms): return c
    return "UNKNOWN_ERROR" if str(r.status).upper() in ["FAILED","ERROR","TIMEOUT"] else "—"
df["error_category"]=df.apply(category,axis=1)
status=df.status.astype(str).str.upper()
failed=df[status.isin(["FAILED","ERROR","TIMEOUT"])]
success=df[status.isin(["SUCCESS","COMPLETED"])]
c1,c2,c3,c4=st.columns(4)
c1.metric("Total runs",len(df)); c2.metric("Successful",len(success)); c3.metric("Failed",len(failed))
c4.metric("Success rate",f"{len(success)/len(df)*100:.1f}%" if len(df) else "0%")
left,right=st.columns(2)
with left:
    st.subheader("Execution status")
    counts=df.status.value_counts().rename_axis("status").reset_index(name="runs")
    st.plotly_chart(px.pie(counts,names="status",values="runs",hole=.55),use_container_width=True)
with right:
    st.subheader("Failure categories")
    cats=failed.error_category.value_counts().rename_axis("category").reset_index(name="incidents")
    st.plotly_chart(px.bar(cats,x="category",y="incidents"),use_container_width=True)
st.subheader("Execution history")
f1,f2=st.columns(2)
status_filter=f1.multiselect("Status",sorted(df.status.astype(str).unique()),default=sorted(df.status.astype(str).unique()))
search=f2.text_input("Search run / invoice / error")
view=df[df.status.isin(status_filter)]
if search: view=view[view.astype(str).apply(lambda col: col.str.contains(search,case=False,na=False)).any(axis=1)]
st.dataframe(view, use_container_width=True, hide_index=True)
st.subheader("Incident queue")
st.dataframe(failed[["run_id","invoice_id","error_category","error_message","started_at"]],use_container_width=True,hide_index=True)
st.download_button("Download failure analysis CSV",failed.to_csv(index=False).encode(),file_name="failure_analysis.csv",mime="text/csv")
st.info("For persistent incident status updates, authentication, and multi-user access, connect a secured backend. This local dashboard is read-only and uses uploaded/local CSV data.")
