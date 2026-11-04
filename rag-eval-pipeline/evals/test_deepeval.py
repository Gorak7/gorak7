"""Optional DeepEval integration smoke test; judge calls are deliberately opt-in."""
import os,pytest
pytestmark=pytest.mark.skipif(not os.getenv("RUN_LLM_EVAL"),reason="Set RUN_LLM_EVAL=1 to enable judge tests")
def test_deepeval_available():
    import deepeval
    assert deepeval is not None
