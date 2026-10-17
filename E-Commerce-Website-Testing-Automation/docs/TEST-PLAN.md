# Test Plan — E-Commerce Demo

| ID | Scenario | Expected result |
|---|---|---|
| UI-001 | Open storefront | Four product cards render |
| UI-002 | Search headphones | One matching product remains |
| UI-003 | Add product | Cart count and total update |
| UI-004 | Checkout with empty cart | Validation message appears; no order created |
| UI-005 | Valid checkout | Confirmation and order ID appear |
| API-001 | GET /api/health | HTTP 200, status UP |
| API-002 | GET /api/products | HTTP 200, four products |
| API-003 | POST valid /api/orders | HTTP 201 and generated order ID |
| API-004 | POST invalid email | HTTP 400 validation response |
| DB-001 | Inspect customer_orders in H2 | Order row persists |

## API commands

    curl -i http://localhost:8080/api/health
    curl -i http://localhost:8080/api/products
    curl -i -X POST http://localhost:8080/api/orders -H "Content-Type: application/json" -d "{\"name\":\"QA Demo\",\"email\":\"qa.demo@example.com\",\"productIds\":[1]}"
    curl -i -X POST http://localhost:8080/api/orders -H "Content-Type: application/json" -d "{\"name\":\"\",\"email\":\"invalid\",\"productIds\":[1]}"

## Execution record (fill after actual run)
- Date/time:
- Commit tested:
- Java/Maven/Chrome versions:
- Command:
- Passed / failed / skipped:
- Defects:
- Report path:
