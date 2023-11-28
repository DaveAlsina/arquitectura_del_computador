from abc import ABC, abstractmethod
from .schema import Org, Crop, Variable, Condition, ActuatorType, Actuator, Measurement, User, Permission, Base

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

        import os
        from dotenv import load_dotenv
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        load_dotenv()

        database = os.getenv('DB_NAME')
        host     = os.getenv('DB_HOST')
        port     = os.getenv('DB_PORT')
        user     = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        url      = f'postgresql://{user}:{password}@{host}:{port}/{database}'

        engine = create_engine(url)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        Base.metadata.create_all(engine)

    def create_user(self, user: str, password: str):
        print(f"Database adapter: Creating user {user} with password {password}")
        user = User(username=user, password=password)
        self.session.add(user)
        self.session.commit()

    def create_zone(self, zone: dict):
        print(f"Database adapter: Creating zone {zone}")

    def add_measurement(self, measurement: dict):
        print(f"Database adapter: Adding measurement {measurement}")