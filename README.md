# Data Registration Module

This Python code defines a RESTful API using the FastAPI module. The API handles various endpoints for managing organizations, variables, users, zones, and measurements. It also utilizes a `RequestMediator` to handle requests and interact with the underlying data storage.

## Endpoints

### 1. Root Endpoint

- **Route:** `/`
- **Method:** GET
- **Function:** `read_root`
- **Description:** Returns a simple JSON response indicating that the API is connected.

### 2. Measurements Endpoint

- **Route:** `/measurements/{zone_id}/{variable_id}`
- **Method:** GET
- **Function:** `get_measurements_by_zone_and_variable`
- **Parameters:**
  - `zone_id`: ID of the zone
  - `variable_id`: ID of the variable
- **Description:** Retrieves measurements for a specific zone and variable. Handles errors with appropriate HTTP responses.

### 3. Organization Endpoint

- **Route:** `/organization`
- **Method:** POST
- **Function:** `create_organization`
- **Parameters:** JSON payload representing an organization
- **Description:** Creates a new organization and returns a success message along with the organization's ID. Handles errors with appropriate HTTP responses.

### 4. Variable Endpoint

- **Route:** `/variable`
- **Method:** POST
- **Function:** `create_variable`
- **Parameters:** JSON payload representing a variable
- **Description:** Creates a new variable and returns a success message along with the variable's ID. Handles errors with appropriate HTTP responses.

### 5. Register Endpoint

- **Route:** `/register`
- **Method:** POST
- **Function:** `register`
- **Parameters:** JSON payload representing a user
- **Description:** Registers a new user and returns a success message along with the user's ID. Handles errors with appropriate HTTP responses.

### 6. Login Endpoint

- **Route:** `/login`
- **Method:** POST
- **Function:** `login`
- **Parameters:** JSON payload representing a user
- **Description:** Logs in a user and returns a success message along with the user's ID. Handles errors with appropriate HTTP responses.

### 7. Zone Endpoint

- **Route:** `/zone`
- **Method:** POST
- **Function:** `create_zone`
- **Parameters:** JSON payload representing a zone
- **Description:** Creates a new zone and returns a success message along with the zone's ID. Handles errors with appropriate HTTP responses.

### 8. Measurement Endpoint

- **Route:** `/measurement`
- **Method:** POST
- **Function:** `add_measurement`
- **Parameters:** JSON payload representing a measurement
- **Description:** Adds a new measurement and returns a success message along with the measurement's ID. Handles errors with appropriate HTTP responses.

Note: The code includes commented-out lines at the end (`# if __name__ == '__main__':`) which suggests that it may be intended for use as a standalone script. Uncommenting these lines would allow the API to be run independently.


# API Models

This Python code defines Pydantic data models for the application, which serves as the basis for request validation and serialization.

## FastAPI()

- **Variable:** `app`
  - **Type:** `FastAPI`
  - **Description:** An instance of the FastAPI class representing the main application.

## Pydantic Models

The code includes several Pydantic models that define the structure and validation rules for different data entities:

### 1. User Model

- **Attributes:**
  - `username` (str): User's username
  - `email` (str): User's email address
  - `password` (str): User's password
- **Type:** `BaseModel`
- **Description:** Represents the structure and validation rules for user-related data.

### 2. Zone Model

- **Attributes:**
  - `org_id` (str): Organization ID to which the zone belongs
  - `name` (str): Name of the zone
  - `latitude` (float): Latitude coordinates of the zone
  - `longitude` (float): Longitude coordinates of the zone
- **Type:** `BaseModel`
- **Description:** Defines the structure and validation rules for zone-related data.

### 3. Measurement Model

- **Attributes:**
  - `variable_id` (str): ID of the variable associated with the measurement
  - `crop_id` (str): ID of the crop associated with the measurement
  - `datetime` (str): Date and time of the measurement
  - `value` (float): Measurement value
- **Type:** `BaseModel`
- **Description:** Represents the structure and validation rules for measurement-related data.

### 4. Organization Model

- **Attributes:**
  - `name` (str): Name of the organization
  - `description` (str): Description of the organization
  - `password` (str): Password for the organization
- **Type:** `BaseModel`
- **Description:** Defines the structure and validation rules for organization-related data.

### 5. Variable Model

- **Attributes:**
  - `name` (str): Name of the variable
  - `units` (str): Measurement units for the variable
  - `description` (str): Description of the variable
- **Type:** `BaseModel`
- **Description:** Represents the structure and validation rules for variable-related data.

# RequestMediator Module

This Python code defines a `RequestMediator` class that acts as an intermediary between a FastAPI application and a PostgreSQL database using the `psycopg2` library. The class includes methods for handling various requests related to user creation, variable creation, organization creation, zone creation, and measurement addition.

## Dependencies

- **psycopg2:** A PostgreSQL adapter for Python.
- **data_validator:** An external module for validating user data.

## Classes and Functions

### 1. RequestMediator Class

- **Attributes:**
  - `adapter` (DatabaseAdapter): An instance of the `DatabaseAdapter` class for interfacing with the PostgreSQL database.
  - `data_validator` (DataValidator): An instance of the `data_validator.DataValidator` class for validating user data.

- **Methods:**

  #### Create Operations

  - **`create_user(self, user: str, email: str, password: str) -> Union[Tuple[int, str], bool]`**
    - Creates a new user in the database.
    - Validates user data and handles potential exceptions.
  
  - **`create_variable(self, name: str, units: str, description: str) -> Union[Tuple[int, str], bool]`**
    - Creates a new variable in the database.
    - Handles potential exceptions such as unique violations.

  - **`create_org(self, name: str, description: str, password: str) -> Union[Tuple[int, str], bool]`**
    - Creates a new organization in the database.
    - Validates organization data and handles potential exceptions.

  - **`create_zone(self, org_id: str, name: str, latitud: float, longitud: float) -> Union[Tuple[int, str], bool]`**
    - Creates a new zone in the database.
    - Handles potential exceptions, including unique violations and foreign key violations.

  - **`add_measurement(self, datetime: str, crop_id: str, value: float, variable_id: str) -> Union[Tuple[int, str], bool]`**
    - Adds a new measurement to the database.
    - Handles potential exceptions, including foreign key violations and invalid text representations.

  #### Read Operations

  - **`login(self, user: str, password: str) -> Union[Tuple[int, str], User]`**
    - Logs in a user and returns user data if successful.
    - Validates user data and handles potential exceptions.

  - **`get_measurements(self, crop_id: str, variable_id: str) -> Union[Tuple[int, str], List[Measurement]]`**
    - Retrieves measurements based on crop and variable IDs.
    - Handles potential exceptions, including foreign key violations and invalid text representations.

  #### Initialization

  - **`__init__(self) -> None`**
    - Initializes the `RequestMediator` class.
    - Prints an initialization message.

### 2. Main Execution (Commented Out)

- The code includes a section for main execution (`if __name__ == '__main__':`) with commented-out lines.
- Demonstrates the usage of the `RequestMediator` class with example operations such as user creation, login, variable creation, organization creation, zone creation, and measurement addition.


# Data Validator Module

This Python code defines a `DataValidator` class responsible for validating user input, particularly user registration data such as username, email, and password.

## Class: DataValidator

### Methods:

#### `validate_user(self, user: str, email: str, password: str) -> bool`

- **Description:** Validates user registration data, including username, email, and password.
- **Parameters:**
  - `user` (str): User's username
  - `email` (str): User's email address
  - `password` (str): User's password
- **Returns:** Boolean indicating whether the user data is valid.

#### `validate_username(self, user: str) -> bool`

- **Description:** Validates the username.
- **Parameters:**
  - `user` (str): User's username
- **Returns:** Boolean indicating whether the username is valid.
- **Validation Criteria:**
  - Length between 3 and 12 characters
  - Alphanumeric characters, printable characters, or alphabetic characters only
  - No spaces
  - All characters with ASCII code less than 128

#### `validate_email(self, email: str) -> bool`

- **Description:** Validates the email address.
- **Parameters:**
  - `email` (str): User's email address
- **Returns:** Boolean indicating whether the email address is valid.
- **Validation Criteria:**
  - Follows the standard email format (local-part@domain)
  
#### `validate_password(self, password: str) -> bool`

#DB folder
#Database Module

This Python code represents a database module that provides access to database services, adapters, and schema definitions. It includes several key components such as `DBService`, `DatabaseAdapter`, and various schema models for different entities.

## Module Components:

### 1. `DBService` Class

- **Description:** A class providing services related to database operations.
- **Source:** Defined in the `db_service` module.

### 2. `DatabaseAdapter` Class

- **Description:** A class serving as an adapter for interacting with the database.
- **Source:** Defined in the `db_adapter` module.

### 3. Schema Models:

   - **Org:** Represents the organization schema.
   - **Crop:** Represents the crop schema.
   - **Variable:** Represents the variable schema.
   - **Condition:** Represents the condition schema.
   - **ActuatorType:** Represents the actuator type schema.
   - **Actuator:** Represents the actuator schema.
   - **Measurement:** Represents the measurement schema.
   - **User:** Represents the user schema.
   - **Permission:** Represents the permission schema.
   - **Base:** Represents the base schema.
  
  **Source:** Defined in the `schema` module.

### 4. `create_engine_with_retry` Function

- **Description:** A function for creating a database engine with retry capability.
- **Source:** Defined in the module.

## Module Initialization:

- **`__name__ = 'db'`**
  - Specifies the module name as 'db'.

- **`__all__ = ['DatabaseAdapter', 'DBService', 'Org', 'Crop', 'Variable', 'Condition', 'ActuatorType', 'Actuator', 'Measurement', 'User', 'Permission', 'Base', 'create_engine_with_retry']`**
  - Specifies the list of symbols exported by the module.

## Usage:

- Import this module to access database-related classes and schema definitions in other parts of the application.
- Use the exported symbols for database operations, including interaction with different schema models and creating a database engine.


- **Description:** Validates the user password.
- **Parameters:**
  - `password` (str): User's password
- **Returns:** Boolean indicating whether the password is valid.
- **Validation Criteria:**
  - Length between 8 and 60 characters
  - Alphanumeric characters, alphabetic characters, printable characters, or spaces only
  - All characters with ASCII code less than 128

### Initialization:

- **`__init__(self)`**
  - Initializes the `DataValidator` class.
  - No additional setup is performed in the constructor.

### Usage:

- Call the `validate_user` method with the user's username, email, and password to determine whether the user input is valid.
- The class includes print statements for validation results.


# Database Adapter Module

This Python code defines a database module containing abstract classes `DatabaseClient` and `DatabaseAdapter`. These classes serve as an interface and implementation, respectively, for interacting with a database using a `DBService`. The module includes methods for creating users, organizations, variables, zones, and measurements, as well as login and retrieving measurements.

## Abstract Class: `DatabaseClient` (ABC)

- **Description:** An abstract base class defining the interface for database clients.
- **Methods:**
  - `create_user(self, user: str, password: str) -> User`: Abstract method for creating a user.
  - `create_zone(self, zone: dict)`: Abstract method for creating a zone.
  - `add_measurement(self, measurement: dict)`: Abstract method for adding a measurement.

## Class: `DatabaseAdapter` (Concrete Implementation of `DatabaseClient`)

- **Description:** A concrete implementation of `DatabaseClient` that interacts with the database using a `DBService`.
- **Methods:**

  #### Create Operations

  - `create_user(self, user: str, email: str, password: str) -> User`: Creates a new user in the database.
  - `create_org(self, name: str, description: str, password: str) -> Org`: Creates a new organization in the database.
  - `create_variable(self, name: str, units: str, description: str) -> Variable`: Creates a new variable in the database.
  - `create_zone(self, org_id: str, name: str, latitud: str, longitud: str) -> Crop`: Creates a new zone in the database.
  - `add_measurement(self, datetime: str, crop_id: str, value: float, variable_id: str) -> Measurement`: Adds a new measurement to the database.

  #### Read Operations

  - `login(self, user: str, password: str) -> User`: Logs in a user and returns user data.
  - `get_measurements(self, crop_id: str, variable_id: str) -> list`: Retrieves measurements based on crop and variable IDs.

  #### Initialization

  - `__init__(self)`: Initializes the `DatabaseAdapter` class.
    - Prints an initialization message.
    - Creates an instance of `DBService` for interacting with the database.

## Usage:

- Import this module to use the `DatabaseAdapter` class for database operations.
- Implement a concrete class that inherits from `DatabaseClient` to define specific database interactions.
- The module includes print statements for logging database operations.

# Database Service Module

This Python code defines a `DBService` class responsible for interacting with a PostgreSQL database. It includes methods for creating users, organizations, crops, variables, and measurements, as well as retrieving user and measurement data. The class uses SQLAlchemy for database operations and includes print statements for logging.

## Class: `DBService`

- **Description:** A class providing services for interacting with a PostgreSQL database.
- **Dependencies:** Requires the `schema` module for entity definitions and `create_engine_with_retry` for creating a database engine.
- **Initialization:**
  - Loads environment variables using `dotenv`.
  - Establishes a connection to the database using SQLAlchemy.
  - Creates an instance of the `sessionmaker` for managing sessions.

### Methods:

#### Create Operations

- `create_user(self, user: str, email: str, password: str) -> User`: Creates a new user in the database.
- `create_org(self, name: str, description: str, password: str) -> Org`: Creates a new organization in the database.
- `create_crop(self, org_id: str, name: str, lat: float, lon: float) -> Crop`: Creates a new crop in the database.
- `create_variable(self, name: str, units: str, description: str) -> Variable`: Creates a new variable in the database.
- `add_measurement(self, datetime: str, crop_id: str, value: float, variable_id: str)`: Adds a new measurement to the database.

#### Read Operations

- `get_user(self, username: str) -> User`: Retrieves user data by username.
- `login(self, username: str, password: str) -> User`: Logs in a user and returns user data.
- `get_measurement_by_id(self, measurement_id: str) -> Measurement`: Retrieves a measurement by ID.
- `get_measurements_by_crop_id(self, crop_id: str) -> List[Measurement]`: Retrieves measurements for a specific crop.
- `get_measurements_by_crop_and_variable(self, crop_id: str, variable_id: str) -> List[Measurement]`: Retrieves measurements for a specific crop and variable.

### Main Execution (Commented Out)

- The code includes a section for main execution (`if __name__ == '__main__':`) with commented-out lines.
- Demonstrates the usage of the `DBService` class with example operations such as user creation, organization creation, crop creation, variable creation, and measurement addition.

# Database Schema

This Python code defines a SQLAlchemy database schema for PostgreSQL integration. It includes several classes representing entities such as organizations, crops, variables, conditions, actuator types, actuators, measurements, users, and permissions.

## Base Class: `Base`

- **Description:** Base class for all database models using SQLAlchemy's declarative base.
- **Attributes:**
  - `id`: UUID primary key for all entities.

## Class: `Org`

- **Description:** Represents an organization in the database.
- **Attributes:**
  - `id`: UUID primary key.
  - `name`: Organization name.
  - `description`: Organization description.
  - `password`: Hashed organization password.
  - `crops`: Relationship with the `Crop` class.

## Class: `Crop`

- **Description:** Represents a crop in the database.
- **Attributes:**
  - `id`: UUID primary key.
  - `org_id`: UUID foreign key referencing the `Org` class.
  - `name`: Crop name.
  - `coordinate_latitude`: Latitude coordinate.
  - `coordinate_longitude`: Longitude coordinate.
  - `conditions`: Relationship with the `Condition` class.
  - `actuators`: Relationship with the `Actuator` class.
  - `measurements`: Relationship with the `Measurement` class.

## Class: `Variable`

- **Description:** Represents a variable in the database.
- **Attributes:**
  - `id`: UUID primary key.
  - `name`: Variable name.
  - `units`: Variable units.
  - `description`: Variable description.

## Class: `Condition`

- **Description:** Represents a condition in the database.
- **Attributes:**
  - `id`: UUID primary key.
  - `crop_id`: UUID foreign key referencing the `Crop` class.
  - `variable_id`: UUID foreign key referencing the `Variable` class.
  - `min_value`: Minimum value for the condition.
  - `max_value`: Maximum value for the condition.
  - `crop`: Relationship with the `Crop` class.
  - `variable`: Relationship with the `Variable` class.

## Class: `ActuatorType`

- **Description:** Represents an actuator type in the database.
- **Attributes:**
  - `id`: UUID primary key.
  - `name`: Actuator type name.
  - `description`: Actuator type description.

## Class: `Actuator`

- **Description:** Represents an actuator in the database.
- **Attributes:**
  - `id`: UUID primary key.
  - `name`: Actuator name.
  - `mqtt_topic`: MQTT topic for the actuator.
  - `crop_id`: UUID foreign key referencing the `Crop` class.
  - `actuator_type_id`: UUID foreign key referencing the `ActuatorType` class.
  - `start_time`: Start time for the actuator.
  - `end_time`: End time for the actuator.
  - `crop`: Relationship with the `Crop` class.
  - `actuator_type`: Relationship with the `ActuatorType` class.

## Class: `Measurement`

- **Description:** Represents a measurement in the database.
- **Attributes:**
  - `id`: UUID primary key.
  - `datetime`: Date and time of the measurement.
  - `crop_id`: UUID foreign key referencing the `Crop` class.
  - `value`: Measurement value.
  - `variable_id`: UUID foreign key referencing the `Variable` class.
  - `crop`: Relationship with the `Crop` class.
  - `variable`: Relationship with the `Variable` class.

## Class: `User`

- **Description:** Represents a user in the database.
- **Attributes:**
  - `id`: UUID primary key.
  - `email`: User email.
  - `username`: Username.
  - `password`: Hashed user password.

## Class: `Permission`

- **Description:** Represents a permission in the database.
- **Attributes:**
  - `id`: UUID primary key.
  - `user_id`: UUID foreign key referencing the `User` class.
  - `org_id`: UUID foreign key referencing the `Org` class.
  - `crop_id`: UUID foreign key referencing the `Crop` class.
  - `granted`: Boolean indicating if the permission is granted.
  - `_id`: Unique identifier combining user, organization, and permission type.
  - `user`: Relationship with the `User` class.
  - `org`: Relationship with the `Org` class.
  - `crop`: Relationship with the `Crop` class.

## Function: `create_engine_with_retry`

- **Description:** Defines a SQLAlchemy engine with a retry mechanism for connecting to the database.
- **Parameters:**
  - `db_url`: Database URL.
- **Returns:**
  - SQLAlchemy engine.

### Main Execution (Commented Out)

- The code includes a section for main execution (`if __name__ == '__main__':`) with commented-out lines.
- Demonstrates the usage of environment variables for database configuration, engine creation, and schema initialization.

## License

[MATICAS](https://github.com/DaveAlsina/arquitectura_del_computador/blob/main/src/main.py)
