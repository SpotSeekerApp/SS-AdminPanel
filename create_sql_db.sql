CREATE DATABASE spotseeker;

CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "surname" varchar,
  "age" integer,
  "email" varchar,
  "password" varchar
);

CREATE TABLE "admins" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "surname" varchar,
  "age" integer,
  "email" varchar,
  "password" varchar
);

CREATE TABLE "placeowners" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "surname" varchar,
  "age" integer,
  "email" varchar,
  "password" varchar
);


INSERT INTO admins(name, surname, age, email, password)
VALUES ('betul', 'altundal', 21, 'zeynepbetulaltundal@gmail.com', '123456');