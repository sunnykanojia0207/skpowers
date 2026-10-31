# Project Brief (PRD)

What we are building, for whom, and how we will know it works. Agents read this before any significant change. Replace every placeholder with a real decision, or write it down as an open question; never leave a guess implicit.

## 1. Product
- Name:
- One sentence: what it is and who it is for.
- Type: SaaS / mobile app / marketplace / internal tool / API / other
- Success metric (the one number that matters):

## Platforms
Tick what applies; the toolkit picks skills from these boxes (`python scripts/sync_toolkit.py --explain`).
- [ ] Web
- [ ] Android
- [ ] iOS
- [ ] Public API
- [ ] Admin portal
- [ ] AI/LLM features

## 2. Problem
- The problem, in the user's words:
- Why it matters now:
- How people solve it today, and why that falls short:

## 3. Users
For each user type: who they are, what they need, what frustrates them today.
-

## 4. User stories
"As a [user], I want to [action] so that [outcome]."
-

## 5. Features
For each feature:
- **Purpose:**
- **Flow:** the steps (details in `docs/UX_FLOWS.md`)
- **Inputs / outputs:**
- **Acceptance criteria** (testable; Given/When/Then where useful):
- **Edge cases:**

## 6. Scope
- MVP (must have):
- Nice to have:
- Later:
- **Non-goals** (explicitly out of this version):

## 7. Constraints
- Technical (stack preferences, hosting, regions):
- Budget / cost ceiling:
- Deadline:
- Third-party integrations:
- Data sensitivity / compliance:
- Expected traffic / scale:

## 8. Assumptions and open questions
- Assumptions (believed but not verified):
- Open questions (decisions still to make; agents ask rather than guess):

## 9. Release expectations
- Staging environment:
- Production approver:
- CI checks:
- Monitoring / alerts:
- Backup and rollback:

## 10. Definition of done
- [ ] Acceptance criteria met
- [ ] Critical user flows work, including loading, empty, error and success states
- [ ] Tests, lint, type checks and build pass
- [ ] Security rules in `docs/SECURITY.md` respected
- [ ] Docs updated where behaviour changed

Related: `DESIGN.md` (design system), `docs/ARCHITECTURE.md`, `docs/DATABASE.md`, `docs/API.md`, `docs/SECURITY.md`, `docs/UX_FLOWS.md`, `docs/CODE_STYLE.md`, `docs/TESTING.md`.
