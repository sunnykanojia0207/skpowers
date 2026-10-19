---
name: architecture-planning
description: Turn a product brief into requirements, stack decisions, system boundaries, data/API contracts, folder structure, and a phased implementation plan.
---
# Architecture Planning

1. Identify users, jobs-to-be-done, critical journeys, acceptance criteria, nonfunctional needs, constraints, integrations, budget, data sensitivity, and release target.
2. Separate MVP from future features. State assumptions and unresolved decisions.
3. Compare viable technology options against product fit, team familiarity, ecosystem maturity, operational burden, security, testing, and cost. Use official current docs for version-sensitive choices.
4. Prefer a modular monolith until independent deployment/scaling/ownership requirements justify services.
5. Draw component/data-flow and trust-boundary diagrams. Define authn/authz, data ownership, failure modes, observability, deployment, and backups.
6. Define an adapted folder structure that reflects project domains. Don't create empty packages or microservices just to fill a template.
7. Specify data model, migrations, API contracts, validation, error shapes, and tests before building dependent components.
8. Write `docs/PRODUCT_REQUIREMENTS.md`, `docs/ARCHITECTURE.md`, `docs/ARCHITECTURE_DECISIONS.md`, `docs/DATA_MODEL.md`, `docs/API_CONTRACTS.md`, and `docs/PROJECT_STRUCTURE.md` when appropriate.
9. End with a milestone plan, dependencies, risks, verification strategy, and explicit production-readiness criteria.
