import os
import sys
import unittest

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir)

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db import Org, Crop, Variable, Condition, ActuatorType, Actuator, Measurement, User, Permission, Base, create_engine_with_retry

load_dotenv()
database = os.getenv('DB_NAME')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
url = f'postgresql://{user}:{password}@{host}:{port}/{database}'

class TestModelInserts(unittest.TestCase):
    def setUp(self):
        # Set up the database connection
        #engine = create_engine_with_retry(url)
        engine = create_engine(url)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def tearDown(self):
        # Clean up the database session
        self.session.close()

        # Drop all tables
        engine = create_engine(url)
        Base.metadata.drop_all(engine)

    def test_org_model(self):
        org = Org(name='org1', description='desc1', password='pass1')
        self.session.add(org)
        self.session.commit()

        retrieved_org = self.session.query(Org).filter_by(name='org1').first()
        self.assertEqual(retrieved_org.name, 'org1')

    def test_crop_model(self):
        org = Org(name='org1', description='desc1', password='pass1')
        self.session.add(org)
        self.session.commit()

        crop = Crop(org_id=org.id, name='crop1', coordinate_latitude=1.0, coordinate_longitude=1.0)
        self.session.add(crop)
        self.session.commit()

        retrieved_crop = self.session.query(Crop).filter_by(name='crop1').first()
        self.assertEqual(retrieved_crop.name, 'crop1')

    def test_variable_model(self):
        variable = Variable(name='var1', units='unit1', description='desc1')
        self.session.add(variable)
        self.session.commit()

        retrieved_variable = self.session.query(Variable).filter_by(name='var1').first()
        self.assertEqual(retrieved_variable.name, 'var1')

    def test_condition_model(self):
        org = Org(name='org1', description='desc1', password='pass1')
        self.session.add(org)
        self.session.commit()

        crop = Crop(org_id=org.id, name='crop1', coordinate_latitude=1.0, coordinate_longitude=1.0)
        self.session.add(crop)
        self.session.commit()

        variable = Variable(name='var1', units='unit1', description='desc1')
        self.session.add(variable)
        self.session.commit()

        condition = Condition(crop_id=crop.id, variable_id=variable.id, min_value=1.0, max_value=1.0)
        self.session.add(condition)
        self.session.commit()

        retrieved_condition = self.session.query(Condition).filter_by(crop_id=crop.id).first()
        self.assertEqual(retrieved_condition.crop_id, crop.id)

    def test_user_model(self):
        user = User(username='user1', password='pass1', email='email1@email.com')
        user.save(self.session)

        retrieved_user = self.session.query(User).filter_by(username='user1').first()
        self.assertEqual(retrieved_user.username, 'user1')



if __name__ == '__main__':
    unittest.main()
