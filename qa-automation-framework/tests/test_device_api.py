import pytest
from fastapi.testclient import TestClient
from mock_backend.app import app, devices

client = TestClient(app)
AUTH = {"Authorization": "Bearer demo-token"}

@pytest.fixture(autouse=True)
def reset_state():
    devices.clear()
    devices.update({"fan-001": {"power": False, "speed": 1}})

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_auth_required():
    assert client.get("/devices").status_code == 401

def test_list_devices():
    response = client.get("/devices", headers=AUTH)
    assert response.status_code == 200
    assert response.json()[0]["id"] == "fan-001"

@pytest.mark.parametrize("speed", [1, 2, 3, 4, 5])
def test_valid_speed_boundaries(speed):
    response = client.patch("/devices/fan-001/speed", headers=AUTH, json={"speed": speed})
    assert response.status_code == 200
    assert response.json()["speed"] == speed

@pytest.mark.parametrize("speed", [0, 6, -1])
def test_invalid_speed(speed):
    assert client.patch("/devices/fan-001/speed", headers=AUTH, json={"speed": speed}).status_code == 422

def test_unknown_device():
    assert client.get("/devices/missing", headers=AUTH).status_code == 404
