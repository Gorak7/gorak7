-- Run after starting the e-commerce database. These are validation queries, not pre-generated results.
USE ecommerce;

-- Product records visible to the UI/API
SELECT id, name, price, stock FROM products ORDER BY id;

-- Basic integrity checks: both queries should return zero rows
SELECT id, name, price FROM products WHERE price < 0;
SELECT id, name, stock FROM products WHERE stock < 0;

-- If demo orders are persisted by a future implementation, validate order totals here.
