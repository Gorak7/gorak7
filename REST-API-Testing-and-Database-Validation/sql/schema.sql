-- Local practice database for QA API validation.
-- This dataset is independent from JSONPlaceholder and uses synthetic data.
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id       INTEGER PRIMARY KEY,
    user_id  INTEGER NOT NULL,
    title    TEXT NOT NULL CHECK (length(trim(title)) > 0),
    body     TEXT NOT NULL CHECK (length(trim(body)) > 0)
);

INSERT INTO posts (id, user_id, title, body) VALUES
(1, 1, 'sunt aut facere repellat provident occaecati', 'Synthetic sample body for SQL validation.'),
(2, 1, 'qui est esse', 'Second synthetic post for aggregation checks.'),
(3, 2, 'ea molestias quasi exercitationem', 'Third synthetic post for cross-user checks.'),
(4, 2, 'eum et est occaecati', 'Fourth synthetic post for validation practice.');

-- Quick sanity check: should display four rows.
SELECT id, user_id, title FROM posts ORDER BY id;
