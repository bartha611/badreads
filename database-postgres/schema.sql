CREATE TABLE person (
	personId SERIAL PRIMARY KEY,
	username VARCHAR(50) NOT NULL,
	password VARCHAR NOT NULL,
	email VARCHAR(70) NOT NULL
);
CREATE TABLE books (
	bookId SERIAL PRIMARY KEY,
	isbn INTEGER NOT NULL,
	title VARCHAR NOT NULL,
	author VARCHAR(30) NOT NULL,
	year SMALLINT NOT NULL,
	average_score FLOAT(3) NOT NULL DEFAULT 0,
	review_count INT NOT NULL DEFAULT 0
);
CREATE TABLE reviews (
	reviewId SERIAL PRIMARY KEY,
	review_rating SMALLINT NOT NULL,
	review_text TEXT,
	personId INT  REFERENCES person,
	bookId INT REFERENCES books
);