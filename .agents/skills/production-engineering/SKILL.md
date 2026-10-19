---
name: production-engineering
description: Apply an end-to-end, evidence-based software delivery workflow for web, mobile, API, and AI applications, especially when planning features, implementing changes, reviewing readiness, or preparing releases.
---
# Production Engineering Workflow

1. Inspect the repository, git status, project instructions, manifests, tests, CI, and deploy configuration.
2. Convert the request into observable acceptance criteria. For significant work, document architecture decisions and risks.
3. Plan implementation as small vertical slices. Avoid scaffolding that is not required by the product.
4. Implement with secure input validation, server-side authorization, explicit error handling, and clear domain boundaries.
5. Add tests for acceptance criteria and regression risks. Prefer test-first development for behavioral changes.
6. Run the real project lint/type/test/build commands. Use browser E2E or native/mobile tests when relevant. Never invent results.
7. Review dependency changes, secrets, authorization, tenant isolation, sensitive logging, and destructive operations.
8. For release work, verify CI, staging smoke tests, migrations, health/readiness, monitoring, backups, and rollback before recommending production.
9. Require explicit human approval for production deployment and destructive operations.
10. Finish with a truthful report: files changed, commands run, results, known gaps, and risks.

## Stop conditions
Stop and ask for approval before deleting data, rewriting history, changing cloud IAM/network/DNS/billing, rotating production secrets, or applying production migrations/deployment. If a test or tool is unavailable, disclose the blocker rather than bypassing the gate.
