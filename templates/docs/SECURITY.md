# Security

What must be protected and how. Agents treat these as requirements, not suggestions; authorization is always enforced on the server.

## 1. Authentication
- Provider:
- Methods (email/password, OAuth, magic link, passkeys):
- Session / token handling:

## 2. Authorization
| Role | Can | Cannot |
|---|---|---|
| | | |

Ownership rules (who may read or change which records):

## 3. Secrets and environment
- Never hard-code or commit credentials; never expose private keys to the client.
- Public variables:
- Private variables (names only; values live in the secret manager or `.env`, never in git):

## 4. API protection
Input validation, rate limits, CORS, request size limits, webhook signature checks.

## 5. Data protection
Sensitive data, encryption, retention, deletion on request.

## 6. Logging
- Never log: passwords, tokens, API keys, sensitive personal data.
- Do log: authentication events, permission denials, important actions, errors.

## 7. File uploads
Allowed types, size limits, validation, storage location, scanning.

## 8. Checklist (per feature)
- [ ] Authenticated where required
- [ ] Authorization checked on the server, including ownership
- [ ] All untrusted input validated on the server
- [ ] Secrets protected
- [ ] Rate limiting considered
- [ ] Errors don't leak internals
- [ ] New dependencies reviewed
