from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Smart Fan Mock API", version="1.0.0")
devices = {"fan-001": {"power": False, "speed": 1}}
TOKEN = "demo-token"

def authorize(value: str | None):
    if value != f"Bearer {TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

class SpeedUpdate(BaseModel):
    speed: int = Field(ge=1, le=5)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/devices")
def list_devices(authorization: str | None = Header(default=None)):
    authorize(authorization)
    return [{"id": key, **value} for key, value in devices.items()]

@app.get("/devices/{device_id}")
def get_device(device_id: str, authorization: str | None = Header(default=None)):
    authorize(authorization)
    if device_id not in devices:
        raise HTTPException(404, "Device not found")
    return {"id": device_id, **devices[device_id]}

@app.put("/devices/{device_id}/power")
def set_power(device_id: str, enabled: bool, authorization: str | None = Header(default=None)):
    authorize(authorization)
    if device_id not in devices:
        raise HTTPException(404, "Device not found")
    devices[device_id]["power"] = enabled
    return {"id": device_id, **devices[device_id]}

@app.patch("/devices/{device_id}/speed")
def set_speed(device_id: str, payload: SpeedUpdate, authorization: str | None = Header(default=None)):
    authorize(authorization)
    if device_id not in devices:
        raise HTTPException(404, "Device not found")
    devices[device_id]["speed"] = payload.speed
    return {"id": device_id, **devices[device_id]}
