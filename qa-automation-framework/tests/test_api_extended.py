import pytest
from fastapi.testclient import TestClient
from mock_backend.app import app,devices
client=TestClient(app); AUTH={'Authorization':'Bearer demo-token'}
pytestmark=pytest.mark.api
@pytest.fixture(autouse=True)
def reset():
 devices.clear();devices.update({'fan-001':{'power':False,'speed':1,'name':'Fan'}})
@pytest.mark.parametrize('speed',[1,2,3,4,5])
def test_speed_valid(speed): assert client.patch('/devices/fan-001/speed',headers=AUTH,json={'speed':speed}).status_code==200
@pytest.mark.parametrize('speed',[0,6,-1,100,'high',None])
def test_speed_invalid(speed): assert client.patch('/devices/fan-001/speed',headers=AUTH,json={'speed':speed}).status_code==422
@pytest.mark.parametrize('token',['','Bearer bad','Basic abc','Bearer demo-tokenx'])
def test_invalid_auth(token): assert client.get('/devices',headers={'Authorization':token}).status_code==401
@pytest.mark.parametrize('enabled',['true','false'])
def test_power_toggle(enabled): assert client.put('/devices/fan-001/power',headers=AUTH,params={'enabled':enabled}).json()['power']==(enabled=='true')
@pytest.mark.parametrize('device',['missing','fan-404','unknown'])
def test_missing_device(device): assert client.get('/devices/'+device,headers=AUTH).status_code==404
def test_device_schema(): assert {'id','power','speed','name'} <= set(client.get('/devices/fan-001',headers=AUTH).json())
