# Testing

How we know it works. Agents don't stop at "the code looks right": they run the checks and verify the critical journeys.

## 1. What must never break
Critical functionality and journeys (sign up, sign in, core create/edit flows, checkout, permissions):
-

## 2. Test types and tools
| Type | Covers | Tool |
|---|---|---|
| Unit | business logic, utilities, components | |
| Integration | API, database, auth, external services | |
| End-to-end | critical journeys in a real browser or device | |

## 3. Layout
```text
tests/unit/  tests/integration/  tests/e2e/   (or the project's own convention)
```

## 4. Critical flows
For each: name, steps, expected result, including failure and empty states.

## 5. Coverage priorities
Business rules, authentication and authorization, payments, data mutations, critical journeys. Coverage target:

## 6. Definition of done
- [ ] Tests pass (new behaviour has tests; each bug fix adds a regression test)
- [ ] Lint and type checks pass
- [ ] Build passes
- [ ] Critical flow verified end to end
