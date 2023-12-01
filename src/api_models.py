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
    name: str

class Measurement(BaseModel):
    zone: str
    value: float


