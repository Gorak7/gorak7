-- Run after creating/registering the curated Delta table as `sales`.

-- 1. Total revenue
SELECT ROUND(SUM(revenue), 2) AS total_revenue
FROM sales;

-- 2. Revenue by region
SELECT
    region,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;

-- 3. Revenue by product
SELECT
    product,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC;

-- 4. Monthly revenue trend
SELECT
    DATE_FORMAT(order_date, 'yyyy-MM') AS month,
    ROUND(SUM(revenue), 2) AS monthly_revenue
FROM sales
GROUP BY DATE_FORMAT(order_date, 'yyyy-MM')
ORDER BY month;

-- 5. Customer segment analysis
SELECT
    customer_segment,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
GROUP BY customer_segment
ORDER BY total_revenue DESC;

-- 6. Top orders
SELECT
    order_id,
    region,
    product,
    quantity,
    revenue
FROM sales
ORDER BY revenue DESC
LIMIT 10;
