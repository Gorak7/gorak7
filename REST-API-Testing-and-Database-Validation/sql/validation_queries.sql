-- Run after sql/schema.sql in SQLite.
-- 1. Confirm the total number of seeded rows (expected: 4).
SELECT COUNT(*) AS total_posts FROM posts;

-- 2. Check required fields for NULL or blank values (expected: zero rows).
SELECT * FROM posts
WHERE id IS NULL
   OR user_id IS NULL
   OR title IS NULL OR length(trim(title)) = 0
   OR body IS NULL OR length(trim(body)) = 0;

-- 3. Find duplicate IDs (expected: zero rows; id is a primary key).
SELECT id, COUNT(*) AS occurrences
FROM posts
GROUP BY id
HAVING COUNT(*) > 1;

-- 4. Validate record counts by user (expected: user 1 = 2; user 2 = 2).
SELECT user_id, COUNT(*) AS post_count
FROM posts
GROUP BY user_id
ORDER BY user_id;

-- 5. Find posts that do not match the expected user IDs (expected: zero rows).
SELECT * FROM posts WHERE user_id NOT IN (1, 2);

-- 6. Retrieve a known record and compare values with the expected test fixture.
SELECT id, user_id, title, body FROM posts WHERE id = 1;

-- 7. Find suspiciously long titles for a simple boundary review (review results).
SELECT id, length(title) AS title_length, title
FROM posts
WHERE length(title) > 100;
