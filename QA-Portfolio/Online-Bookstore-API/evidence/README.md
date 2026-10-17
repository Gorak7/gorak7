# Evidence checklist

Capture screenshots/results from actual local runs:
- `01-bookstore-homepage.png`: catalog UI
- `02-search-results.png`: search by title/author
- `03-postman-list-books.png`: Postman response and assertions
- `04-postman-invalid-payload.png`: validation response
- `05-swagger-ui.png`: OpenAPI endpoint documentation
- `06-sql-validation.png`: SQL query output
- `07-rest-assured-report.png`: Maven/Surefire results
- `08-github-actions.png`: workflow run in GitHub

Useful SQL:
```sql
SELECT id, title, author, price, stock FROM books ORDER BY id;
```
Store sanitized output only. Never claim tests passed until the run actually completed. Keep secrets and personal data out of screenshots.
