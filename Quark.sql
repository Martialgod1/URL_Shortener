CREATE DATABASE IF NOT EXISTS my_database;


USE my_database;

CREATE TABLE IF NOT EXISTS input_data (
    input_str VARCHAR(255) NOT NULL,
    unique_integer VARCHAR(255) NOT NULL PRIMARY KEY
);
