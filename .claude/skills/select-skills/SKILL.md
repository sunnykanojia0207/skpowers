---
name: select-skills
description: Pick and enable the right skills for this project from its requirements. Use at the start of a new project, after the user describes or changes requirements, after adding a platform (web, iOS, Android, API, AI features) or a significant dependency (framework, database, ORM, auth, payments, animation library), or when the user asks which skills or MCP servers apply.
---

# Select skills for this project

The toolkit chooses skill profiles from the project itself. Your job is to keep that input accurate, run the selection, and report what changed. Never hand-edit `.agents/skills/` copies or generated MCP files.

## Steps

1. **Update the brief.** If the user described requirements in conversation, reflect them in `docs/PROJECT_BRIEF.md`: tick the platform checkboxes (`- [x] Web`, `- [x] iOS`, `- [x] Android`, `- [x] Public API`, `- [x] Admin portal`, `- [x] AI/LLM features`) and fill in product, journeys and constraints. Show the user the brief changes.

2. **Preview the selection.**
   ```bash
   python scripts/sync_toolkit.py --explain
   ```
   It lists every enabled profile and skill with the reason (a dependency, a file, a brief checkbox), plus suggestions it will not enable on its own.

3. **Apply it.**
   ```bash
   python scripts/sync_toolkit.py
   ```
   This copies the matching skills into `.agents/skills/` for every tool (and `.claude/skills/` for Claude Code) and removes skills that no longer match. Hand-written skills are never touched.

4. **Handle suggestions.** Profiles listed under "Suggested" (for example `security`, `ripwire`) pre-approve shell commands or need extra software. Explain why they were suggested and add them to `skillProfiles` in `toolkit.config.json` only if the user agrees, then run step 3 again.

5. **MCP servers are not enabled automatically.** If the stack would benefit from one (for example `supabase`, `next-devtools`, `magicui`, `github`), name it and ask; enabling a server means setting `"enabled": true` in `toolkit.config.json` and syncing.

6. **Report.** Tell the user which profiles were added or removed and why. Some tools load skills only at session start: suggest restarting the session if newly enabled skills do not appear.

## Notes

- To force a profile on, add it to `skillProfiles`; to turn automatic selection off, set `"autoSkills": false` in `toolkit.config.json`.
- If the selection misses an obvious need, add the profile to `skillProfiles` rather than editing the detection rules in a product repository; propose rule changes to the toolkit repository instead.
- After the selection, use the enabled skills whose descriptions match each task before writing code.
