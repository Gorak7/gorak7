from fastapi import FastAPI,Header,HTTPException
from pydantic import BaseModel,Field
from threading import RLock
app=FastAPI(title="Smart Fan API",version="1.0.0")
_lock=RLock()
devices={"fan-001":{"power":False,"speed":1,"name":"Living room fan"}}
TOKEN="demo-token"
def authorize(value):
    if value != f"Bearer {TOKEN}": raise HTTPException(401,"Invalid or missing bearer token")
class SpeedUpdate(BaseModel):
    speed:int=Field(ge=1,le=5)
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/auth/token")
def issue_token(username:str="qa",password:str="qa-password"):
    if username!="qa" or password!="qa-password": raise HTTPException(401,"Invalid credentials")
    return {"access_token":TOKEN,"token_type":"bearer"}
@app.get("/devices")
def list_devices(authorization:str|None=Header(default=None)):
    authorize(authorization)
    with _lock: return [{"id":k,**v} for k,v in devices.items()]
@app.get("/devices/{device_id}")
def get_device(device_id:str,authorization:str|None=Header(default=None)):
    authorize(authorization)
    if device_id not in devices: raise HTTPException(404,"Device not found")
    with _lock: return {"id":device_id,**devices[device_id]}
@app.post("/devices",status_code=201)
def create_device(device_id:str,authorization:str|None=Header(default=None)):
    authorize(authorization)
    with _lock:
        if device_id in devices: raise HTTPException(409,"Device already exists")
        devices[device_id]={"power":False,"speed":1,"name":"Test fan"}
        return {"id":device_id,**devices[device_id]}
@app.delete("/devices/{device_id}",status_code=204)
def delete_device(device_id:str,authorization:str|None=Header(default=None)):
    authorize(authorization)
    with _lock:
        if device_id not in devices: raise HTTPException(404,"Device not found")
        del devices[device_id]
@app.put("/devices/{device_id}/power")
def set_power(device_id:str,enabled:bool,authorization:str|None=Header(default=None)):
    authorize(authorization)
    if device_id not in devices: raise HTTPException(404,"Device not found")
    with _lock:
        devices[device_id]["power"]=enabled
        return {"id":device_id,**devices[device_id]}
@app.patch("/devices/{device_id}/speed")
def set_speed(device_id:str,payload:SpeedUpdate,authorization:str|None=Header(default=None)):
    authorize(authorization)
    if device_id not in devices: raise HTTPException(404,"Device not found")
    with _lock:
        devices[device_id]["speed"]=payload.speed
        return {"id":device_id,**devices[device_id]}
