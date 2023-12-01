from typing import Union
from pydantic import BaseModel
import fastapi as fapi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

app = fapi.FastAPI()

# Pydantic models
class User(BaseModel):
    username: str
    email: str
    password: str

class Zone(BaseModel):
    org_id: str
    name: str
    latitude: float
    longitude: float

class Measurement(BaseModel):
    variable_id: str
    crop_id: str
    datetime: str
    value: float

class Organization(BaseModel):
    name: str
    description: str
    password: str

class Variable(BaseModel):
    name: str
    units: str
    description: str

