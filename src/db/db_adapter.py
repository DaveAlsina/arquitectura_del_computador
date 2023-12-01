from abc import ABC, abstractmethod
from .db_service import DBService
from .schema import Org, Crop, Variable, Condition, ActuatorType, Actuator, Measurement, User, Permission, Base, create_engine_with_retry

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

    def create_user(self, user: str, password: str):
        print(f"Database adapter: Creating user {user} with password {password}")
        self.service.create_user(user, password)

    def create_org(self, name: str, description: str, password: str):
        print(f"Database adapter: Creating org {name} with description {description} and password {password}")
        self.service.create_org(name, description, password)

    def create_zone(self, zone: dict):
        print(f"Database adapter: Creating zone {zone}")

    def add_measurement(self, measurement: dict):
        print(f"Database adapter: Adding measurement {measurement}")