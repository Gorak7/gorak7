import importlib.util
from pathlib import Path
SPEC=importlib.util.spec_from_file_location("analyze",Path(__file__).parents[1]/"analyze.py")
mod=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(mod)

def test_sample_detects_server_errors_and_auth_failures():
    root=Path(__file__).parents[1]
    access=mod.analyze(root/"sample_logs/access.log")
    assert access["total_lines"] == 6
    assert access["http_5xx_count"] == 3
    assert any(f["title"] == "HTTP 5xx error spike" for f in access["findings"])
    auth=mod.analyze(root/"sample_logs/auth.log",ssh_threshold=3)
    assert auth["ssh_failures_by_ip"]["203.0.113.20"] == 3

def test_empty_file(tmp_path):
    p=tmp_path/"empty.log"; p.write_text("")
    assert mod.analyze(p)["total_lines"] == 0
