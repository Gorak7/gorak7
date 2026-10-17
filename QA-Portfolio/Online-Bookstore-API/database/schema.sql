CREATE DATABASE IF NOT EXISTS bookstore;
USE bookstore;
CREATE TABLE IF NOT EXISTS books (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 title VARCHAR(180) NOT NULL,
 author VARCHAR(120) NOT NULL,
 price DECIMAL(10,2) NOT NULL CHECK (price > 0),
 stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0)
);
INSERT INTO books(title,author,price,stock)
SELECT 'Clean Code','Robert C. Martin',499.00,10
WHERE NOT EXISTS (SELECT 1 FROM books WHERE title='Clean Code');
INSERT INTO books(title,author,price,stock)
SELECT 'The Pragmatic Programmer','Andrew Hunt and David Thomas',599.00,8
WHERE NOT EXISTS (SELECT 1 FROM books WHERE title='The Pragmatic Programmer');
INSERT INTO books(title,author,price,stock)
SELECT 'Designing Data-Intensive Applications','Martin Kleppmann',799.00,5
WHERE NOT EXISTS (SELECT 1 FROM books WHERE title='Designing Data-Intensive Applications');
