# Project documentation templates

The installer copies these into a project's `docs/` folder (never overwriting existing files). Together with `docs/PROJECT_BRIEF.md` (the PRD), `DESIGN.md` (the design system) and `AGENTS.md` (agent rules), they give coding agents the context to implement instead of guess.

Start with the smallest useful set: the brief, then the documents the next feature touches. Replace placeholders with real decisions or explicit open questions, and keep them in step with the code.

| Document | Answers |
|---|---|
| `docs/PROJECT_BRIEF.md` | What are we building, for whom, and what counts as done? |
| `DESIGN.md` | What should it look and feel like? (Google DESIGN.md format; lint with `npx @google/design.md@0.4.0 lint DESIGN.md`) |
| `docs/ARCHITECTURE.md` + `docs/ARCHITECTURE_DECISIONS.md` | How is the system built, and why? |
| `docs/DATABASE.md` | What data exists and how does it relate? |
| `docs/API.md` | What are the API contracts? |
| `docs/SECURITY.md` | What must be protected and how? |
| `docs/UX_FLOWS.md` | How do users move through the product? |
| `docs/CODE_STYLE.md` | How should code be written? |
| `docs/TESTING.md` | How will we know it works? |

Structure adapted from "The Vibe Coding Blueprint" (context → implementation → validation).
