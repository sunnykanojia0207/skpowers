# API

The source of truth for API contracts. Agents implement and test against these; changes are documented here first.

## Conventions
- Base URL and versioning:
- Authentication:
- Error format (shape and codes):
- Pagination:
- Rate limits:
- Idempotency (which writes accept an idempotency key):

## Endpoint: `METHOD /resource`
- **Purpose:**
- **Permission:** role and ownership rule
- **Path and query parameters:** names, types, constraints, defaults
- **Request body:** schema and example
- **Success response:** status, schema, example
- **Errors:** status codes and meaning (validation, unauthenticated, forbidden, not found, conflict)
- **Side effects:** writes, events, emails, external calls
- **Retries:** behaviour on duplicate or partial requests
- **Tests:** success, invalid input, unauthenticated, forbidden
