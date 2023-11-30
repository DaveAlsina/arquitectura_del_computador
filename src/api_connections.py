from typing import Union
from pydantic import BaseModel
import fastapi as fapi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

app = fapi.FastAPI()


@app.get("/")
def read_root():
    return {"conectado"}

@app.get("/sensor/{item_id}")
def read_item(item_id: int, b: bool = True, q: Union[str, None] = None):
    return {"sensor_id": item_id, "connected": b, "": q}

# In-memory data structures
users = {}
zones = {}
measurements = {}

# Pydantic models
class User(BaseModel):
    username: str
    password: str

class Zone(BaseModel):
    name: str

class Measurement(BaseModel):
    zone: str
    value: float

@app.post("/register")
def register(user: User):
    if user.username in users:
        raise fapi.HTTPException(status_code=400, detail="Username already exists")
    users[user.username] = user
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: User):
    if user.username not in users or users[user.username].password != user.password:
        raise fapi.HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Logged in successfully"}

@app.post("/zone")
def create_zone(zone: Zone):
    if zone.name in zones:
        raise fapi.HTTPException(status_code=400, detail="Zone already exists")
    zones[zone.name] = []
    return {"message": "Zone created successfully"}

@app.post("/measurement")
def add_measurement(measurement: Measurement):
    if measurement.zone not in zones:
        raise fapi.HTTPException(status_code=400, detail="Zone does not exist")
    zones[measurement.zone].append(measurement.value)
    return {"message": "Measurement added successfully"}

@app.get("/measurement/{zone}")
def get_measurement(zone: str):
    if zone not in zones:
        raise fapi.HTTPException(status_code=400, detail="Zone does not exist")
    return {"measurements": zones[zone]}

@app.get("/zones")
def get_zones():
    return {"zones": list(zones.keys())}