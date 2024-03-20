CREATE DATABASE IF NOT EXISTS my_database;


USE my_database;

CREATE TABLE IF NOT EXISTS input_data (
    input_str VARCHAR(255) NOT NULL,
    unique_integer VARCHAR(255) NOT NULL PRIMARY KEY
);

select *from input_data;
select input_str from input_data where unique_integer="bnF";

