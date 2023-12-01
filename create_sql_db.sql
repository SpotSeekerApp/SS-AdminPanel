CREATE DATABASE spotseeker;

CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" varchar,
  "name" varchar,
  "surname" varchar,
  "age" integer,
  "email" varchar,
  "password" varchar
);

CREATE TABLE "admins" (
  "id" SERIAL PRIMARY KEY,
  "username" varchar,
  "name" varchar,
  "surname" varchar,
  "age" integer,
  "email" varchar,
  "password" varchar
);

CREATE TABLE "placeholder" (
  "id" SERIAL PRIMARY KEY,
  "username" varchar,
  "name" varchar,
  "surname" varchar,
  "age" integer,
  "email" varchar,
  "password" varchar
);