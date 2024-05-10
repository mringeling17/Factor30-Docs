CREATE TABLE measurements (
    id SERIAL PRIMARY KEY,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    wind_speed FLOAT NOT NULL,
    risk_level VARCHAR(255) NOT NULL,
    uuid VARCHAR(36) NOT NULL,
    received_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);
