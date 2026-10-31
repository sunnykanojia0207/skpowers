# Architecture

How the system is built and why. Agents follow this when deciding where code goes and how parts talk to each other. Record significant decisions in `docs/ARCHITECTURE_DECISIONS.md`.

## 1. Overview
One paragraph: the main parts and how a request flows through them.

## 2. Pattern
- Pattern: modular monolith / monolith / services / serverless / other
- Why (the constraint that drove it):

## 3. Stack
| Concern | Choice | Notes |
|---|---|---|
| Frontend | | |
| Backend / API | | |
| Database | | see `docs/DATABASE.md` |
| Authentication | | see `docs/SECURITY.md` |
| File storage | | |
| Hosting | | |
| Payments | | |
| Email / notifications | | |
| Analytics / monitoring | | |

## 4. Components and responsibilities
For each component (frontend, API, workers, database, integrations): what it owns and what it must not do.

## 5. Request and data flow
The normal path step by step, e.g. user submits form → client validation → API → authentication → authorization → business rules → database → response → UI update.

## 6. Project structure
```text
(folder tree, one line per folder saying what belongs there)
```

## 7. Dependency rules
Which layers may depend on which, e.g. "UI never talks to the database directly", "business rules live in services, not route handlers".

## 8. Failure behaviour
What the user sees and what the system does when the database is unavailable, an API call times out, a third-party service fails, authentication fails, or a background job fails.

## 9. Performance and scale
Targets (latency, load) and the known bottlenecks to watch.
