"""Optional online LLM evaluation; requires RAGAS and configured judge credentials."""
import os,pytest
pytestmark=pytest.mark.skipif(not os.getenv("RUN_LLM_EVAL"),reason="Set RUN_LLM_EVAL=1 and configure judge credentials")
def test_ragas_dependencies_are_available():
    import ragas
    assert ragas is not None
