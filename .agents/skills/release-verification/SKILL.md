---
name: release-verification
description: Prepare and verify CI/CD, staging, production releases, observability, data migration safety, and rollback plans.
---
# Release Verification

1. Discover actual build/test scripts, CI workflows, hosting, secrets, environment separation, migrations, and deployment process.
2. Ensure PR gates include format/lint, types, unit/integration tests, build, and relevant security/dependency scans.
3. Use least-privilege workflow permissions, protected branches/environments, pinned third-party GitHub Actions SHAs for production, and short-lived identity where supported.
4. Keep secrets in secret stores; never print them or include them in generated artifacts.
5. Ensure staging uses test data and non-production credentials. Verify the same artifact intended for release where practicable.
6. Before migration, assess locking, backward compatibility, data loss, backup, recovery, and rollback. Never run production destructive migrations without explicit approval.
7. After deploy, verify health/readiness, core workflows, auth/authorization, database connectivity, logs, error monitoring, and relevant performance indicators.
8. Ensure an actionable rollback/recovery procedure exists and is documented.
9. Report release evidence: commit/build identifier, environment, checks run/results, smoke-test evidence, outstanding risks, and manual steps not verified.
10. Never state “deployed” or “production ready” unless real deployment and verification occurred.
