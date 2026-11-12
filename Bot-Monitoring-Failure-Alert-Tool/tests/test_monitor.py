import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("monitor",Path(__file__).parents[1]/"src"/"monitor.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def test_failure_categories():
    assert mod.classify("Invalid invoice number","FAILED")=="DATA_ERROR"
    assert mod.classify("Database connection refused","FAILED")=="DATABASE_ERROR"
    assert mod.classify("Execution timed out","TIMEOUT")=="TIMEOUT"
    assert mod.classify("Application not responding","FAILED")=="APPLICATION_ERROR"

def test_unknown_error():
    assert mod.classify("unclassified exception","FAILED")=="UNKNOWN_ERROR"

def test_success_no_error():
    assert mod.classify("","SUCCESS")==""
