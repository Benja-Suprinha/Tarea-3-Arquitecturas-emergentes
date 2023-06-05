CREATE TABLE Admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
);

CREATE TABLE Company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT,
    company_api_key TEXT
);

CREATE TABLE Location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    location_name TEXT,
    location_country TEXT,
    location_city TEXT,
    location_meta TEXT,
    FOREIGN KEY (company_id) REFERENCES Company(id)
);

CREATE TABLE Sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER,
    sensor_id INTEGER,
    sensor_name TEXT,
    sensor_category TEXT,
    sensor_meta TEXT,
    sensor_api_key TEXT,
    FOREIGN KEY (location_id) REFERENCES Location(id)
);

CREATE TABLE SensorData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER,
    -- Agrega los campos correspondientes a los datos del sensor según tus necesidades
    FOREIGN KEY (sensor_id) REFERENCES Sensor(id)
);
