from abc import ABC, abstractmethod
from .schema import Org, Crop, Variable, Condition, ActuatorType, Actuator, Measurement, User, Permission, Base, create_engine_with_retry
from .db_service import DBService

class DatabaseClient(ABC):

    @abstractmethod
    def create_user(self, user: str, password: str):
        pass
    
    @abstractmethod
    def create_zone(self, zone: dict):
        pass

    @abstractmethod
    def add_measurement(self, measurement: dict):
        pass

class DatabaseAdapter(DatabaseClient):

    def __init__(self) -> None:
        print("Database adapter: Inicializando...")
        self.service = DBService()


    #------------------------------
    # Create
    #------------------------------
    def create_user(self,
                    user: str,
                    email: str,
                    password: str) -> User:
        print(f"Database adapter: Creating user {user} with password {password}")
        return self.service.create_user(user, email, password)

    def create_org(self,
                   name: str,
                   description: str,
                   password: str) -> Org:

        print(f"Database adapter: Creating org {name} with description {description} and password {password}")
        return self.service.create_org(name, description, password)

    def create_variable(self,
                        name: str,
                        units: str,
                        description: str,) -> Variable:

        print(f"Database adapter: create_variable name: {name}, units: {units}, description: {description}")
        return self.service.create_variable(name, units, description)


    def create_zone(self,
                    org_id: str,
                    name: str,
                    latitud: str,
                    longitud,)-> Crop:

        print(f"Database adapter: Creating zone {name} with latitud {latitud} and longitud {longitud}")
        return self.service.create_crop(org_id, name, latitud, longitud)

    def add_measurement(self,
                        datetime: str,
                        crop_id: str,
                        value: float,
                        variable_id: str) -> Measurement:
        print(f"Database adapter: Adding measurement {datetime} {crop_id} {value} {variable_id}")
        return self.service.add_measurement(datetime, crop_id, value, variable_id)



    #------------------------------
    # Read
    #------------------------------
    def login(self,
               user: str,
               password: str) -> User:
        print(f"Database adapter: Logging in user {user} with password {password}")
        return self.service.login(user, password)

    def get_measurements(self,
                         crop_id: str,
                         variable_id: str,) -> list:

        print(f"Database adapter: Getting measurements from crop {crop_id} and variable {variable_id}")
        return self.service.get_measurements_by_crop_and_variable(crop_id, variable_id)