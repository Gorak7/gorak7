import pytest
from fastapi.testclient import TestClient
from mock_backend.app import app
@pytest.fixture
def api_client(): return TestClient(app)
@pytest.fixture
def auth_headers(): return {"Authorization":"Bearer demo-token"}
