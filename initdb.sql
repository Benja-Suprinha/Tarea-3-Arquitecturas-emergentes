CREATE TABLE admin
(
    username TEXT PRIMARY KEY,
    password TEXT
);

CREATE TABLE company(
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT,
    company_api_key TEXT);


CREATE TABLE location
(
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    location_name TEXT,
    location_country TEXT,
    location_city TEXT,
    location_meta TEXT,
    location_api_key TEXT NOT NULL,
    FOREIGN KEY(company_id) REFERENCES company(company_id)
);


CREATE TABLE sensor
(
    sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER,
    sensor_name TEXT,
    sensor_category TEXT,
    sensor_meta TEXT,
    sensor_api_key TEXT,
    FOREIGN KEY(location_id) REFERENCES location(location_id)
);

CREATE TABLE sensor_data
(
    sensor_data_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER,
    timestamp INTEGER NOT NULL,
    data TEXT,
    FOREIGN KEY(sensor_id) REFERENCES sensor(sensor_id)
);

INSERT INTO company (company_id, company_name, company_api_key) VALUES(1, 'ACME Inc.', '1234'),(2, 'XYZ Corp.', '1232'),(3, 'Testing', 'Testing');