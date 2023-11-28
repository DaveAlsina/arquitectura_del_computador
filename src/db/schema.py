import uuid
import hashlib

from datetime import datetime
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID, TIME
#from sqlalchemy.ext.declarative import declared_attr
#from sqlalchemy_utils import ChoiceType

Base = declarative_base()

class Org(Base):
    __tablename__ = 'orgs'

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name        = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    password    = Column(String(64), nullable=False)

    crops = relationship('Crop', cascade='all, delete-orphan')

    def save(self, session):
        passlen = len(self.password)
        numbers = sum(c.isdigit() for c in self.password)
        letters = sum(c.isalpha() for c in self.password)
        spaces = sum(c.isspace() for c in self.password)

        hash_str = f"{self.password}.{passlen}.{letters}.{spaces}"
        hash_value = hashlib.sha256(hash_str.encode("utf-8")).hexdigest()

        self.password = hash_value

        session.add(self)
        session.commit()

    def __str__(self):
        return f"{self.id}.{self.name}"

class Crop(Base):
    __tablename__ = 'crops'

    id      = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    org_id  = Column(UUID(as_uuid=True), ForeignKey('orgs.id'), nullable=False)
    name    = Column(String(50), nullable=False)
    coordinate_latitude = Column(Float, nullable=False)
    coordinate_longitude = Column(Float, nullable=False)

    conditions = relationship('Condition', cascade='all, delete-orphan')
    actuators = relationship('Actuator', cascade='all, delete-orphan')
    measurements = relationship('Measurement', cascade='all, delete-orphan')

    def __str__(self):
        return f"{self.name}"

class Variable(Base):
    __tablename__ = 'variables'

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name        = Column(String(50), nullable=False)
    units       = Column(String(20), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return f"{self.name}.{self.units}"

class Condition(Base):
    __tablename__ = 'conditions'

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    crop_id     = Column(UUID(as_uuid=True), ForeignKey('crops.id'), nullable=False)
    variable_id = Column(UUID(as_uuid=True), ForeignKey('variables.id'), nullable=False)
    min_value   = Column(Float, nullable=False)
    max_value   = Column(Float, nullable=False)

    crop        = relationship('Crop', back_populates='conditions')
    variable    = relationship('Variable')

    def __str__(self):
        return f"{self.variable}.{self.min_value}.{self.max_value}"

class ActuatorType(Base):
    __tablename__ = 'actuator_types'

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name        = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self):
        return f"{self.name}"

class Actuator(Base):
    __tablename__ = 'actuators'

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name       = Column(String(50), nullable=False)
    mqtt_topic = Column(String(64), nullable=False)
    crop_id    = Column(UUID(as_uuid=True), ForeignKey('crops.id'), nullable=False)

    actuator_type_id = Column(UUID(as_uuid=True), ForeignKey('actuator_types.id'), nullable=False)
    start_time       = Column(TIME, nullable=True)
    end_time         = Column(TIME, nullable=True)

    crop          = relationship('Crop', back_populates='actuators')
    actuator_type = relationship('ActuatorType')

    def __str__(self):
        return f"{self.name}.{self.mqtt_topic}"

    def get_state(self):
        pass

    def set_state(self, state):
        pass

class Measurement(Base):
    __tablename__ = 'measurements'

    id          = Column(UUID(as_uuid = True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    datetime    = Column(DateTime, nullable = False, default = datetime.now)
    crop_id     = Column(UUID(as_uuid = True), ForeignKey('crops.id'), nullable = False)
    value       = Column(Float, nullable = False)
    variable_id = Column(UUID(as_uuid = True), ForeignKey('variables.id'), nullable = False)

    crop        = relationship('Crop', back_populates='measurements')
    variable    = relationship('Variable')

    def __str__(self):
        return f"{self.value}.{self.variable}.{self.crop}"

class User(Base):
    __tablename__ = 'users'

    id       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(64), nullable=False)

    def save(self, session):
        passlen = len(self.password)
        numbers = sum(c.isdigit() for c in self.password)
        letters = sum(c.isalpha() for c in self.password)
        spaces = sum(c.isspace() for c in self.password)

        hash_str = f"{self.password}.{passlen}.{letters}.{spaces}"
        hash_value = hashlib.sha256(hash_str.encode("utf-8")).hexdigest()

        self.password = hash_value

        session.add(self)
        session.commit()

    def __str__(self):
        return f"{self.username}"

class Permission(Base):
    __tablename__  = 'permissions'
    __table_args__ = (UniqueConstraint('user_id', 'org_id', 'crop_id', name='_user_org_crop_permission_uc'),)

    id      = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    org_id  = Column(UUID(as_uuid=True), ForeignKey('orgs.id'), nullable=False)
    crop_id = Column(UUID(as_uuid=True), ForeignKey('crops.id'), nullable=True)
    granted = Column(Boolean, default=False)
    _id     = Column(String(255), unique=True, nullable=False)
    #permission_type = Column(ChoiceType(Permission.PERMISSION_CHOICES), nullable=False)

    user = relationship('User')
    org = relationship('Org')
    crop = relationship('Crop')

    def __str__(self):
        if self.crop is None:
            return f"'{self.user.username}' has '{self.permission_type}' permission for '{self.org.name}'"
        else:
            return f"'{self.user.username}' has '{self.permission_type}' permission for '{self.org.name}' on crop '{self.crop.name}'"

    def save(self, session):
        conditions = {
            'user_id': str(self.user_id),
            'org_id': str(self.org_id),
            'permission_type': str(self.permission_type),
        }

        if self.crop_id is not None:
            conditions['crop_id'] = str(self.crop_id)

        self._id = '_'.join(conditions.values())

        session.add(self)
        session.commit()

if __name__ == '__main__':
    
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
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()