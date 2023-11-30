import request_mediator
from typing import Union

from fastapi import FastAPI
class APIGateway():
    app = FastAPI()
    def __init__(self) -> None:
        print("\nAPIGateway: Inicializando...")
        self.request_mediator = request_mediator.RequestMediator()

    @app.get("/login/{user}")
    @app.get("/login/{password}")
    def log_in(self, user: str, password: str):
        print(f"\nAPIGateway: log_in user: {user}, password: {password}")
        self.request_mediator.log_in(user, password)

    @app.get("/login/{user}")
    @app.get("/login/{password}")
    def create_user(self, user: str, password: str):
        print(f"\nAPIGateway: create_user user: {user}, password: {password}")
        self.request_mediator.create_user(user, password)

        
    @app.get("/Zones/{zone}")
    def create_zone(self, zone: dict):
        print(f"\nAPIGateway: create_zone zone: {zone}")
        self.request_mediator.create_zone(zone)

    @app.get("/Measurement/{measurement}")
    def add_measurement(self, measurement: dict):
        print(f"\nAPIGateway: add_measurement measurement: {measurement}")
        self.request_mediator.add_measurement(measurement)
