#import request_mediator
from api_models import User, Zone, Measurement, Organization, Variable
from request_mediator import RequestMediator
import fastapi as fapi


app = fapi.FastAPI()

class APIGateway():
    
    def __init__(self):
        self.request_mediator = RequestMediator()

    @app.get("/")
    def read_root(self):
        return {"conectado"}

    @app.get("/measurements/{zone_id}/{variable_id}")
    def get_measurements_by_zone_and_variable(zone_id: str, variable_id: str):
        response = self.request_mediator.get_measurements(crop_id=zone_id, variable_id=variable_id)
        if isinstance(response, tuple):
            raise fapi.HTTPException(status_code=response[0], detail=response[1])
        return response

    #--------------------#
    @app.post("/organization")
    def create_organization(self, organization: Organization):
        response = self.request_mediator.create_org(name=organization.name, description=organization.description, password=organization.password)
        if isinstance(response, tuple):
            raise fapi.HTTPException(status_code=response[0], detail=response[1])
        return {"message": "Organization created successfully", "id": response.id}

    @app.post("/variable")
    def create_variable(self, variable: Variable):
        response = self.request_mediator.create_variable(name=variable.name, units=variable.units, description=variable.description)
        if isinstance(response, tuple):
            raise fapi.HTTPException(status_code=response[0], detail=response[1])
        return {"message": "Variable created successfully", "id": response.id}

    @app.post("/register")
    def register(self, user: User):
        response = self.request_mediator.create_user(user=user.username, email=user.email,password=user.password)
        if isinstance(response, tuple):
            raise fapi.HTTPException(status_code=response[0], detail=response[1])
        return {"message": "User registered successfully", "id": response.id}

    @app.post("/login")
    def login(self, user: User):
        response = self.request_mediator.login(user=user.username,password=user.password)
        if isinstance(response, tuple):
            raise fapi.HTTPException(status_code=response[0], detail=response[1])
        return {"message": "Logged in successfully", "id": response.id}

    @app.post("/zone")
    def create_zone(self, zone: Zone):
        response = self.request_mediator.create_zone(org_id=zone.org_id, name=zone.name, latitud=zone.latitude, longitud=zone.longitude)
        if isinstance(response, tuple):
            raise fapi.HTTPException(status_code=response[0], detail=response[1])
        return {"message": "Zone created successfully", "id": response.id}

    @app.post("/measurement")
    def add_measurement(self, measurement: Measurement):
        response = self.request_mediator.add_measurement(variable_id=measurement.variable_id, crop_id=measurement.crop_id, datetime=measurement.datetime, value=measurement.value)
        if isinstance(response, tuple):
            raise fapi.HTTPException(status_code=response[0], detail=response[1])
        return {"message": "Measurement added successfully", "id": response.id}