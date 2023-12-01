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

    def create_user(self, user: str, password: str) -> User:
        print(f"DBService: Creating user {user} with password {password}")
        user = User(username=user, password=password)
        self.session.add(user)
        self.session.commit()
        return user
    
    def create_org(self, name: str, description: str, password: str) -> Org:
        print(f"DBService: Creating org {name} with description {description} and password {password}")
        org = Org(name=name, description=description, password=password)
        self.session.add(org)
        self.session.commit()
        return org

    def create_crop(self, name: str, description: str, org_id: str, lat: float, lon: float) -> Crop:
        print(f"DBService: Creating crop {name} with description {description} and org_id {org_id}")
        crop = Crop(name = name, description = description, org_id = org_id, coordinate_latitude = lat, coordinate_longitude = lon)
        self.session.add(crop)
        self.session.commit()
        return crop

    def create_variable(self, name: str, units: str, description: str) -> Variable:
        print(f"DBService: Creating variable {name} with units {units} and description {description}")
        variable = Variable(name = name, units = units, description = description)
        self.session.add(variable)
        self.session.commit()
        return variable
