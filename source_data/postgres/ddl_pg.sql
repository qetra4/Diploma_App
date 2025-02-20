CREATE TABLE device_user (
    id SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    passwd VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES device_user(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL
);

CREATE TABLE steps (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES device_user(id) ON DELETE CASCADE,
    Value INTEGER NOT NULL,
    Time TIMESTAMP NOT NULL
);

CREATE TABLE distance (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES device_user(id) ON DELETE CASCADE,
    Value FLOAT NOT NULL,
    Time TIMESTAMP NOT NULL
);

CREATE TABLE pulse (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES device_user(id) ON DELETE CASCADE,
    Value INTEGER NOT NULL,
    Time TIMESTAMP NOT NULL
);

CREATE TABLE calories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES device_user(id) ON DELETE CASCADE,
    Value INTEGER NOT NULL,
    Time TIMESTAMP NOT NULL
);

CREATE TABLE weight (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES device_user(id) ON DELETE CASCADE,
    Value FLOAT NOT NULL,
    Time TIMESTAMP NOT NULL
);

COPY device_user(id, login, passwd, name)
FROM '/data/users.csv' DELIMITER ',' CSV HEADER;

COPY role(id, user_id, role)
FROM '/data/roles.csv' DELIMITER ',' CSV HEADER;

COPY steps(id, user_id, Value, Time)
FROM '/data/steps.csv' DELIMITER ',' CSV HEADER;

COPY distance(id, user_id, Value, Time)
FROM '/data/distance.csv' DELIMITER ',' CSV HEADER;

COPY pulse(id, user_id, Value, Time)
FROM '/data/pulse.csv' DELIMITER ',' CSV HEADER;

COPY calories(id, user_id, Value, Time)
FROM '/data/calories.csv' DELIMITER ',' CSV HEADER;

COPY weight(id, user_id, Value, Time)
FROM '/data/weight.csv' DELIMITER ',' CSV HEADER;
