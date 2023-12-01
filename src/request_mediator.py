import psycopg2
import data_validator

from typing import Union, List, Tuple
from db import DatabaseAdapter, User, Crop, Measurement, Variable, Condition, ActuatorType, Actuator, Permission, Org, Base, create_engine_with_retry

class RequestMediator():

    def __init__(self) -> None:
        print("RequestMediator: Inicializando...")
        self.adapter = DatabaseAdapter()
        self.data_validator = data_validator.DataValidator()

    #------------------------------
    # Create
    #------------------------------
    def create_user(self,
                    user: str,
                    email: str,
                    password: str) -> Union[Tuple[int, str], bool]:

        print(f"\nRequestMediator: create_user user: {user}, password: {password}")
        is_valid = self.data_validator.validate_user(user, email, password)

        if is_valid:
            try:
                user = self.adapter.create_user(user, email, password)
                return user

            except Exception as e:
                if psycopg2.errors.UniqueViolation == type(e.orig):
                    return (400, "Username or email already exists")
                else:
                    raise e
        else:
            return (400, "Invalid username or password")

    def create_variable(self,
                        name: str,
                        units: str,
                        description: str):

        print(f"\nRequestMediator: create_variable name: {name}, units: {units}, description: {description}")
        
        try:
            return self.adapter.create_variable(name, units, description)

        except Exception as e:
            if psycopg2.errors.UniqueViolation == type(e.orig):
                return (400, "Variable already exists")
            else:
                raise e

    def create_org(self,
                   name: str,
                   description: str,
                   password: str):

        print(f"\nRequestMediator: create_org name: {name}, description: {description}, password: {password}")

        try:
            is_valid = self.data_validator.validate_user(name, 'valid@email.com', password)
        
            if is_valid:
                return self.adapter.create_org(name, description, password)
            else:
                return (400, "Invalid org name or password")

        except Exception as e:
            if psycopg2.errors.UniqueViolation == type(e.orig):
                return (400, "Org name already exists")
            else:
                raise e


    def create_zone(self,
                    org_id: str,
                    name: str,
                    latitud: float,
                    longitud: float,):
        print(f"\nRequestMediator: create_zone zone: {name} with latitud {latitud} and longitud {longitud}")
        
        try:
            return self.adapter.create_zone(org_id, name, latitud, longitud,)

        except Exception as e:
            if psycopg2.errors.UniqueViolation == type(e.orig):
                return (400, "Zone already exists")
            if psycopg2.errors.ForeignKeyViolation == type(e.orig):
                return (400, "Org does not exist")
            if psycopg2.errors.InvalidTextRepresentation == type(e.orig):
                return (400, "Invalid org UUID")
            else:
                raise e

    def add_measurement(self,
                        datetime: str,
                        crop_id: str,
                        value: float,
                        variable_id: str):

        print(f"\nRequestMediator: add_measurement measurement: {datetime} {crop_id} {value} {variable_id}")

        try:
            return self.adapter.add_measurement(datetime, crop_id, value, variable_id)
        except Exception as e:
            if psycopg2.errors.ForeignKeyViolation == type(e.orig):
                return (400, "Crop or variable does not exist")
            if psycopg2.errors.InvalidTextRepresentation == type(e.orig):
                return (400, "Invalid crop or variable UUID")
            else:
                raise e


    #------------------------------
    # Read
    #------------------------------
    def login(self, user: str, password: str) -> Union[Tuple[int, str], User]:
        print(f"\nRequestMediator: log_in user: {user}, password: {password}")
        is_valid = self.data_validator.validate_user(user, 'valid@email.com', password)
        
        if is_valid:
            try:
                user = self.adapter.login(user, password)

                if user is None:
                    return (400, "Invalid username or password, or user does not exist")
                return user

            except Exception as e:
                if psycopg2.errors.UniqueViolation == type(e.orig):
                    return (400, "Username already exists")
                else:
                    raise e
        else:
            return (400, "Invalid username or password")


    def get_measurements(self, crop_id: str, variable_id: str) -> Union[Tuple[int, str], List[Measurement]]:
        print(f"\nRequestMediator: get_measurements crop_id: {crop_id}, variable_id: {variable_id}")

        try:
            return self.adapter.get_measurements(crop_id, variable_id)
        except Exception as e:
            if psycopg2.errors.ForeignKeyViolation == type(e.orig):
                return (400, "Crop or variable does not exist")
            if psycopg2.errors.InvalidTextRepresentation == type(e.orig):
                return (400, "Invalid crop or variable UUID")
            else:
                raise e


#if __name__ == '__main__':
#    rm = RequestMediator()
    #ans = rm.create_user('user1', 'laurita@gmail.com', 'pass1word')
    #print(ans)

    #ans = rm.create_user('user6', 'laurita6@gmail.com', 'pass2word')
    #print(ans, ans.id, type(ans.id))

    #ans = rm.login('user2', 'pass1word')
    #print(ans)

    #ans = rm.create_variable('variable1', 'units1', 'description1')
    #print(ans)
    
    #ans = rm.create_org('org1', 'description1', 'pass1word')
    #print(ans)
    
    #ans = rm.create_zone(ans.id, 'zone1', 1.0, 1.0)
    #print(ans)

    #var = rm.create_variable('variable1', 'units1', 'description1')
    #print(var)
    #org = rm.create_org('org9', 'description1', 'pass1word')
    #print(org)
    #zone = rm.create_zone(org.id, 'zone8', 1.0, 1.0)
    #print(zone)

    #meas = rm.add_measurement('2021-01-01 00:00:00', zone.id, 1.0, var.id)
    #print(meas, meas.id, type(meas.id))

    #measurements = [rm.add_measurement(f'2021-01-01 00:00:0{i}', zone.id, i, var.id) for i in range(2, 10)]
    #print(measurements, "\n\n")

    #measurements2 = rm.get_measurements(zone.id, var.id)

    #print(measurements2, "\n\n")
    #print(measurements == measurements2)
    #print(len(measurements), len(measurements2))
