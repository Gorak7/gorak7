-- Run against database qadb after the app has started.
SELECT id,name,email,role FROM user_records ORDER BY id;
-- Expected zero rows: duplicate normalized emails
SELECT lower(email),count(*) FROM user_records GROUP BY lower(email) HAVING count(*)>1;
-- Expected zero rows: required fields missing or blank
SELECT id FROM user_records WHERE name IS NULL OR trim(name)='' OR email IS NULL OR trim(email)='' OR role IS NULL OR trim(role)='';
SELECT count(*) AS total_records FROM user_records;
-- Optional cleanup: replace the email with a synthetic test email first.
-- DELETE FROM user_records WHERE email='qa.demo@example.com';
