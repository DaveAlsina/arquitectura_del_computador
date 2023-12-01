from typing import List
from .schema import Org, Crop, Variable, Condition, ActuatorType, Actuator, Measurement, User, Permission, Base, create_engine_with_retry

class DBService:

    def __init__(self) -> None:
        print("DBService: Inicializando...")

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

        engine       = create_engine(url)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        Base.metadata.create_all(engine)

    #------------------------------
    # Create
    #------------------------------
    def create_user(self, user: str, email: str, password: str) -> User:
        print(f"DBService: Creating user {user} with password {password}")
        user = User(username=user, email=email, password=password)
        self.session.add(user)

        try:
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise e
    
    def create_org(self, name: str, description: str, password: str) -> Org:
        print(f"DBService: Creating org {name} with description {description} and password {password}")
        org = Org(name=name, description=description, password=password)
        self.session.add(org)
        
        try:
            self.session.commit()
            return org
        except Exception as e:
            self.session.rollback()
            raise e

    def create_crop(self, org_id: str, name: str, lat: float, lon: float) -> Crop:
        print(f"DBService: Creating crop {name} with org_id {org_id}")
        crop = Crop(name = name, org_id = org_id, coordinate_latitude = lat, coordinate_longitude = lon)
        self.session.add(crop)
        
        try:
            self.session.commit()
            return crop
        except Exception as e:
            self.session.rollback()
            raise e

    def create_variable(self, name: str, units: str, description: str) -> Variable:
        print(f"DBService: Creating variable {name} with units {units} and description {description}")
        variable = Variable(name = name, units = units, description = description)
        self.session.add(variable)
        
        try:
            self.session.commit()
            return variable
        except Exception as e:
            self.session.rollback()
            raise e

    def add_measurement(self,
                        datetime: str,
                        crop_id: str,
                        value: float,
                        variable_id: str):

        print(f"DBService: Adding measurement {datetime} with crop_id {crop_id} and value {value}")
        measurement = Measurement(datetime = datetime, crop_id = crop_id, value = value, variable_id = variable_id)
        self.session.add(measurement)

        try:
            self.session.commit()
            return measurement
        except Exception as e:
            self.session.rollback()
            raise e
        


    #------------------------------
    # Read
    #------------------------------

    def get_user(self, username: str) -> User:
        print(f"DBService: Getting user {username}")
        user = self.session.query(User).filter_by(username=username).first()
        return user

    def login(self, username: str, password: str) -> User:
        print(f"DBService: Logging user {username} with password {password}")
        user = self.session.query(User).filter_by(username=username, password=password).first()
        return user

    def get_measurement_by_id(self, measurement_id: str) -> Measurement:
        print(f"DBService: Getting measurement {measurement_id}")
        measurement = self.session.query(Measurement).filter_by(id=measurement_id).first()
        return measurement

    def get_measurements_by_crop_id(self, crop_id: str) -> List[Measurement]:
        print(f"DBService: Getting measurements for crop {crop_id}")
        measurements = self.session.query(Measurement).filter_by(crop_id=crop_id).all()
        return measurements

    def get_measurements_by_crop_and_variable(self, crop_id: str, variable_id: str) -> List[Measurement]:
        print(f"DBService: Getting measurements for crop {crop_id} and variable {variable_id}")
        measurements = self.session.query(Measurement).filter_by(crop_id=crop_id, variable_id=variable_id).all()
        return measurements

    
if __name__ == '__main__':

    db_service = DBService()

    #------------------------------
    # Create
    #------------------------------
    user = db_service.create_user('user1', 'pass1')
    print(f"User created: {user}")

    user = db_service.create_user('user1', 'pass1')
    print(f"User created: {user}")

    #org = db_service.create_org('org1', 'desc1', 'pass1')
    #print(f"Org created: {org}")

    #crop = db_service.create_crop('crop1', 'desc1', org.id, 1.0, 1.0)
    #print(f"Crop created: {crop}")

    #variable = db_service.create_variable('var1', 'unit1', 'desc1')
    #print(f"Variable created: {variable}")

    #------------------------------
    # Read
    #------------------------------
    #user = db_service.get_user('user1')
    #print(f"User retrieved: {user}")

    #user = db_service.login('user1', 'pass1')
    #print(f"User retrieved: {user}")

    #measurement = db_service.get_measurement_by_id('measurement1')
    #print(f"Measurement retrieved: {measurement}")

    #measurements = db_service.get_measurements_by_crop_id('crop1')
    #print(f"Measurements retrieved: {measurements}")