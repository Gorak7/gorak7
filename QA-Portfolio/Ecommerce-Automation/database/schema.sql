CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

CREATE TABLE IF NOT EXISTS products (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(120) NOT NULL,
  description VARCHAR(500),
  price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS orders (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  customer_email VARCHAR(180) NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'CREATED',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO products(name, description, price, stock)
SELECT 'Wireless Mouse', 'Ergonomic wireless mouse', 799.00, 25
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name='Wireless Mouse');
INSERT INTO products(name, description, price, stock)
SELECT 'Mechanical Keyboard', 'Compact mechanical keyboard', 2499.00, 12
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name='Mechanical Keyboard');
INSERT INTO products(name, description, price, stock)
SELECT 'USB-C Hub', 'Seven-port USB-C hub', 1599.00, 18
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name='USB-C Hub');
