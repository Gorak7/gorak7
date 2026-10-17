-- Run against the bookstore DB after starting the app.
USE bookstore;

-- Inspect seeded and created books
SELECT id, title, author, price, stock FROM books ORDER BY id;

-- These integrity checks should return zero rows
SELECT id, title, price FROM books WHERE price <= 0;
SELECT id, title, stock FROM books WHERE stock < 0;

-- After a demo order, verify stock is decremented for the ordered book.
