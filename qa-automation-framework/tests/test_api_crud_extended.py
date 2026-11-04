import pytest
from fastapi.testclient import TestClient
from mock_backend.app import app,devices
client=TestClient(app);AUTH={"Authorization":"Bearer demo-token"}
pytestmark=pytest.mark.api
@pytest.fixture(autouse=True)
def clean():
 devices.clear();devices.update({"fan-001":{"power":False,"speed":1,"name":"Fan"}})
@pytest.mark.parametrize("new_id",["fan-101","fan-102","fan-103","fan-104"])
def test_create_device_ids(new_id):
 r=client.post("/devices",headers=AUTH,params={"device_id":new_id})
 assert r.status_code==201 and r.json()["id"]==new_id
@pytest.mark.parametrize("new_id",["fan-201","fan-202","fan-203"])
def test_delete_device_ids(new_id):
 client.post("/devices",headers=AUTH,params={"device_id":new_id})
 r=client.delete("/devices/"+new_id,headers=AUTH)
 assert r.status_code==204 and new_id not in devices
@pytest.mark.parametrize("method,path",[
 ("get","/devices"),("get","/devices/fan-001"),("post","/devices"),("delete","/devices/fan-001")
])
def test_crud_requires_auth(method,path):
 response=getattr(client,method)(path)
 assert response.status_code==401
def test_duplicate_device_returns_conflict():
 assert client.post("/devices",headers=AUTH,params={"device_id":"fan-001"}).status_code==409
def test_deleted_device_is_not_readable():
 client.delete("/devices/fan-001",headers=AUTH)
 assert client.get("/devices/fan-001",headers=AUTH).status_code==404
