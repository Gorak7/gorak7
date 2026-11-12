import importlib.util
from pathlib import Path
import pandas as pd
import pytest
spec=importlib.util.spec_from_file_location("monitor",Path(__file__).parents[1]/"src"/"monitor.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
def test_failure_categories():
    assert mod.classify("Invalid invoice number","FAILED")=="DATA_ERROR"
    assert mod.classify("Database connection refused","FAILED")=="DATABASE_ERROR"
    assert mod.classify("Execution timed out","TIMEOUT")=="TIMEOUT"
    assert mod.classify("Application not responding","FAILED")=="APPLICATION_ERROR"
def test_unknown_and_success():
    assert mod.classify("unclassified exception","FAILED")=="UNKNOWN_ERROR"
    assert mod.classify("","SUCCESS")==""
def sample():
    return pd.DataFrame([{"run_id":"R1","bot_name":"Invoice Bot","invoice_id":"I1","status":"FAILED","started_at":"2026-11-12T08:00:00","completed_at":"2026-11-12T08:00:05","duration_seconds":"5","error_message":"Database connection refused"}])
def test_normalize_and_validate():
    assert mod.normalize_logs(sample()).iloc[0].error_category=="DATABASE_ERROR"
    with pytest.raises(ValueError): mod.normalize_logs(sample().drop(columns=["run_id"]))
    bad=sample(); bad.loc[0,"duration_seconds"]="-1"
    with pytest.raises(ValueError): mod.normalize_logs(bad)
def test_monitor_csv_and_repeat_is_idempotent(tmp_path):
    csv=tmp_path/"logs.csv"; sample().to_csv(csv,index=False)
    db=tmp_path/"monitor.db"; out=tmp_path/"reports"
    first=mod.monitor_file(csv,out,f"sqlite:///{db}")
    second=mod.monitor_file(csv,out,f"sqlite:///{db}")
    assert first["failed_runs"]==1 and second["failed_runs"]==1
    from sqlalchemy import create_engine,text
    engine=create_engine(f"sqlite:///{db}")
    with engine.connect() as conn:
        assert conn.execute(text("select count(*) from bot_execution_runs")).scalar()==1
        assert conn.execute(text("select count(*) from bot_incidents")).scalar()==1
    engine.dispose()
