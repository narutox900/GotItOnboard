CREATE TABLE if not exists users (
    id INTEGER PRIMARY KEY,
    username text, 
    password text);

CREATE TABLE if not exists items (
    id INTEGER PRIMARY KEY,
    name text, 
    price real);