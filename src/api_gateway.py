#import request_mediator
import api_models

import fastapi as fapi


app = fapi.FastAPI()



class APIGateway():

    User = api_models.User()
    Zone = api_models.Zone()
    Measurement = api_models.Measurement()

    @app.get("/")
    def read_root(self):
        return {"conectado :P"}

    def __init__(self) -> None:
        print("\nAPIGateway: Inicializando...")
   

    @app.post("/register")
    def register(self,user: User):
        if user.username in users:
            raise fapi.HTTPException(status_code=400, detail="Username already exists")
        users[user.username] = user
        return {"message": "User registered successfully"}

    @app.post("/login")
    def login(self, user: User):
        if user.username not in users or users[user.username].password != user.password:
            raise fapi.HTTPException(status_code=400, detail="Invalid username or password")
        return {"message": "Logged in successfully"}

    @app.post("/zone")
    def create_zone(self,zone: Zone):
        if zone.name in zones:
            raise fapi.HTTPException(status_code=400, detail="Zone already exists")
        zones[zone.name] = []
        return {"message": "Zone created successfully"}

    @app.post("/measurement")
    def add_measurement(self,measurement: Measurement):
        if measurement.zone not in zones:
            raise fapi.HTTPException(status_code=400, detail="Zone does not exist")
        zones[measurement.zone].append(measurement.value)
        return {"message": "Measurement added successfully"}

    @app.get("/measurement/{zone}")
    def get_measurement(self,zone: str):
        if zone not in zones:
            raise fapi.HTTPException(status_code=400, detail="Zone does not exist")
        return {"measurements": zones[zone]}

    @app.get("/zones")
    def get_zones(self):
        return {"zones": list(zones.keys())}







    

