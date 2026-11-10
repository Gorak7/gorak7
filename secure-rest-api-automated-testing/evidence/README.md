# Evidence capture guide

No fabricated screenshots or unrun test reports are included. After running locally, create evidence/screenshots and capture:
1. Health check HTTP 200.
2. Token issuance HTTP 201 (mask token).
3. Unauthenticated request HTTP 401.
4. Startup create HTTP 201.
5. Startup list and pagination.
6. Startup PATCH update.
7. Validation failure HTTP 422.
8. Mentor and programme CRUD.
9. Postman collection runner actual summary.
10. PHPUnit terminal output.
11. SQL audit log rows.
12. GitHub Actions successful run.

Export actual reports:
```bash
mkdir -p evidence/screenshots
composer lint | tee evidence/php-lint-output.txt
composer test | tee evidence/phpunit-output.txt
newman run postman/Secure-REST-API.postman_collection.json -e postman/Secure-REST-API.local.postman_environment.json --reporters cli,junit --reporter-junit-export evidence/newman-junit.xml | tee evidence/newman-output.txt
```

Audit query:
```sql
SELECT id,user_id,action,resource,resource_id,created_at FROM audit_logs ORDER BY id DESC LIMIT 50;
```

Mask tokens, passwords and personal data. Update docs/TEST-REPORT.md with real execution counts and defects. Never present illustrative API examples as captured evidence.