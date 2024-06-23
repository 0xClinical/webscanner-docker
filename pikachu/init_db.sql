CREATE DATABASE IF NOT EXISTS pikachu;
USE pikachu;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password CHAR(32) NOT NULL
);

INSERT INTO users (username, password) VALUES ('admin', MD5('123456'));


CREATE TABLE IF NOT EXISTS member (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password CHAR(32) NOT NULL
);

INSERT INTO users (username, password) VALUES ('lili', MD5('123456'));
