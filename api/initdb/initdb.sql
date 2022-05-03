CREATE DATABASE disco;

\c disco;

CREATE TABLE filters (
  id serial PRIMARY KEY NOT NULL,
  freq REAL,
  gain REAL
);

INSERT INTO filters (freq, gain) VALUES (440.0, 0.0);
